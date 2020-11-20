import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tzager", 
    version="0.0.1.8.6",
    author="tzager",
    author_email = "nikos@intoolab.com,a.ntokos@intoolab.com",
    description="A demo example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tzagerAI/tzager",
    project_urls = {"Code": "https://github.com/tzagerAI/tzager"},
    packages=setuptools.find_packages(),
    install_requires=["requests", "pdfminer", "pandas", "networkx"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.6',
)