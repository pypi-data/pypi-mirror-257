from setuptools import setup, find_packages

VERSION = '0.0.3'

DESCRIPTION = 'Vanilla Regression Transformer'
LONG_DESCRIPTION = 'Vanilla Regression Transformer of general purpose'

setup(
       # the name must match the folder name 'verysimplemodule'
        name="Transformer_lafae", 
        version=VERSION,
        author="Luan Lopes",
        author_email="luansantos@poli.ufrj.br",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'transformer','Machine Learning'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)