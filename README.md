# Scan2Pdf

This simple Python script converts scanned image files in a directory. It is a workaround for scanners which do not 
support duplex scan. Therefore, the first half of images are assumed as all frontpages. The second half of the images are
are assumed as all backpages. The backpages are in reverse order.

Suppose, you have the following files scanned:
```
CCF28092024_00000.png (front page of first page)
CCF28092024_00001.png (front page of second page)
CCF28092024_00002.png (back page of first page)
CCF28092024_00003.png (back page of second page)
```

The script will convert the images to PDF in the following order:
```
CCF28092024_00000.png
CCF28092024_00003.png
CCF28092024_00001.png
CCF28092024_00002.png
```

Note: It was only tested with files by a Brother scanner having the format "CCF28092024_00000.png" etc.

## How to run

### Install

In order to make this script runnable, follow the installation instructions which has to be executed only once.

#### Venv

Import Virtual environment (Venv) in Windows to this project folder:

- Open cmd.exe
  ```shell
  cd C:\PATH_TO_THIS_PYTHON_PROJECT
  @REM Install virtualenv
  pip3 install virtualenv 
  @REM Create a virtual environment with subdirectory 'venv'
  virtualenv venv
  @REM Activate venv
  venv\Scripts\activate.bat
  pip3 install -r src\main\resources\venv-requirements.txt --no-deps
  ```
  
#### Windows Batch File

Copy 'src/main/batch/_scan2pdf.bat' to the Scanner folder and adapt the SCAN2PDF_FOLDER variable.

### Run

Open the Windows Explorer and double-click '_scan2pdf.bat'.

### Usage

```
usage: scan2pdf.py [-h] [--inputPath INPUT_PATH] [--imagePrefix IMAGE_PREFIX]
                   [--imageExt IMAGE_EXT] [--noFakeDuplexScan]

options:
  -h, --help            show this help message and exit
  --inputPath INPUT_PATH
                        Path to the scanned image files.
  --imagePrefix IMAGE_PREFIX
                        Prefix of scanned image files. Default: CCF
  --imageExt IMAGE_EXT  Extension of scanned image files. Default: .jpg
  --noFakeDuplexScan    If set, it is assumed, that only front pages were
                        scanned. If not set, the script assumes a fake duplex
                        scan. Assumption: All front pages were scanned first,
                        then all backpages were scanned (in reverse order).
```

## Development details

Venv dependency list was generated by:

- Open cmd.exe
  ```shell
  cd C:\PATH_TO_THIS_PYTHON_PROJECT
  venv\Scripts\activate.bat
  pip3 freeze list > src\main\resources\venv-requirements.txt
  ```
