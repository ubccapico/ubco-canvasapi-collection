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
    
def DownloadDiscussion():
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

        courseStudents = api.getCourseStudents(courseID)
        studentList = {}
        for student in courseStudents:
            studentList[student['name']] = student['sis_user_id']
        try:
            topicID = input("\nPlease Enter Topic ID: ").strip()
            topicDetails = api.getSingleTopic(courseID, topicID)
            
            #Enforces FIPPA compliance
            fippaDecision = input("Do you wish to have Student Name and ID showing (yes/no, default=yes): ").strip()
            #This will clean the input from the user. Using in function any combination of 'y', 'e', 's', or '' will be run yes and 'n' and 'o' will set to no
            if fippaDecision in 'yes':
                fippaDecision = 'yes'
            elif fippaDecision in 'no':
                fippaDecision = 'no'
            else:
                #If they don't enter any character of '', 'y', 'e', 's', 'n', or 'o' it will repeat asking the user for input
                while (fippaDecision not in 'yes') and (fippaDecision not in 'no'):
                   fippaDecision = input("Do you wish to have Student Name and ID showing (yes/no): ").strip() 
                   if fippaDecision in 'yes':
                       fippaDecision = 'yes'
                   elif fippaDecision in 'no':
                       fippaDecision = 'no'       
            try:      
                outputFile = FIPPA(fippaDecision, topicDetails, studentList)
                try:
                    title = input("\nPlease enter what you would like to name the completed file, including the extension (.csv), and then press Enter (or leave empty for "+courseName+"_DiscussionDownload.csv): ").strip()
                    if(title in ""):
                        title = courseName+'_DiscussionDownload.csv'
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
                    outputFile.to_csv(title, encoding="utf-8", index=False)
                    input("\nSuccess! CSV file named: " + title + " has been successfully created in the same directory as this script. Hit enter or close this window to exit:").strip()    
                    
                #Raise error if issue while naming and creating file
                except Exception as e:
                    print(e)
                    decision = input("\nThere was an issue while attempting to name and/or creating the file. Please contact the CTL for assitional assistance. Hit Enter to restart the program or type 'quit' to exit: ")
                    if decision.lower() == "quit":
                        return
                    else:
                        DownloadDiscussion()
            #Raise error if problem creating the digital file
            except Exception as e:
                print(e)
                decision = input("\nThere was an issue while attempting to create the outputted file. Please contact the CTL for assitional assistance. Hit Enter to restart the program or type 'quit' to exit: ")
                if decision.lower() == "quit":
                    return
                else:
                    DownloadDiscussion()
        #If there is an issue with the discussion, ask users to try again
        except Exception as e:
            print(e)
            decision = input("\nThere was an error attempting to connect to your discussion. Please check to make sure you have the correct discussion ID and try again. Hit Enter to restart the program or type 'quit' to exit: ")
            if decision.lower() == "quit":
                return
            else:
                DownloadDiscussion()
    #If there is an issue with API or token, ask user to check
    except Exception as e:
        print(e)
        decision = input("\nSomething went wrong. Perhaps you entered an invalid Canvas API Access Token or Course ID? Hit Enter to restart the program or type 'quit' to exit: ")
        if decision.lower() == "quit":
            return
        else:
            DownloadDiscussion()

#Occurs only if user wants formatted name is already taken. Asks user if they want to correct or quit format, and if they want to correct it ensures they the file name is not blank and is a unique file name (otherwise it'd over write other files)   
def loopFileName(courseName):
    rename = input("\n\t(Invalid Name) The previous name ended up compliling into a name that the computer won't accept.\n\tWould you like to try again with a new name?\n\tHit Enter to try again or type 'quit' to exit:  ").strip()  
    if rename.lower() == "quit":
        return 'quit'
    else:
        title = input("\nPlease enter what you would like to name the completed file, including the extension (.csv), and then press Enter (or leave empty for "+courseName+"_DiscussionDownload.csv): ").strip()
        if (os.path.isfile(title)):
            while(os.path.isfile(title)):
                title = input("\n\t(Conflicting Name) The previous name ended up compliling into a name thats already taken.\n\tWould you like to try again with a new name?\n\tHit Enter to try again or type 'quit' to exit:  ").strip()  
                if(title.lower() == "quit"):
                    return 'quit'
        #If the title is blank ask the user for a non blank name. This is because otherwise it will create a csv file without a name and the file will not open.
        if not title:
            title = courseName+'_DiscussionDownload.csv'
        #Check to see if name includes .csv, if not change to .csv file
        if title.endswith('.csv'):
            pass
        else:
            print("\nIt seems like you forgot to add the .csv extension. Don't worry I've added it for you!")
            title = os.path.splitext(title)[0]+'.csv'
        return title

