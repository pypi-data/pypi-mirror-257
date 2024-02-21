import setuptools

# Each Python project should have pyproject.toml or setup.py (if both exist, we use the setup.py)
# TODO: Please create pyproject.toml instead of setup.py (delete the setup.py)
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release) as we have moved away from needing to generate a setup.py file to enable editable installs - We might able to delete this file in the near future

# TODO: Change the PACKAGE_NAME to the name of the package - Either xxx-local or xxx-remote (without the -python-package suffix)
PACKAGE_NAME = "star-local"
# Since all PACAKGE_NAMEs are with an underscore, we don't need this. Why do we need it?
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    # TODO: Please update the name and delete this line i.e. XXX-local or XXX-remote (without the -python-package suffix). Only lowercase, no underlines.
    name=PACKAGE_NAME,
    version='0.0.15', # https://pypi.org/project/star-local
    # update only the minor version each time 

    author="Circles",
    author_email="info@circlez.ai",
    # TODO: Please update the description and delete this line
    description="PyPI Package for Circles <short-project-name-with-dash> Python",
    long_description="PyPI Package for Circles <short-project-name-with-dash> Python",
    long_description_content_type='text/markdown',
    url="https://github.com/circles-zone/star-local-python-package",
    # packages=setuptools.find_packages(),
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TODO: Update which packages to include with this package
    install_requires=[
        'PyMySQL>=1.0.2',
        'pytest>=7.4.3',
        'mysql-connector>=2.2.9',
        'logzio-python-handler>= 4.1.0',
        'user-context-remote>=0.0.17',
        'python-sdk-local>=0.0.27'
    ],
)
