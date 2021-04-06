# -*- coding: utf-8 -*-

#make sure you pip install the necessary libraries before running the script
try:
    import os
except:
    import pip
    pip.main(['install', 'os'])
    import os
try:
    import pandas
except:
    import pip
    pip.main(['install', 'pandas'])
    import pandas
try:
    import glob
except:
    import pip
    pip.main(['install', 'glob'])
    import glob
try:
    import api_calls as api
except:
    print("You are missing the api_calls.py file. Please ensure this file is in the same folder as this script and try again.")

#*****Main method*****
#This method contains the bulk of the code. Here the code will format a new spreadsheet for the user
def revel():
    #get course ID 
    courseID = input("\nEnter Course ID: ").strip() 
    #Try to read the file (if the user wants to quit, the title will be 'quit')
    try:
        #api calls to gather course and student information
        courseDetails = api.getCourseDetails(courseID)
        courseName = courseDetails.get('name')
        decision = input("\nFound course \"" + courseName + "\". Hit Enter if this is the correct course or type 'change' to select a different course: ").strip()
        #if the course doesn't exist, either let the user reenter or quit the program
        while decision.lower() == "change":
            courseID = input("\nEnter Course ID: ").strip() 
            courseDetails = api.getCourseDetails(courseID)
            courseName = courseDetails.get('name')
            decision = input("\nFound course " + courseName + ". Hit Enter if this is the correct course or type 'change' to select a different course: ").strip()
        #gather the remaining single call api calls we need
        courseStudents = api.getCourseStudents(courseID)
        studentList = {}
        for student in courseStudents:
            studentList[student.get('name').replace(" ", "").lower()] = [student.get('sis_user_id')]
        #Get file name from user
        title = input("\nEnsure the Revel CSV file is in the same location as this script. Enter the name of the file (including the extension .csv) and then press Enter: ").strip()
        try:
            if title=='quit': #If users want to quit, exit program
                return
            originalFile = pandas.read_csv(title, skiprows=1)
            try:
                #Start processing the file
                #Combine first and last name
                originalFile["Student"] = originalFile["First Name"].map(str) + " " + originalFile["Last Name"]
                #Create column for ID and Section
                originalFile["SIS User ID"] = ""
                originalFile["Section"] = ""
                #Drop columns & reorganize
                originalFile = originalFile.drop(['Email' , 'First Name', 'Last Name'], axis=1)
                cols = list(originalFile.columns)
                cols = cols[-3:] + cols[:-3]
                originalFile = originalFile[cols]
                #Create a list of students to drop who aren't in the Canvas course
                studentToDrop = []
                for index, row in originalFile.iterrows():
                    if((originalFile.at[index, 'Student']).replace(" ", "").lower() in studentList):
                        if(studentList[(originalFile.at[index, 'Student']).replace(" ", "").lower()][0] is None):
                            studentToDrop.append(index)
                        else:
                            originalFile.at[index, 'SIS User ID'] = studentList[(originalFile.at[index, 'Student']).replace(" ", "").lower()][0]
                    elif(originalFile.at[index, 'Student'] == 'Total Points'):
                        pass
                    else:
                        studentToDrop.append(index)
                #If students are going to be dropped, create a error log excel sheet with proper information
                if(len(studentToDrop)!=0):
                    droppedStudents = pandas.DataFrame(columns=cols)
                    for student in studentToDrop:
                        droppedStudents = droppedStudents.append(originalFile.iloc[student], ignore_index = True)
                    droppedStudents = droppedStudents.drop(['SIS User ID' , 'Section'], axis=1)
                #Finish formatting Canvas ready file
                originalFile = originalFile.drop(studentToDrop)
                originalFile.loc[-1]=''
                originalFile.at[0, 'Student'] = 'Points Possible'
                originalFile.at[0, 'SIS User ID'] = ''
                originalFile.sort_index(inplace=True)
                originalFile.index = originalFile.index + 1  # shifting index
                #Start naming process
                title = input("\nPlease enter what you would like to name the completed file, including the extension (.csv), and then press Enter (or leave empty for "+courseName+"_GroupList.csv): ").strip()
                if(title in ""):
                    title = courseName+'_GroupList.csv'
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
                            title = loopFileName()
                #Creates a csv with the given title name and tell user that the file has been created!
                originalFile.to_csv(title, encoding="utf-8", index=False)
                if(len(studentToDrop)!=0):
                    droppedStudents.to_csv('errorLog.csv', encoding="utf-8", index=False)
                    print('\nAn Error Log was produced. Not all students in the given file exist in Canvas. Please check the Error Log for which students could not be identified.')
                input("\nSuccess! CSV file named: " + title + " has been successfully created in the same directory as this script. Hit enter or close this window to exit:").strip()    
            except Exception as e:
                print(e)
                print('There was an issue formatting ' + str(title) + '. Please check the integrity of the file and try again.')
        #If there is an issue reading the file, throw an error
        except Exception as e:
            print(e)
            print('There was an issue reading ' + str(title) + '. Please check the integrity of the file and try again.')
    #If the program fails in general, throw this error and ask user if they want to retry
    except Exception as e:
        print(e)
        decision = input("\nSomething went wrong. Perhaps you entered an invalid Canvas API Access Token or Course ID? Hit Enter to restart the program or type 'quit' to exit: ")
        if decision.lower() == "quit":
            return
        else:
            revel()

