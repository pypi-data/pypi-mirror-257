import os
import pathlib
import json
import pickle
import requests
import numpy as np
import pandas as pd
from typing import Optional, Union
from scipy.special import expit
from sklearn import __version__ as skv
from . import logger

models_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def _requests_get(url: str, timeout = 30):
    """
    For internal use. Make a request and raise errors (including timeout error) if it fails.
    """
    try:
        r = requests.get(url, timeout = timeout)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(
                f"🛑 Cannot fetch '{url}', the error is: {e}")
    return r

class Model():
    """
    Class that wraps the logistic Classifier and the StandardScaler.

    Parameters
    ----------
    clf
        A logistic Classifier incorporated in the loaded model.
    scaler
        A StandardScaler incorporated in the loaded model.
    description
        Description of the model as a dictionary.

    Attributes
    ----------
    classifier
        The logistic Classifier incorporated in the loaded model.
    scaler
        The StandardScaler incorporated in the loaded model.
    description
        Description of the loaded model.
    """
    def __init__(self, clf, scaler, description):
        self.classifier = clf
        self.scaler = scaler
        self.description = description

    @staticmethod
    def load(model: Optional[str] = None):
        """
        Load the desired model.

        Parameters
        ----------
        model
            Model name specifying the model you want to load. Default to `'Immune_All_Low.pkl'` if not provided.
            To see all available models and their descriptions, use :func:`~celltypist.models.models_description`.

        Returns
        ----------
        :class:`~celltypist.models.Model`
            A :class:`~celltypist.models.Model` object.
        """
        # if not model:
        #     model = get_default_model()
        if model in get_all_models():
            model = get_model_path(model)
        if not os.path.isfile(model):
            raise FileNotFoundError(
                    f"🛑 No such file: {model}")
        with open(model, "rb") as fh:
            try:
                pkl_obj = pickle.load(fh)
                return Model(pkl_obj['Model'], pkl_obj['Scaler_'], pkl_obj['description'])
            except Exception as exception:
                raise Exception(
                        f"🛑 Invalid model: {model}. {exception}")

    @property
    def cell_types(self) -> np.ndarray:
        """Get cell types included in the model."""
        return self.classifier.classes_

    @property
    def features(self) -> np.ndarray:
        """Get genes included in the model."""
        return self.classifier.features

    def __repr__(self):
        base = f"CellTypist model with {len(self.cell_types)} cell types and {len(self.features)} features"
        for x in ['date', 'details', 'source', 'version']:
            if self.description[x] != '':
                base += f"\n    {x}: {self.description[x]}"
        if len(self.cell_types) == 2:
            base += f"\n    cell types: {self.cell_types[0]}, {self.cell_types[1]}\n    features: {self.features[0]}, {self.features[1]}, ..., {self.features[-1]}"
        elif len(self.cell_types) == 3:
            base += f"\n    cell types: {self.cell_types[0]}, {self.cell_types[1]}, {self.cell_types[2]}\n    features: {self.features[0]}, {self.features[1]}, ..., {self.features[-1]}"
        else:
            base += f"\n    cell types: {self.cell_types[0]}, {self.cell_types[1]}, ..., {self.cell_types[-1]}\n    features: {self.features[0]}, {self.features[1]}, ..., {self.features[-1]}"
        return base

    def predict_labels_and_prob(self, indata, mode: str = 'best match', p_thres: float = 0.5) -> tuple:
        """
        Get the decision matrix, probability matrix, and predicted cell types for the input data.

        Parameters
        ----------
        indata
            The input array-like object used as a query.
        mode
            The way cell prediction is performed.
            For each query cell, the default (`'best match'`) is to choose the cell type with the largest score/probability as the final prediction.
            Setting to `'prob match'` will enable a multi-label classification, which assigns 0 (i.e., unassigned), 1, or >=2 cell type labels to each query cell.
            (Default: `'best match'`)
        p_thres
            Probability threshold for the multi-label classification. Ignored if `mode` is `'best match'`.
            (Default: 0.5)

        Returns
        ----------
        tuple
            A tuple of decision score matrix, raw probability matrix, and predicted cell type labels.
        """
        if skv.split('.')[0] != '0' and isinstance(indata, np.matrix):
            scores = self.classifier.decision_function(np.asarray(indata))
        else:
            scores = self.classifier.decision_function(indata)
        if len(self.cell_types) == 2:
            scores = np.column_stack([-scores, scores])
        probs = expit(scores)
        if mode == 'best match':
            return scores, probs, self.classifier.classes_[scores.argmax(axis=1)]
        elif mode == 'prob match':
            flags = probs > p_thres
            labs = np.array(['|'.join(self.classifier.classes_[np.where(x)[0]]) for x in flags])
            labs[labs == ''] = 'Unassigned'
            return scores, probs, labs
        else:
            raise ValueError(
                    f"🛑 Unrecognized `mode` value, should be one of `'best match'` or `'prob match'`")

    def write(self, file: str) -> None:
        """Write out the model."""
        obj = dict(Model = self.classifier, Scaler_ = self.scaler, description = self.description)
        file = os.path.splitext(file)[0] + '.pkl'
        with open(file, 'wb') as output:
            pickle.dump(obj, output)

    def extract_top_markers(self, cell_type: str, top_n: int = 10, only_positive: bool = True) -> np.ndarray:
        """
        Extract the top driving genes for a given cell type.

        Parameters
        ----------
        cell_type
            The cell type to extract markers for.
        top_n
            Number of markers to extract for a given cell type.
            (Default: 10)
        only_positive
            Whether to extract positive markers only. Set to `False` to include negative markers as well.
            (Default: `True`)

        Returns
        ----------
        :class:`~numpy.ndarray`
            A list of marker genes for the query cell type.
        """
        if cell_type not in self.cell_types:
            raise ValueError(
                    f"🛑 '{cell_type}' is not found. Please provide a valid cell type name")
        if len(self.cell_types) == 2:
            coef_vector = self.classifier.coef_[0] if cell_type == self.cell_types[1] else -self.classifier.coef_[0]
        else:
            coef_vector = self.classifier.coef_[self.cell_types == cell_type][0]
        if not only_positive:
            coef_vector = np.abs(coef_vector)
        return self.features[np.argsort(-coef_vector)][:top_n]

