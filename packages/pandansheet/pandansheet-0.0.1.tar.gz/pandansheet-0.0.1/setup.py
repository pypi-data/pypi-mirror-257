import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandansheet",  # Replace with your own package name
    version="0.0.1",
    author="J",
    author_email="jyoungjin0106@gmail.com",
    description="Pandas와 Google sheet를 연동하는 모듈.(A module to integrate pandas and Google Sheets)", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/janyoungjin",  
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.0.0',
        'openpyxl>=3.0.0',
        'requests>=2.0.0',
        'numpy>=1.19.0',
    ],
)
