from setuptools import *

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='TemplateMatchResearch',
    version='1.0.0',
    author="Emmanuel Mireku",
    author_email="emmanuelmireku15@gmail.com",
    description="A lightweight package to detect chrome, firefox, edge, and opera browser on a windows user's computer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emire1/TemplateMactchResearch",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6', install_requires=['opencv-python', 'pyautogui', 'numpy', 'imutils']
)
