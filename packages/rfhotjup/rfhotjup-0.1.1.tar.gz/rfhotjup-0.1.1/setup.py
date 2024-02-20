import setuptools

setuptools.setup(
    name='rfhotjup',
    version='0.1.1',
    description='Library that gives you predicted radio fluxes of Hot Jupiters',
    author='Cristina Cordun, ASTRON',
    packages=setuptools.find_packages(),
    package_data={'rfhotjup': ['database/*']}
)