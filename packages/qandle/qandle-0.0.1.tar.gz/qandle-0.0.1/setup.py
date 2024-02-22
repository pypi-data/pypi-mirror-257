from setuptools import setup, find_packages

setup(
    name="qandle",
    version="0.0.1",
    packages=find_packages(),
    author="Gerhard Stenzel",
    author_email="gerhard.stenzel@ifi.lmu.de",
    description="short description",
    long_description=open("README.md").read(),
    license="MIT",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qandle",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: GPU :: NVIDIA CUDA",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=1.10",
        "qW_Map>=0.1.2",
        "networkx>=3.2",
        "einops>=0.7",
    ]
)