#This is the function used to process the discussion post to
def FIPPA(fippaDecision, topicDetails, studentList):
    #If you want student names, create dictionary relating namnes and ids
    if fippaDecision == 'yes':
        student_canvasList = {}
        for student in topicDetails['participants']:
            if student['id'] not in student_canvasList:
                student_canvasList[student['id']] = student['display_name']

    studentResponseList = {}
    #For each response in the discussion
    for response in topicDetails['view']:
        if fippaDecision == 'no':
            studnetResponse = response['user_id']
            #print(response['user_id'])
        elif fippaDecision == 'yes':
            studnetResponse = student_canvasList[response['user_id']]        
        #If the student hasn't been added to the dictionary, add them to the dictionary
        if studnetResponse not in studentResponseList:
            studentResponseList[studnetResponse] = []
            if fippaDecision == 'yes':
                studentResponseList[studnetResponse].append(studentList[studnetResponse])  
        #Then if student is in dictionary, add their response to their dictionary list (a list inside a dictionary)
        if studnetResponse in studentResponseList:
            studentResponseList[studnetResponse].append(str(response['message']).replace('<p>', '').replace('</p>', ''))
        
        #Then if that reponse has a reply, for each reply check who its from and add it to responder's dictionary list
        if 'replies' in response:
            #For each reply to a response
            for reply in response['replies']:
                if fippaDecision == 'no':
                    studnetReply = reply['user_id'] 
                elif fippaDecision == 'yes':
                    studnetReply = student_canvasList[reply['user_id']]  
  
                #Check if replier has been added to dictionary, and if not then add them to dictionary
                if studnetReply not in studentResponseList:
                    studentResponseList[studnetReply] = []
                    if fippaDecision == 'yes':
                        if studnetReply in studentList:
                            studentResponseList[studnetReply].append(studentList[studnetReply])
                        else:
                            studentResponseList[studnetReply].append('None')

                #Then if replier is in dictionary, add their reply to their dictionary list (a list inside a dictionary)
                if studnetReply in studentResponseList:
                    studentResponseList[studnetReply].append(str(reply['message']).replace('<p>', '').replace('</p>', ''))
    #Converts dictionary with lists inside to dataframe
    outputFile = pandas.DataFrame.from_dict(studentResponseList, orient="index")
    #Takes sis_id from index and convert to column
    outputFile = outputFile.reset_index()
    
    #Rename columns so that they match what the column contains
    columnIDList = []
    startPoint = 0
    if fippaDecision == 'no':
        columnIDList.append('Canvas_ID')
        startPoint = 1
    elif fippaDecision == 'yes':
        columnIDList.append('StudentName')
        columnIDList.append('SIS_ID')
        startPoint = 2

    #For each response, add to columnIDList so that all student responses are listed without limit
    for response in range(startPoint, len(outputFile.columns)):
        if fippaDecision == 'no':
            columnIDList.append('Response' + str(response))
        elif fippaDecision == 'yes':
            columnIDList.append('Response' + str(response-1))
    #Change column names in dataframe
    outputFile.columns = columnIDList
     
    #If contains student names, ask if sort by first nam, last namne, or student number
    if fippaDecision == 'yes':
        #Ask how user wants to sort
        sortDecision = input("Do you wish to sort by first, last name, or student number? (first/last/number, default=first): ").strip()
        #Basic loop to make sure a proper sorting decision is made
        if sortDecision not in 'first' or sortDecision not in 'last' or sortDecision not in 'number':
            while sortDecision not in 'first' and sortDecision not in 'last' and sortDecision not in 'number':
                sortDecision = input("Do you wish to sort by first, last name, or student number? (first/last/number, default=first): ").strip()

        outputFile["FirstName"] = outputFile["StudentName"].str.split().str[0]
        outputFile["LastName"] = outputFile["StudentName"].str.split().str[-1]       
        outputFile = outputFile.drop('StudentName', axis=1)
        cols = outputFile.columns.tolist()
        newcols = cols[-1:] + cols[-2:-1] + cols[0:1] + cols[1:-2]
        outputFile = outputFile[newcols]
        
        #If sort by first name, sort first by first name then by student number
        if sortDecision in 'first':
            outputFile = outputFile.sort_values(['FirstName', 'LastName', 'SIS_ID'])
        #If sort by last name, create column for last substring in, then sort by that substring followed by first name then student number. Finally remove substring column
        elif sortDecision in 'last':
            outputFile = outputFile.sort_values(['LastName', 'FirstName', 'SIS_ID'])
        #If sort by student number, just sort by student number
        elif sortDecision in 'number':
            outputFile = outputFile.sort_values(['SIS_ID', 'LastName', 'FirstName'])

    #Return output file
    return outputFile    
    
if __name__ == '__main__':            
    DownloadDiscussion()