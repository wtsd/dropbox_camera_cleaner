# Image File Organizer
## Overview
This Python script organizes image files in a specified directory. It moves .png files to a designated folder and sorts .jpg files into folders based on their names.

## Requirements
Python 3.x
PyYAML (for YAML configuration file support)

## Installation
1. Clone this repository or download the script.

```
git clone https://github.com/your-repo/image-file-organizer.git
```

1. Install the required packages.
```
pip install -r requirements.txt
```

## Usage
### Command-Line Arguments
Run the script with optional command-line arguments for specifying the target directory and the folder for .png files.

```
python organize_files_argparse.py --dir [YourTargetFolder] --ext [YourExtFolderName]
```

* [YourTargetFolder]: The directory containing the .png and .jpg files you wish to organize.
* [YourExtFolderName]: The name of the folder where .png files will be moved.

### Configuration File
Alternatively, you can specify the parameters in a YAML configuration file (config.yml). Here's a sample structure:

```
dir: '/path/to/target/folder'
ext: 'name_of_ext_folder'
```

Run the script using the configuration file:

```
python organize_files_argparse.py --config config.yml
```

### Combined Usage
You can also use both command-line arguments and a configuration file. Command-line arguments will override the settings in the configuration file.

