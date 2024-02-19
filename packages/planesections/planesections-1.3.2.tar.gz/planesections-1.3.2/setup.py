import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="planesections",
    version="1.3.2",
    author="Christian Slotboom",
    author_email="christian.slotboom@gmail.com",
    description="A light-weight FEM beam analyzer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cslotboom/planesections",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    'numpy',
    'matplotlib',
    'PyniteFEA',
    'textalloc>=0.0.6'
    
    ],
    extras_require={
        "opensees": ["openseespy"],
    },
    python_requires='>=3.9',
)