# DxfNumberedPlates

DxfNumberedPlates is a Python module designed to automate the creation of numbered DXF plates with tags. It simplifies the process of adding sequential labels to DXF files, making it useful for CNC machining, metalworking, and other engineering applications.

## Features
- Automatically generate numbered tags in DXF format
- Supports customizable text and positioning
- Simple and efficient workflow for batch processing

## Installation
Ensure you have Python installed, then install the required dependencies:
```bash
pip install ezdxf
```

## Usage
To generate a single numbered tag, use the following command:
```python
from DxfNumberedPlates import DxfTag

DxfTag.generate_single_tag(6)
```
This will create a DXF file with a single tag containing the number 6.

To generate a sequence of numbered tags from 0 to 25, with a height of 250, holes enabled, a hole radius of 10, and a prefix "Tag_", use:
```python
from DxfNumberedPlates import DxfTag 

DxfTag.generate_tag_sequence(0, 25, height=250, holes=True, radius=10, prefix='Tag_')
```
This will create a series of DXF files with numbered tags from 0 to 25.


## License
This project is licensed under the MIT License.

## Contributions
Pull requests are welcome! If you find issues or have suggestions, please open an issue in the repository.

## Author
Federico Sidraschi https://www.linkedin.com/in/federico-sidraschi-059a961b9/

