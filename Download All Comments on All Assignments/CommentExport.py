# -*- coding: utf-8 -*-

#make sure you pip install the necessary libraries before running the script
try:
    import pandas 
except:
    import pip
    pip.main(['install', 'pandas'])
    import pandas
try:
    import os
except:
    import pip
    pip.main(['install', 'os'])
    import os
try:
    import api_calls as api
except:
    print("You are missing the api_calls.py file. Please ensure this file is in the same folder as this script and try again.")

def CommentExport():
    #get course ID 
    courseID = input("\nEnter Course ID: ").strip() 
    try:
        #api calls to gather course and student information
        courseStudents = api.getCourseStudents(courseID)
        courseDetails = api.getCourseDetails(courseID)
        courseName = courseDetails.get('name')
        courseAssignments = api.getAssignments(courseID)
        
        #Creates a dictionary of every student and prepares it for the addition of their commented assignment (basically reorganize)
        assignmentByStudent = {}
        for student in courseStudents:
            assignmentByStudent[student.get('name')] = {"studentName": student.get('name'), "studentID": student.get('id')}

        decision = input("\nFound course \"" + courseName + "\". Hit Enter if this is the correct course or type 'change' to select a different course: ").strip()
        while decision.lower() == "change":
            courseID = input("\nEnter Course ID: ").strip() 
            courseStudents = api.getCourseStudents(courseID)
            courseDetails = api.getCourseDetails(courseID)
            courseName = courseDetails.get('name')
            decision = input("\nFound course " + courseName + ". Hit Enter if this is the correct course or type 'change' to select a different course: ").strip()
        
        #For each assignment, check to see if it has a comment and if it does give the corresponding student in "assignmentByStudent"the name of the assignment and it's comments
        for assignment in courseAssignments:
                courseSubmissions = api.getAssignmentSubmission(courseID, assignment.get('id'))
                for submission in courseSubmissions:
                    if submission.get('submission_comments'):
                        assignmentByStudent[submission.get('user').get('name')][assignment.get('name')] = []
                        for comment in submission.get('submission_comments'): 
                            assignmentByStudent[submission.get('user').get('name')][assignment.get('name')].append(comment.get('comment')) 
        
        spreadsheet = pandas.DataFrame.from_dict(assignmentByStudent, orient='index')
        
        #Ask user to enter name of prefered csv output (if blank uses their course name _GroupList.csv)
        title = input("\nPlease enter what you would like to name the completed file, including the extension (.csv), and then press Enter (or leave empty for "+courseName+"_AllComments.csv): ").strip()
        if(title in ""):
            title = courseName+'_AllComments.csv'
        #If user forgets to add .csv system will add it in here
        if title.endswith('.csv'):
            pass
        else:
            print("\nIt seems like you forgot to add the .csv extension. Don't worry I've added it for you!")
            title = os.path.splitext(title)[0]+'.csv'
        #If the title is somehow blank or already take, ask user to re-enter name and loop until its a valid name
        if (os.path.isfile(title) or not title or not title.endswith('.csv') or title=='.csv'):
            while (os.path.isfile(title) or not title or not title.endswith('.csv') or title=='.csv'):
                if title=='quit':
                    return
                else:
                    title = loopFileName(courseName)
        #Creates a csv with the given title name and tell user that the file has been created!
        spreadsheet.to_csv(title, encoding="utf-8", index=False)
        input("\nSuccess! CSV file named: " + title + " has been successfully created in the same directory as this script. Hit enter or close this window to exit:").strip()    
   
    except Exception as e:
        print(e)
        decision = input("\nSomething went wrong. Perhaps you entered an invalid Canvas API Access Token or Course ID? Hit Enter to restart the program or type 'quit' to exit: ")
        if decision.lower() == "quit":
            return
        else:
            CommentExport()
 
if __name__ == '__main__':            
    CommentExport()
    
#Occurs only if user wants formatted name is already taken. Asks user if they want to correct or quit format, and if they want to correct it ensures they the file name is not blank and is a unique file name (otherwise it'd over write other files)   
def loopFileName(courseName):
    rename = input("\n\t(Invalid Name) The previous name ended up compliling into a name that the computer won't accept.\n\tWould you like to try again with a new name?\n\tHit Enter to try again or type 'quit' to exit:  ").strip()  
    if rename.lower() == "quit":
        return 'quit'
    else:
        title = input("\nPlease enter what you would like to name the completed file, including the extension (.csv), and then press Enter (or leave empty for "+courseName+"_AllComments.csv): ").strip()
        if (os.path.isfile(title)):
            while(os.path.isfile(title)):
                title = input("\n\t(Conflicting Name) The previous name ended up compliling into a name thats already taken.\n\tWould you like to try again with a new name?\n\tHit Enter to try again or type 'quit' to exit:  ").strip()  
                if(title.lower() == "quit"):
                    return 'quit'
        #If the title is blank ask the user for a non blank name. This is because otherwise it will create a csv file without a name and the file will not open.
        if not title:
            title = courseName+'_AllComments.csv'
        #Check to see if name includes .csv, if not change to .csv file
        if title.endswith('.csv'):
            pass
        else:
            print("\nIt seems like you forgot to add the .csv extension. Don't worry I've added it for you!")
            title = os.path.splitext(title)[0]+'.csv'
        return title
