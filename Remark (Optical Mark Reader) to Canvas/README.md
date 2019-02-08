# Remark (Optical Mark Reader) to Canvas

## Introduction

The purpose of this script is to facilitate the process of formatting the grades output produced by the Remark OMR software into a file that can be imported into the Canvas Gradebook. 

## Requirements

* Python 3

* Canvas API Token ([Learn How to Generate a Token](https://community.canvaslms.com/docs/DOC-10806-4214724194))

* Course ID (e.g. ht<span>tps://</span>canvas.ubc.ca/courses/**10754**)

* Remark OMR output file

You will need to install the additional libraries using the command **pip install -r requirements.txt**

## Running the Script

1. Download or clone the repository onto your local machine.

1. Add your Canvas API Token to the canvas.cfg file.

1. Place the Remark OMR output file in the same directory as this script. Open the file and ensure that:

   * The file is in CSV format.
   
   * At least the **Student ID** and **Total Score** columns are present. **First Name**, **Last Name**, and **Percent Score** columns are optional, but they can be included as well.

   * The column names have not been changed.

   * Any extra columns like **T-Score** have been removed.

1. Run omr\_to\_canvas.py and it will prompt you for your course ID and the filename of the Remark OMR CSV file. Note that this is a command-line tool, so there is no graphic user interface. You can run the program in a terminal window or a Python IDE.

1. When the script has finished running a file (Import_into_Canvas.csv) will be generated in the same directory as the script. This file can be imported into the Canvas Gradebook. If any students in the input file were not found in your course, an ERROR_LOG text file will also be generated. You can enter the grades for these students manually.

## Additional Information

* IMPORTANT: Rename or move the output files before running the script again, otherwise you will overwrite the content in the file.

## Authors

* Levi Magnus - levi.magnus@ubc.ca
