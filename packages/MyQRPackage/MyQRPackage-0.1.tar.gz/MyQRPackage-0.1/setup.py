from setuptools import setup, find_packages

setup(
    name='MyQRPackage',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy', 
    ],
    author='Renan Maciel',
    author_email='renan.maciel@physics.uu.se',
    description='A package for QR decomposition using Householder reflections.',
    url='https://github.com/RenanM05/AdvancedPython2022/tree/main/FinalProject/MyQRPackage', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
