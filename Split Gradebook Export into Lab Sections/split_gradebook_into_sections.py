# -*- coding: utf-8 -*-

#make sure you pip install the necessary libraries before running the script
import os
import pandas
import api_calls as api

def splitCSV():
    
    #get course ID and token
    courseID = input("\nEnter Course ID: ").strip()

    try:
        #gather data from the Canvas API
        assignmentGroups = api.getAssignmentGroups(courseID)
        courseDetails = api.getCourseDetails(courseID)
        courseSections = api.getCourseSections(courseID)
        
        courseName = courseDetails.get('name')
        courseCode = courseDetails.get('course_code')
        numSections = len(courseSections)
        
        decision = input("\nFound course \"" + courseName + "\". Hit Enter if this is the correct course or type 'change' to select a different course: ").strip()
        
        while decision.lower() == "change":
            
            courseID = input("\nEnter Course ID: ").strip()  
            
            assignmentGroups = api.getAssignmentGroups(courseID)
            courseDetails = api.getCourseDetails(courseID)
            courseSections = api.getCourseSections(courseID)
            
            courseName = courseDetails.get('name')
            numSections = len(courseSections)
            
            decision = input("\nFound course " + courseName + ". Hit Enter if this is the correct course or type 'change' to select a different course: ").strip()
            
        #read full CSV export
        while True:
            title = input("\nMake sure the exported Canvas Gradebook CSV file is in the same directory as this script. Enter the name of the file, including the extension (.csv), and then press Enter: ") 
            try:
                df = pandas.read_csv(title)
                break
            except FileNotFoundError:
                decision = input("\nFile not found. Make sure you have placed the exported Canvas Gradebook CSV file in the same directory as this script and that you typed the filename correctly, including the extension (.csv). Hit Enter to try again or type 'quit' to exit: ")
                if decision.lower() == "quit":
                    return
        
        #if there were muted assignments, remove the extra row that was generated
        for column in df.columns:
            if df[column].astype(str).str.contains('Muted').any():
                df = df.iloc[1:]
                break
            
        #check that the spreadsheet contains the Lab column, which is required for this script to work
        if 'Lab' not in df.columns:
            input('Your course does not have the lab column in the Gradebook, therefore this script cannot work. Hit ENTER to close the program:')
            return
        
        #delete undesired columns (by default, only columns required for a successful import back into Canvas are kept)
        if 'ID' in df.columns:
            del df['ID']
        if 'SIS Login ID' in df.columns:
            del df['SIS Login ID']
        if 'Notes' in df.columns:
            del df['Notes']
        if 'Student Number' in df.columns:
            del df['Student Number']
        if 'Lecture' in df.columns:
            del df['Lecture']
        if 'Tutorial' in df.columns:
            del df['Tutorial']
        if 'Current Points' in df.columns:
            del df['Current Points']
        if 'Final Points' in df.columns:
            del df['Final Points']
        if 'Current Grade' in df.columns:
            del df['Current Grade']
        if 'Unposted Current Grade' in df.columns:
            del df['Unposted Current Grade']
        if 'Final Grade' in df.columns:
            del df['Final Grade']
        if 'Unposted Final Grade' in df.columns:
            del df['Unposted Final Grade']
        if 'Current Score' in df.columns:
            del df['Current Score']
        if 'Unposted Current Score' in df.columns:
            del df['Unposted Current Score']
        if 'Final Score' in df.columns:
            del df['Final Score']
        if 'Unposted Final Score' in df.columns:
            del df['Unposted Final Score']
         
        #loop removes all of the "read only" columns that are generated for each assignment group
        for i in range(0, len(assignmentGroups)):

            if assignmentGroups[i]['name']+ ' Current Points' in df.columns:
                del df[assignmentGroups[i]['name']+ ' Current Points']
            if assignmentGroups[i]['name']+ ' Final Points' in df.columns:
                del df[assignmentGroups[i]['name']+ ' Final Points']
            if assignmentGroups[i]['name']+ ' Current Score' in df.columns:
                del df[assignmentGroups[i]['name']+ ' Current Score']
            if assignmentGroups[i]['name']+ ' Unposted Current Score' in df.columns:
                del df[assignmentGroups[i]['name']+ ' Unposted Current Score']
            if assignmentGroups[i]['name']+ ' Final Score' in df.columns:
                del df[assignmentGroups[i]['name']+ ' Final Score']
            if assignmentGroups[i]['name']+ ' Unposted Final Score' in df.columns:
                del df[assignmentGroups[i]['name']+ ' Unposted Final Score']
            
        #build CSV output files
        for size in range(0, numSections):
            
            #the last 3 characters of the section usually contains the lab info (e.g. for section CHEM 111 L01, L01 is what we want to match in the lab column)
            name = courseSections[size]['name'][-3:]
            
            #don't create a file for the students that are exempt from the labs
            if "XMT" in name:
                continue
            else:
                #create a folder for the output files in the same directory as script
                path = os.getcwd()
                directory = path+"/"+courseCode+"/"
                os.makedirs(os.path.dirname(directory), exist_ok=True)
                
                #separate the files based on lab section
                df2 = df.loc[df['Lab'] == name] 
                
                #add the points possible row back in
                pandas.concat([df2[:0],df.iloc[0,:].to_frame().T,df2[0:]],ignore_index=True).to_csv(directory + courseCode + " " + name+".csv", encoding="utf-8", index=False)
            
        input("\nSuccess! CSV files for each lab section have been created and can be found in a folder titled " + courseCode + " in the same directory as this script. Hit enter or close this window to exit:")
                   
    except:
        decision = input("\nSomething went wrong. Make sure you have added your token to the canvas.cfg file and that you entered the correct course ID. Hit Enter to restart the program or type 'quit' to exit: ")
        if decision.lower() == "quit":
            return
        else:
            splitCSV()
            
if __name__ == '__main__':  
    splitCSV()
