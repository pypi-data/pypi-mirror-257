import setuptools

def get_requirements():
    with open("requirements.txt", "rt", encoding="utf-8") as fh:
        return [line.strip() for line in fh.readlines()]

setuptools.setup(
    name='TCATT',
    version='0.1',
    packages=setuptools.find_packages(),
    install_requires=get_requirements(),
    include_package_data=True,
    python_requires='>=3.6'

)
