# -*- coding: utf-8 -*-

#make sure you pip install the necessary libraries before running the script
import csv
import pandas
import re   
import api_calls as api
import error_log_generator as elg

def formatCSV():
    
    #get course ID 
    courseID = input("\nEnter Course ID: ").strip() 
    
    try:
        #api calls to gather course and student information
        courseStudents = api.getCourseStudents(courseID)
        courseDetails = api.getCourseDetails(courseID)
        courseName = courseDetails.get('name')
        
        decision = input("\nFound course \"" + courseName + "\". Hit Enter if this is the correct course or type 'change' to select a different course: ").strip()

        while decision.lower() == "change":
            
            courseID = input("\nEnter Course ID: ").strip() 
            
            courseStudents = api.getCourseStudents(courseID)
            courseDetails = api.getCourseDetails(courseID)
            courseName = courseDetails.get('name')
            
            decision = input("\nFound course " + courseName + ". Hit Enter if this is the correct course or type 'change' to select a different course: ").strip()
        
        #lists for storing student information
        studentNumbers = []
        studentNames = []
        studentIDs = []
        
        #store necessary data for each student in the course
        for student in courseStudents:
            studentNumbers.append(student.get('sis_user_id')) 
            studentNames.append(student.get('name'))
            studentIDs.append(student.get('id'))
        
        #read the OMR CSV file
        while True:
            title = input("\nEnsure the OMR CSV file is in the same location as this script. Enter the name of the file (including the extension .csv) and then press Enter: ")
            try:
                df = pandas.read_csv(title)
                break
            except FileNotFoundError:
                decision = input("\nFile not found. Make sure you have placed the OMR CSV file in the same location as this script and that you typed the filename correctly (including the extension .csv). Hit Enter to try again or type 'quit' to exit: ")
                if decision.lower() == "quit":
                    return
                
        #handles any blank cells
        df.fillna("N/A", inplace=True)
        
        assignmentTitle = input("\nType in the desired name for this assessment: ")
        pointsPossible = input("Type in the points total for this assessment: ")
        
        #get the data columns from the OMR CSV file and perform some data cleansing/validation
        studentID_column = df['Student ID']
        for number in range(0, len(studentID_column.values)):
            if isinstance(studentID_column.values[number], str):
                studentID_column.values[number] = re.sub("[^0-9]", "", str(studentID_column.values[number]))
            else:
                studentID_column.values[number] = re.sub("[^0-9]", "", str(int(studentID_column.values[number])))
            if studentID_column.values[number] == "":
                studentID_column.values[number] = 0
        if 'First Name' in df.columns and 'Last Name' in df.columns:
            firstName_column = df['First Name']
            lastName_column = df['Last Name']
        if 'Percent Score' in df.columns:
            percent_column = df['Percent Score']
        scores_column = df['Total Score']
        
        #lists that will contain the column data for the output CSV file
        outputIDs = []
        outputNames = ["Student", "     Points Possible"]
        outputNumbers = ["SIS User ID", ""]
        outputSections = ["Section", ""]
        outputPercent = ["" + assignmentTitle + " (Percent)", 100]
        outputScores = [assignmentTitle, pointsPossible]
        
        #lists that will contain the data for the error log
        errorNum = []
        errorFName = []
        errorLName = []
        errorScore = []
        errorPercent = []
        
        #match student numbers from the OMR file to student numbers from the course and build output accordingly
        for student in range(0, len(studentID_column.values)):
            for number in range(0, len(studentNumbers)):
                if str(int(studentID_column.values[student])) == str(studentNumbers[number]):
                    outputIDs.append(studentIDs[number])
                    outputNames.append(studentNames[number])
                    outputNumbers.append(studentNumbers[number])
                    outputSections.append(courseName)
                    outputScores.append(scores_column[student])
                    if 'Percent Score' in df.columns:
                        outputPercent.append(percent_column[student])
        
        #build the error log file if a student from the OMR file does not match a student in the course
        for student in range(0, len(studentID_column.values)):
            if str(int(studentID_column.values[student])) not in outputNumbers:
                errorNum.append(studentID_column.values[student])
                if 'First Name' in df.columns and 'Last Name' in df.columns:
                    errorFName.append(firstName_column.values[student])
                    errorLName.append(lastName_column.values[student])
                errorScore.append(scores_column.values[student])
                if 'Percent Score' in df.columns:
                    errorPercent.append(percent_column.values[student])
                   
        elg.logGenerator(df, errorNum, errorFName, errorLName, errorScore, errorPercent)
        
        #combine output columns 
        output = [outputNames,outputNumbers,outputSections]
           
        output.append(outputScores)
        if 'Percent Score' in df.columns:
            output.append(outputPercent)
        
        #build CSV output    
        if len(output) == 4:
            rows = zip(output[0], output[1], output[2], output[3])  
        elif len(output) == 5:
            rows = zip(output[0], output[1], output[2], output[3], output[4]) 
            
        with open('Import_into_Canvas.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                for row in rows:
                    writer.writerow(row)
        
        input("\nSuccess! A CSV file titled Import_into_Canvas is ready to be uploaded into the Canvas Gradebook and can be found in the same directory as this script. Hit Enter or close this window to exit:")
   
    except:
        decision = input("\nSomething went wrong. Perhaps you entered an invalid Canvas API Access Token or Course ID? Hit Enter to restart the program or type 'quit' to exit: ")
        if decision.lower() == "quit":
            return
        else:
            formatCSV()
 
if __name__ == '__main__':            
    formatCSV()