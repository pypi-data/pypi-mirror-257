import setuptools
from pathlib import Path


def get_install_requirements():
    """
    Extract packages from requirements.txt file to list

    Returns:
        list: list of packages
    """
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets


setuptools.setup(name='opsys-cart-controller',
                 version='0.0.3',
                 description='python package for cart moving on rail control',
                 url='https://bitbucket.org/opsys_tech/opsys-cart-controller/src/master/',
                 download_url='https://bitbucket.org/opsys_tech/opsys-cart-controller/src/master/',
                 author='dmitry.borovensky',
                 install_requires=get_install_requirements(),
                 author_email='dmitry.borovensky@opsys-tech.com',
                 packages=setuptools.find_packages(),
                 zip_safe=False)