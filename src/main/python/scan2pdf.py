# 3rd party modules
import logging
from PIL import Image  # install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation
from os import listdir
import os
import sys
from pathlib import Path
import argparse

# Project modules
import commons

BROTHER_SCAN_SUBDIRECTORY = os.path.join("Pictures", "ControlCenter3", "Scan")
TARGETFILE_EXT = ".pdf"

DEFAULT_BROTHER_IMAGE_PREFIX = "CCF"
DEFAULT_BROTHER_IMAGE_EXT = ".jpg"


class Scan2Pdf:
    def __init__(
            self
    ):
        LOG_FILE_PATH = "../../../logs/"
        # locale.setlocale(locale.LC_ALL, "german")
        commons.initialize(LOG_FILE_PATH)

        logging.getLogger('matplotlib').setLevel(logging.WARNING)
        logging.getLogger('matplotlib.pyplot').setLevel(logging.WARNING)
        logging.getLogger("PIL.PngImagePlugin").setLevel(logging.WARNING)

        self.args = None
        self.input_path = None

    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--inputPath', dest='input_path', type=str, help='Path to the scanned image files.')
        parser.add_argument('--imagePrefix', dest='image_prefix', type=str, default=DEFAULT_BROTHER_IMAGE_PREFIX, help='Prefix of scanned image files. Default: ' + DEFAULT_BROTHER_IMAGE_PREFIX)
        parser.add_argument('--imageExt', dest='image_ext', type=str,
                            default=DEFAULT_BROTHER_IMAGE_EXT, help='Extension of scanned image files. Default: ' + DEFAULT_BROTHER_IMAGE_EXT)
        parser.add_argument('--duplexScan', dest='is_duplex_scan',
                            action="store_true",
                            help='If set, the script assumes a fake duplex scan. I.e. all front pages were scanned '
                                 'first, then all back pages were scanned (in reverse order).'
                                 'If not set, it is assumed, that only front pages were scanned. '
                            )
        self.args = parser.parse_args()

        if self.args.input_path == None:
            # Ubuntu
            home = os.getenv("HOME")
            if home is None:
                # Windows
                home = Path.home()
            self.input_path = os.path.join(home, BROTHER_SCAN_SUBDIRECTORY)
        else:
            self.input_path = os.path.abspath(self.args.input_path)

    def start(self):
        self.parseArgs()

        image_file_names = [f for f in listdir(self.input_path) if (os.path.isfile(os.path.join(self.input_path, f)) and f.startswith(self.args.image_prefix) and f.endswith(self.args.image_ext))]

        image_array_length = len(image_file_names)

        if image_array_length == 0:
            print("Could not find any images files with prefix '" + self.args.image_prefix + "' and extension '" + self.args.image_ext + "' in the directory '" + self.input_path + "'. Script aborted.", file=sys.stderr)
            exit(1)

        if self.args.is_duplex_scan:
            print("Assembling duplex scanned files ...")

            if image_array_length % 2 != 0:
                print("There must be an even number of images files in the directory '" + self.input_path + "' if this is a duplex scan. Found only " + str(image_array_length) + ". Script aborted.", file=sys.stderr)
                exit(1)
        else:
            print("Assembling scanned files ... ...")

        targetfile_name = "_" + image_file_names[0].split("_", 1)[0]

        if targetfile_name is None:
            print("Could not determine a target PDF filename. There must be a '_' in the png file names. Script aborted.", file=sys.stderr)
            exit(1)

        targetfilepath = os.path.join(self.input_path, targetfile_name) + TARGETFILE_EXT
        targetfile = Path(targetfilepath)
        index = 0
        while targetfile.exists():
            index += 1
            targetfilepath = os.path.join(self.input_path, targetfile_name) + "_v" + str(index) + TARGETFILE_EXT
            targetfile = Path(targetfilepath)
            if index > 100:
                break

        if targetfile.exists():
            print(
                "The target PDF file '" + targetfilepath + "' already exists. Script aborted.",
                file=sys.stderr)
            exit(1)

        print("Starting converting to '" + targetfilepath + "'. This can take a while ...")

        if self.args.is_duplex_scan:
            half_length = int(image_array_length / 2)
            scannedfiles = [0 for x in range(image_array_length)]
            for i in range(0, half_length):
                scannedfiles[2 * i] = image_file_names[i]
                scannedfiles[2 * i + 1] = image_file_names[image_array_length - i - 1]
        else:
            scannedfiles = image_file_names

        images = [
            Image.open(os.path.join(self.input_path, f))
            for f in scannedfiles
        ]

        images[0].save(
            targetfilepath, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )

        print("")
        print("Stored PDF to '" + targetfilepath + "'")

if __name__ == '__main__':
    print("This script will convert all scanned images in a directory to a PDF file.")
    print("")

    scan2Pdf = Scan2Pdf()
    scan2Pdf.start()