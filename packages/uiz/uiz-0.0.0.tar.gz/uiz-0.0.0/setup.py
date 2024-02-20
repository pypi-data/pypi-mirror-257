from setuptools import setup, find_packages

setup(
    name='uiz',
    version='0.0.0',  # Use semantic versioning (major.minor.patch)
    description='uiz is a simple user interface library',
    author='PyModuleDev',
    url='https://github.com/zPointless/uiz',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        # Add any other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
