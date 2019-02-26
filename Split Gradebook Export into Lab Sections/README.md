# Split Gradebook Export into Lab Sections

## Introduction

The purpose of this script is to simplify the process of managing lab courses in Canvas that contain a large number of lab sections each graded by a different Teaching Assistant (TA). It generates individual CSV Gradebook files for each lab section that can then be distributed to the TAs. Each file only contains student data that is relevant to the section the TA is grading, and the unnecessary data columns (i.e. the read-only columns) are omitted.

## Requirements

* Python 3

* Canvas API Token ([Learn How to Generate a Token](https://community.canvaslms.com/docs/DOC-10806-4214724194))

* Course ID (e.g. ht<span>tps://</span>canvas.ubc.ca/courses/**10754**)

* Exported Canvas Gradebook CSV File

You will need to install the additional libraries using the command `pip install -r requirements.txt`

## Running the Script

1. Download or clone the repository onto your local machine.

1. Add your Canvas API Token to the `canvas.cfg` file.

1. Place your exported Gradebook CSV file in the same directory as this script.

1. Run `split_gradebook_into_sections.py` and it will prompt you for your course ID and the filename of the Gradebook CSV file. Note that this is a command-line tool. There is no graphical user interface. So, you can run it in a terminal window or a Python IDE.

1. When the script has finished running a folder named after your course will be generated in the same directory as the script. The individual CSV files for each lab section are contained within this folder and are named according to section.

## Additional Information

* The script is designed to organize data based on lab section, therefore your course must have the Lab column in its Gradebook.

* For lab courses containing sections from two or more SIS-linked courses, lab sections with the same extension will be grouped together (e.g. if a lab course contains sections CHEM 111 L01 and CHEM 121 L01, students from both L01 sections will be contained in the same output file).

## Authors

* Levi Magnus - levi.magnus@ubc.ca
