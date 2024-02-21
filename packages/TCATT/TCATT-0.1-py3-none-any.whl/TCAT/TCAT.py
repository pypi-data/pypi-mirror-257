import pandas as pd
import os
import scanpy as sc
from . import annotate
import json
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from multiprocessing import Process, Queue

def TCAT(adata):
    ### number是用户输入的adata用sc取出的每个over_clustering的前marker数
    # adata = sc.read_h5ad(file_path)
    
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    print(f'adata cell number :',adata.X.shape[0])

    if 'predicted_labels_0' in adata.obs:    
        del adata.obs['predicted_labels_0']
        del adata.obs['over_clustering_0']
        del adata.obs['majority_voting_0']
        del adata.obs['predicted_labels_1']
        del adata.obs['over_clustering_1']
        del adata.obs['majority_voting_1']
    global adata_None_T
    # 第一步 鉴别T/非T
    adata.var['CD3'] = adata.var_names.isin(['CD3D','CD3E','CD3G'])
    sc.pp.calculate_qc_metrics(adata, qc_vars=['CD3'], percent_top=None, log1p=False, inplace=True)
    adata_T = adata[adata.obs.total_counts_CD3 > 0]
    adata_None_T = adata[adata.obs.total_counts_CD3 == 0]
    adata_None_T.obs['marker_results'] = 'None_T'

    print(f'adata_T cell number :',adata_T.X.shape[0])
    print(f'adata_None_T cell number :',adata_None_T.X.shape[0])
    # 第二步 celltypist+marker 分出直出细胞和CD4/8
    # 计算每个细胞中CD4的表达量
    adata_T.var['CD4'] = adata_T.var_names.isin(['CD4'])
    sc.pp.calculate_qc_metrics(adata_T, qc_vars=['CD4'], percent_top=None, log1p=False, inplace=True)
    
    # 计算每个细胞中CD8的表达量
    adata_T.var['CD8'] = adata_T.var_names.isin(['CD8A','CD8B'])
    sc.pp.calculate_qc_metrics(adata_T, qc_vars=['CD8'], percent_top=None, log1p=False, inplace=True)

    if float(adata_T.X[:1000].max()).is_integer():
        print(f"The input file seems a raw count matrix.")
        print(f"Do normalized!")
        sc.pp.normalize_total(adata_T, target_sum=1e4)
        sc.pp.log1p(adata_T)

    else:
        print(f"The input file seems not a raw count matrix.")
        
        if np.abs(np.expm1(adata_T.X[0]).sum()-10000) > 1:
            print(f"invalid expression matrix, expect all genes and log1p normalized expression to 10000 counts per cell. The prediction result may not be accurate")
        else:
            print(f"All genes and log1p normalized expression to 10000 counts per cell.")

    # 设置全局种子
    np.random.seed(0)
    model = os.path.join(data_path, 'annotation_state_correction_low_polish_nkt.pkl')
    predictions_voting = annotate.annotate(adata_T, model = model, majority_voting = True, min_prop =0.3)
    df = predictions_voting.predicted_labels.rename(columns={'predicted_labels': 'predicted_labels_'+ str(0), 'over_clustering': 'over_clustering_' + str(0), 'majority_voting': 'majority_voting_'+ str(0)})
    adata_T.obs = pd.merge(adata_T.obs, df, how='outer', left_index=True, right_index=True)

    # 类型判断
    type_dict = {}
    for over_clustering in predictions_voting.predicted_labels['over_clustering'].unique():
        type_dict[over_clustering] = predictions_voting.predicted_labels[predictions_voting.predicted_labels['over_clustering'] == over_clustering]['majority_voting'][0]
    global adata_T_UN_D
    adata_T_UN_D = adata_T[adata_T.obs['majority_voting_0'].isin(['Double Negative','Double Positive','MAIT','NKT','gdT']), :]
    adata_T_UN_D.obs['marker_results'] = adata_T_UN_D.obs['majority_voting_0']

    print(f'adata_T_UN_D cell number :',adata_T_UN_D.X.shape[0])
    # DN/DP/UN直出 剩下检测CD4/8 再celltypist预测marker出
    # core
    next_step = []
    for key in type_dict.keys():
        if type_dict[key] in ['Double Negative','Double Positive','MAIT','NKT','gdT']:
            continue
        else:
            next_step.append(key)

    # 分CD4/8
    adata_T_sub = adata_T[adata_T.obs['over_clustering_0'].isin(next_step), :]

    print('分CD4/8')
    CD8_COUNTS = adata_T_sub.obs.total_counts_CD8
    CD4_COUNTS = adata_T_sub.obs.total_counts_CD4
    adata_T_sub.obs['CD4_OR_CD8'] = np.where(CD8_COUNTS > CD4_COUNTS, 'CD8', 'CD4')
    adata_T_sub.obs['CD4_OR_CD8'] = adata_T_sub.obs['CD4_OR_CD8'].astype('category')
    
    global adata_T_sub_CD4
    global adata_T_sub_CD8

    
    # 判断极端情况
    cd4_or_cd8_values = adata_T_sub.obs['CD4_OR_CD8']
    cd4_count = (cd4_or_cd8_values == 'CD4').sum()
    cd8_count = (cd4_or_cd8_values == 'CD8').sum()
    total_cells = len(cd4_or_cd8_values)
    cd4_percentage = cd4_count / total_cells
    cd8_percentage = cd8_count / total_cells
    if cd4_percentage > 0.95:
        adata_T_sub.obs['CD4_OR_CD8'] = 'CD4'
    elif cd8_percentage > 0.95:
        adata_T_sub.obs['CD4_OR_CD8'] = 'CD8'

    adata_T_sub_CD4 = adata_T_sub[adata_T_sub.obs['CD4_OR_CD8'] == 'CD4']
    adata_T_sub_CD8 = adata_T_sub[adata_T_sub.obs['CD4_OR_CD8'] == 'CD8']