#Allows user to input target file name and if the program doesn't find it or it isn't a csv, this method will be called and a new file can be chosen
def getFileName():
    #General Input Message
    text_String = "\nMake sure the exported spreadsheet CSV file is in the same directory as this script. Enter the name of the file, including the extension (.csv), and then press Enter (or enter quit to exit): "
    title = input(text_String).strip()
    path = title
    textError = ''
    #While the file does not exist, isn't a csv, or the user wants to quit
    while(len(glob.glob(path))!=1 or not title.endswith('.csv') or title == 'quit'):
        #If the user wants to quit, stop the program
        if(title == 'quit'):
            return 'quit'
        #Else if the file doesn't exist, tell the user the file doesn't exist
        elif(len(glob.glob(path))!=1):
            textError = '\nThe given file was not found. Please check to make sure the file exists in the same location as this script and try again. '
        #Else if the file is not a csv, tell the user it needs to be a csv
        elif (not title.endswith('.csv')):
            textError = '\nThe given file did not include a .csv file tag at the end. Please try again and make sure to include the .csv to the end of the file name. '
        #Here it will tell the user why the file doesn't work, repeat the general input message, and let users input a new file name
        title = input(textError + text_String).strip()
        #Reset path to the new title
        path = title
    #Presuming the user doesn't quit, this will return a valid file
    return title

#Occurs only if user wants formatted name is already taken. Asks user if they want to correct or quit format, and if they want to correct it ensures they the file name is not blank and is a unique file name (otherwise it'd over write other files)   
def loopFileName():
    rename = input("\n\t(Invalid Name) The previous name ended up compliling into a name that the computer won't accept.\n\tWould you like to try again with a new name?\n\tHit Enter to try again or type 'quit' to exit:  ").strip()  
    if rename.lower() == "quit":
        return 'quit'
    else:
        title = input("\nPlease enter what you would like to name the completed file, including the extension (.csv), and then press Enter (or leave empty for GroupList.csv): ").strip()
        if (os.path.isfile(title)):
            while(os.path.isfile(title)):
                title = input("\n\t(Conflicting Name) The previous name ended up compliling into a name thats already taken.\n\tWould you like to try again with a new name?\n\tHit Enter to try again or type 'quit' to exit:  ").strip()  
                if(title.lower() == "quit"):
                    return 'quit'
        #If the title is blank ask the user for a non blank name. This is because otherwise it will create a csv file without a name and the file will not open.
        if not title:
            title = 'GroupList.csv'
        #Check to see if name includes .csv, if not change to .csv file
        if title.endswith('.csv'):
            pass
        else:
            print("\nIt seems like you forgot to add the .csv extension. Don't worry I've added it for you!")
            title = os.path.splitext(title)[0]+'.csv'
        return title
    
#Starts code
if __name__ == '__main__':  
    revel()