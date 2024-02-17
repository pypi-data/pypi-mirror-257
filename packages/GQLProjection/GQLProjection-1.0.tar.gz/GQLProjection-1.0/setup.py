import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GQLProjection", 
    version="1.0",
    author="J. S. Oishi",
    author_email="jsoishi@gmail.com",
    description="A tool to do GQL projection in Dedalus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jsoishi/GQLProjection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.10',
    install_requires=['numpy', 'dedalus>=3.0']
)