def get_model_path(file: str) -> str:
    """
    Get the full path to a file in the `models` folder.

    Parameters
    ----------
    file
        File name as a string.
        To see all available models and their descriptions, use :func:`~celltypist.models.models_description`.

    Returns
    ----------
    str
        A string of the full path to the desired file.
    """
    return os.path.join(models_path, f"{file}")


# def get_default_model() -> str:
#     """
#     Get the default model name.

#     Returns
#     ----------
#     str
#         A string showing the default model name (should be `'Immune_All_Low.pkl'`).
#     """
#     models_json = get_models_index()
#     default_model = [m["filename"] for m in models_json["models"] if ("default" in m and m["default"])]
#     if not default_model:
#         first_model = models_json["models"][0]["filename"]
#         logger.warn(f"👀 No model marked as 'default', using {first_model}")
#         return first_model
#     if len(default_model) > 1:
#         logger.warn(f"👀 More than one model marked as 'default', using {default_model[0]}")
#     return default_model[0]


def get_all_models() -> list:
    """
    Get a list of all the available models.

    Returns
    ----------
    list
        A list of available models.
    """
    # download_if_required()
    available_models = []
    for model_filename in os.listdir(models_path):
        if model_filename.endswith(".pkl"):
            model_name = os.path.basename(model_filename)
            available_models.append(model_name)
    return available_models


# def download_if_required() -> None:
#     """Download models if there are none present in the `models` directory."""
#     if len([m for m in os.listdir(models_path) if m.endswith(".pkl")]) == 0:
#         logger.info(f"🔎 No available models. Downloading...")
#         download_models()


# def get_models_index(force_update: bool=False) -> dict:
#     """
#     Get the model json object containing the model list.

#     Parameters
#     ----------
#     force_update
#         If set to `True`, will download the latest model json file from the remote.
#         (Default: `False`)

