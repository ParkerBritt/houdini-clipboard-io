<h1 align="center">Houdini Clipboard IO</h1>
<p align="center"}>
  <img src="https://img.shields.io/badge/Houdini-FF4713?style=for-the-badge&logo=houdini&logoColor=white">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
</p>

Houdini Clipboard IO is a python module, providing tools for creating and modifying nodes in Houdini's clipboard from external programs.
> Early WIP  
> Because of Houdini's DRM it is not possible to use .cpio files generated with a non commercial version of Houdini.

## Installation
### Requirements
- Python >= 3.6
- Sidefx Houdini

First **clone** and **cd** into the repository  
```bash
git clone https://github.com/ParkerBritt/houdini-clipboard-io
cd houdini-clipboard-io
```
### (Option 1) Interactive installation
Run the **install** command
```bash
pip install -e .
```
### (Option 2) Regular installation
**Build** the tar.gz package
```bash
pip install build
python -m build --sdist
```
**Install** the built package, make sure to type the relevant package version
```bash
pip install dist/hclipboard_io-0.1.0.tar.gz
```

## Usage
**Import** the package
```python
import hclipboard_io
```
placeholder