#############################################################################################################################################################################################################
    # CD4预测
    def process_CD4(q1):
        global adata_T_sub_CD4
        print(f'CD4预测 :',adata_T_sub_CD4.X.shape[0])
        if adata_T_sub_CD4.X.shape[0] != 0:
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            model = os.path.join(data_path, 'annotation_state_correction_low_cd4_polish.pkl')
            predictions_voting = annotate.annotate(adata_T_sub_CD4, model = model, majority_voting = True, min_prop =0.3)
            df = predictions_voting.predicted_labels.rename(columns={'predicted_labels': 'predicted_labels_'+ 'CD4', 'over_clustering': 'over_clustering_' + 'CD4', 'majority_voting': 'majority_voting_'+ 'CD4'})
            adata_T_sub_CD4.obs = pd.merge(adata_T_sub_CD4.obs, df, how='outer', left_index=True, right_index=True)

            # 对query做rank_genes_groups
            # 计算每个类别中的细胞个数
            cell_counts = adata_T_sub_CD4.obs['over_clustering_CD4'].value_counts()

            # 找出只有一个细胞的类别
            single_cell_groups = cell_counts[cell_counts == 1].index

            # 保留有2个及以上细胞的类别
            adata_T_sub_CD4 = adata_T_sub_CD4[~adata_T_sub_CD4.obs['over_clustering_CD4'].isin(single_cell_groups)]
            print('rank_genes_groups CD4')
            adata_T_sub_CD4.uns['log1p'] = {'base': None}
            sc.tl.rank_genes_groups(adata_T_sub_CD4, 'over_clustering_CD4', method='wilcoxon' , key_added = 'model_CD4',n_genes=1000)
            print('rank_genes_groups CD4 done!')
            # 读取reference的marker
            marker = os.path.join(data_path, 'marker_combine_CD4.txt')
            with open(marker, 'r') as txtfile_high:
                marker_combine_CD4 = json.load(txtfile_high)

            # marker对比
            df_0 = sc.get.rank_genes_groups_df(adata_T_sub_CD4, group=None, key='model_CD4',log2fc_min=0.05,pval_cutoff=0.5)

                # 创建一个空的字典，用于存储每个分组的前number个marker
            markers = {}

                # 遍历所有的分组
            for group in adata_T_sub_CD4.obs['over_clustering_CD4'].unique():
                # 从DataFrame中筛选出该分组的数据
                sub_df = df_0[df_0["group"] == group]
                # 从数据中取出前60个marker的基因名
                top_60 = sub_df["names"].head(60).tolist()
                # 将分组和对应的marker添加到字典中
                markers[group] = top_60

            # 类型判断
            type_dict_CD4 = {}
            for over_clustering in predictions_voting.predicted_labels['over_clustering'].unique():
                type_dict_CD4[over_clustering] = predictions_voting.predicted_labels[predictions_voting.predicted_labels['over_clustering'] == over_clustering]['majority_voting'][0]

            for i in list(single_cell_groups):
                del type_dict_CD4[i]

            # core
            for key in type_dict_CD4.keys():
                gene_list = markers[key]  # 从markers中取出gene列表

                if type_dict_CD4[key] == 'Heterogeneous':  # 比例最大
                    # 和marker_combine的gene列表取交集，计算占比，找到最大的那一个
                    max_ratio = 0
                    max_key = None
                    for combine_key in marker_combine_CD4.keys():
                        temp_list = marker_combine_CD4[combine_key]
                        temp_intersection = list(set(gene_list) & set(temp_list))
                        # 计算交集在temp_list中的占比
                        temp_ratio = len(temp_intersection) / len(temp_list)
                        if temp_ratio > max_ratio:
                            max_ratio = temp_ratio
                            max_key = combine_key

                    # 修改type_dict的key对应的值
                    if max_key is not None:
                        type_dict_CD4[key] = max_key

                else:
                    combine_list = marker_combine_CD4[type_dict_CD4[key]]  # 从marker_combine中取出gene列表

                    # 取交集
                    intersection = list(set(gene_list) & set(combine_list))

                    # 如果交集大于等于marker_combine中取的gene列表中的一半
                    if len(intersection) >= len(combine_list) / 2:
                        continue
                    else:   # 比例最大
                        # 和剩下marker_combine的gene列表取交集，找到最大的那一个
                        max_ratio = 0
                        max_key = None
                        for combine_key in marker_combine_CD4.keys():
                            temp_list = marker_combine_CD4[combine_key]
                            temp_intersection = list(set(gene_list) & set(temp_list))
                            temp_ratio = len(temp_intersection) / len(temp_list)
                            if temp_ratio > max_ratio:
                                max_ratio = temp_ratio
                                max_key = combine_key

                        # 修改type_dict的key对应的值
                        if max_key is not None:
                            type_dict_CD4[key] = max_key
            
            for key in type_dict_CD4.keys():
                if type_dict_CD4[key] in ['CD4 Tn', 'CD4 Tn Quiescence', 'CD4 Tn Adhesion', 'CD4 Tn IFN-Response', 'CD4 Tn Regulating'] and sum(marker in markers[key] for marker in ['CCR7', 'SELL', 'TCF7', 'LEF1']) >2:
                    continue
                elif type_dict_CD4[key] in ['CD4 Tn', 'CD4 Tn Quiescence', 'CD4 Tn Adhesion', 'CD4 Tn IFN-Response', 'CD4 Tn Regulating'] and any(marker in markers[key] for marker in ['KLF2', 'TRADD', 'ICAM2', 'PTGER2', 'GPR183', 'LTB', 'FLT3LG', 'SORL1']):
                    type_dict_CD4[key] = 'CD4 Tcm'

            adata_T_sub_CD4.obs['marker_results'] = adata_T_sub_CD4.obs['over_clustering_CD4'].map(type_dict_CD4)

        else:
            adata_T_sub_CD4 = adata_T_sub_CD4
        q1.put(adata_T_sub_CD4)