#     Returns
#     ----------
#     dict
#         A dict object converted from the model json file.
#     """
#     models_json_path = get_model_path("models.json")
#     if not os.path.exists(models_json_path) or force_update:
#         download_model_index()
#     with open(models_json_path) as f:
#         return json.load(f)


# def download_model_index(only_model: bool = True) -> None:
#     """
#     Download the `models.json` file from the remote server.

#     Parameters
#     ----------
#     only_model
#         If set to `False`, will also download the models in addition to the json file.
#         (Default: `True`)
#     """
#     url = 'https://celltypist.cog.sanger.ac.uk/models/models.json'
#     logger.info(f"📜 Retrieving model list from server {url}")
#     response = _requests_get(url)
#     with open(get_model_path("models.json"), "wb") as f:
#         f.write(response.content)
#     model_count = len(response.json()["models"])
#     logger.info(f"📚 Total models in list: {model_count}")
#     if not only_model:
#         download_models()

# def download_models(force_update: bool=False, model: Optional[Union[str, list, tuple]] = None) -> None:
#     """
#     Download all the available or selected models.

#     Parameters
#     ----------
#     force_update
#         Whether to fetch a latest JSON index for downloading all available or selected models.
#         Set to `True` if you want to parallel the latest celltypist model releases.
#         (Default: `False`)
#     model
#         Specific model(s) to download. By default, all available models are downloaded.
#         Set to a specific model name or a list of model names to only download a subset of models.
#         For example, set to `["ModelA.pkl", "ModelB.pkl"]` to only download ModelA and ModelB.
#         To check all available models, use :func:`~celltypist.models.models_description`.
#     """
#     models_json = get_models_index(force_update)
#     logger.info(f"📂 Storing models in {models_path}")
#     if model is not None:
#         model_list = {model} if isinstance(model, str) else set(model)
#         models_json["models"] = [m for m in models_json["models"] if m["filename"] in model_list]
#         provided_no = len(model_list)
#         filtered_no = len(models_json["models"])
#         if filtered_no == 0:
#             raise ValueError(
#                     f"🛑 No models match the celltypist model repertoire. Please provide valid model names")
#         elif provided_no == filtered_no:
#             logger.info(f"💾 Total models to download: {provided_no}")
#         else:
#             ignored_models = model_list.difference({m["filename"] for m in models_json["models"]})
#             logger.warn(f"💾 Total models to download: {filtered_no}. {len(ignored_models)} not available: {ignored_models}")
#     model_count = len(models_json["models"])
#     for idx,model in enumerate(models_json["models"]):
#         model_path = get_model_path(model["filename"])
#         if os.path.exists(model_path) and not force_update:
#             logger.info(f"⏩ Skipping [{idx+1}/{model_count}]: {model['filename']} (file exists)")
#             continue
#         logger.info(f"💾 Downloading model [{idx+1}/{model_count}]: {model['filename']}")
#         try:
#             response = _requests_get(model["url"])
#             with open(model_path, "wb") as f:
#                 f.write(response.content)
#         except Exception as exception:
#             logger.error(f"🛑 {model['filename']} failed {exception}")


# def models_description(on_the_fly: bool=False) -> pd.DataFrame:
    # """
    # Get the descriptions of all available models.

    # Parameters
    # ----------
    # on_the_fly
    #     Whether to fetch the model information from downloaded model files.
    #     If set to `True`, will fetch the information by loading downloaded models.
    #     Default to fetching the information for all available models from the JSON file.
    #     (Default: `False`)

    # Returns
    # ----------
    # :class:`~pandas.DataFrame`
    #     A :class:`~pandas.DataFrame` object with model descriptions.
    # """
    # logger.info(f"👉 Detailed model information can be found at `https://www.celltypist.org/models`")
    # if on_the_fly:
    #     filenames = get_all_models()
    #     descriptions = [Model.load(filename).description['details'] for filename in filenames]
    # else:
    #     models_json = get_models_index()
    #     models = models_json["models"]
    #     filenames = [model['filename'] for model in models]
    #     descriptions = [model['details'] for model in models]
    # return pd.DataFrame({'model': filenames, 'description': descriptions})