##############################################################################################################################################################################################################
    # CD8预测
    def process_CD8(q2):
        global adata_T_sub_CD8    
        print(f'CD8预测 :',adata_T_sub_CD8.X.shape[0])
        if adata_T_sub_CD8.X.shape[0] != 0:
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            model = os.path.join(data_path, 'annotation_state_correction_low_cd8_polish_nkt.pkl')
            predictions_voting = annotate.annotate(adata_T_sub_CD8, model = model, majority_voting = True, min_prop =0.3)
            df = predictions_voting.predicted_labels.rename(columns={'predicted_labels': 'predicted_labels_'+ 'CD8', 'over_clustering': 'over_clustering_' + 'CD8', 'majority_voting': 'majority_voting_'+ 'CD8'})
            adata_T_sub_CD8.obs = pd.merge(adata_T_sub_CD8.obs, df, how='outer', left_index=True, right_index=True)

            # 对query做rank_genes_groups
            # 计算每个类别中的细胞个数
            cell_counts = adata_T_sub_CD8.obs['over_clustering_CD8'].value_counts()

            # 找出只有一个细胞的类别
            single_cell_groups = cell_counts[cell_counts == 1].index

            # 保留有2个及以上细胞的类别
            adata_T_sub_CD8 = adata_T_sub_CD8[~adata_T_sub_CD8.obs['over_clustering_CD8'].isin(single_cell_groups)]
            print('rank_genes_groups CD8')
            adata_T_sub_CD8.uns['log1p'] = {'base': None}
            sc.tl.rank_genes_groups(adata_T_sub_CD8, 'over_clustering_CD8', method='wilcoxon' , key_added = 'model_CD8',n_genes=1000)
            print('rank_genes_groups CD8 done!')
            # 读取reference的marker
            marker = os.path.join(data_path, 'marker_combine_CD8.txt')
            with open(marker, 'r') as txtfile_high:
                marker_combine_CD8 = json.load(txtfile_high)

            # marker对比
            df_0 = sc.get.rank_genes_groups_df(adata_T_sub_CD8, group=None, key='model_CD8',log2fc_min=0.05,pval_cutoff=0.5)

                # 创建一个空的字典，用于存储每个分组的前number个marker
            markers = {}

                # 遍历所有的分组
            for group in adata_T_sub_CD8.obs['over_clustering_CD8'].unique():
                # 从DataFrame中筛选出该分组的数据
                sub_df = df_0[df_0["group"] == group]
                # 从数据中取出前60个marker的基因名
                top_60 = sub_df["names"].head(60).tolist()
                # 将分组和对应的marker添加到字典中
                markers[group] = top_60

            # 类型判断
            type_dict_CD8 = {}
            for over_clustering in predictions_voting.predicted_labels['over_clustering'].unique():
                type_dict_CD8[over_clustering] = predictions_voting.predicted_labels[predictions_voting.predicted_labels['over_clustering'] == over_clustering]['majority_voting'][0]

            for i in list(single_cell_groups):
                del type_dict_CD8[i]

            # core
            for key in type_dict_CD8.keys():
                gene_list = markers[key]  # 从markers中取出gene列表

                if type_dict_CD8[key] == 'Heterogeneous':  # 比例最大
                    # 和marker_combine的gene列表取交集，计算占比，找到最大的那一个
                    max_ratio = 0
                    max_key = None
                    for combine_key in marker_combine_CD8.keys():
                        temp_list = marker_combine_CD8[combine_key]
                        temp_intersection = list(set(gene_list) & set(temp_list))
                        # 计算交集在temp_list中的占比
                        temp_ratio = len(temp_intersection) / len(temp_list)
                        if temp_ratio > max_ratio:
                            max_ratio = temp_ratio
                            max_key = combine_key

                    # 修改type_dict的key对应的值
                    if max_key is not None:
                        type_dict_CD8[key] = max_key

                else:
                    combine_list = marker_combine_CD8[type_dict_CD8[key]]  # 从marker_combine中取出gene列表

                    # 取交集
                    intersection = list(set(gene_list) & set(combine_list))

                    # 如果交集大于等于marker_combine中取的gene列表中的一半
                    if len(intersection) >= len(combine_list) / 2:
                        continue
                    else:   # 比例最大
                        # 和剩下marker_combine的gene列表取交集，找到最大的那一个
                        max_ratio = 0
                        max_key = None
                        for combine_key in marker_combine_CD8.keys():
                            temp_list = marker_combine_CD8[combine_key]
                            temp_intersection = list(set(gene_list) & set(temp_list))
                            temp_ratio = len(temp_intersection) / len(temp_list)
                            if temp_ratio > max_ratio:
                                max_ratio = temp_ratio
                                max_key = combine_key

                        # 修改type_dict的key对应的值
                        if max_key is not None:
                            type_dict_CD8[key] = max_key

            for key in type_dict_CD8.keys():
                if type_dict_CD8[key] in ['CD8 Tn'] and sum(marker in markers[key] for marker in ['GZMA', 'GZMB', 'GZMK', 'GZMH','CREM', 'FAM177A1', 'LDHA', 'OAZ1', 'CMC1', 'CLDND1', 'SARAF', 'FTH1', 'TRAT1', 'MLLT3', 'GGA2', 'CYSTM1', 'DUSP2', 'CST7', 'DKK3', 'ITM2C', 'GPR183', 'TRMO', 'ATP6V0C'])>1:
                    type_dict_CD8[key] = 'CD8 Tcm'
                elif type_dict_CD8[key] in ['CD8 Tcm'] and 'IL7R' not in markers[key]:
                    type_dict_CD8[key] = 'CD8 Tem'
                
            adata_T_sub_CD8.obs['marker_results'] = adata_T_sub_CD8.obs['over_clustering_CD8'].map(type_dict_CD8)
        else:
            adata_T_sub_CD8 = adata_T_sub_CD8
        q2.put(adata_T_sub_CD8)
################################################################################################################################################################## 
    def start_processes():
        q1 = Queue()
        q2 = Queue()
        p1 = Process(target=process_CD4,args=(q1,))
        p2 = Process(target=process_CD8,args=(q2,))
        p1.start()
        p2.start()
        adata_T_sub_CD4 = q1.get()
        adata_T_sub_CD8 = q2.get()
        p1.join()
        p2.join()
        # 返回结果
        return adata_T_sub_CD4, adata_T_sub_CD8
    
    adata_T_sub_CD4, adata_T_sub_CD8 = start_processes()        
    adata = sc.AnnData.concatenate(adata_None_T, adata_T_UN_D, adata_T_sub_CD4, adata_T_sub_CD8, index_unique = None)

    return adata