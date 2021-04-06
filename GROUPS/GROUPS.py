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
    import numpy as np
except:
    import pip
    pip.main(['install', 'numpy'])
    import numpy as np
try:
    import string
except:
    import pip
    pip.main(['install', 'string'])
    import string
try:
    import api_calls as api
except:
    print("You are missing the api_calls.py file. Please ensure this file is in the same folder as this script and try again.")

def groupListGenerator():
    #get course ID 
    courseID = input("\nEnter Course ID: ").strip() 
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
        courseSections = api.getCourseSections(courseID)
        courseGroupCategory = api.getGroupCategory(courseID)
        #Ask User if they want Student Number, Sections, and/or Section Check
        numberDecision = input("Would you like to include Student Numbers in the output? (y/n): ").strip()
        numberDecision = inputYNCheck(numberDecision, 'yes')
        sectionDecision = input("Would you like to include the Section each Student is enrolled in the output? (y/n): ").strip()
        sectionDecision = inputYNCheck(sectionDecision, 'yes')
        if(sectionDecision=='yes'):    
            checkDecision = input("Would you like to include checking that each Student in each Group is from the same Section in the output? (y/n): ").strip()
            checkDecision = inputYNCheck(checkDecision, 'yes')
        else:
            checkDecision='no'
        decisionList = [numberDecision, sectionDecision, checkDecision]
        #for each section in the course, get it's id and name to put into a dictionary
        courseList = {}
        for section in courseSections:
            courseList[section.get('id')] = [section.get('name')]
        #for each student create a dictionary regarding their canvas id, name, and section (used to have sis_id but doesn't work anymore)
        studentDic = {}
        for student in courseStudents:
            #since a studnet can be in multiple "sections" (lecture and tutorial, ect.) generate a list, sort list, and convert to string
            enrolledSections = []
            stringEnrolledSections = ""
            for section in student.get('enrollments'):
                enrolledSections.append(courseList[section.get('course_section_id')][0])
            enrolledSections.sort()
            for section in enrolledSections:
                stringEnrolledSections = stringEnrolledSections+section+", "
            stringEnrolledSections = stringEnrolledSections[:-2]
            studentDic[student.get('id')] = [student.get('name'), student.get('sis_user_id'), stringEnrolledSections]
        #generate variables that will be used
        defaultColumns = ['GroupSet', 'Group', 'GroupSize']
        spreadsheet = pandas.DataFrame(columns=defaultColumns) #only need these two as the amount of students varies based off of group and set
        GroupSet = ""
        Group = ""
        maxGroupSize = 0
        #for each group set gather it's individual groups
        for GroupCategory in courseGroupCategory:
            courseGroupSetGroups = api.getGroups(GroupCategory.get('id'))
            groupCategoryUnassignedStudents = api.getUnassignedGroup(GroupCategory.get('id'))
            GroupSet = GroupCategory.get('name')
            #for each group in a group set gather it's students and create an entry into spreadsheet
            for groupSet in courseGroupSetGroups:
                Group = groupSet.get('name')
                groupMembers = api.getGroupMembers(courseID, groupSet.get('id'))
                spreadsheet = spreadsheet.append({'GroupSet' : GroupSet, 'Group' : Group} , ignore_index=True)
                counter = 1
                #for each group member in a group in a set gather their name and section and add them in a row to a group
                for student in groupMembers:                    
                    addStudentToList(spreadsheet, studentDic, student, 'user_id', counter, decisionList)
                    counter = counter+1
                if(counter-1>maxGroupSize):
                    maxGroupSize = counter-1
                spreadsheet.at[spreadsheet.index[-1], 'GroupSize'] = counter-1
            #Same as above except only for students not in a group
            if(len(groupCategoryUnassignedStudents)>0):
                counter = 1
                listCounter = 1
                spreadsheet = spreadsheet.append({'GroupSet' : GroupSet, 'Group' : 'Unassigned List '+str(listCounter)} , ignore_index=True)
                for student in groupCategoryUnassignedStudents: 
                    #Due to how many students can be unassigned I decided that each unassigned list can only contain 5 students (on the 6th it creates a new list and ass the student as 1st)
                    if(counter == 6): #this is inclusive. So what ever number is compared to it will restart on that number
                        spreadsheet.at[spreadsheet.index[-1], 'GroupSize'] = len(groupCategoryUnassignedStudents)
                        listCounter = listCounter+1
                        spreadsheet = spreadsheet.append({'GroupSet' : GroupSet, 'Group' : 'Unassigned List '+str(listCounter)} , ignore_index=True)
                        counter = 1
                    addStudentToList(spreadsheet, studentDic, student, 'id', counter, decisionList)
                    counter = counter+1
                spreadsheet.at[spreadsheet.index[-1], 'GroupSize'] = len(groupCategoryUnassignedStudents)
        #Compares each student in each group to see if they're from the same section.
        #Due to how this works, it must be the last column in the spreadsheet otherwise the code needs to be modified
        if(decisionList[2]=='yes'):
            #Gets some variables ready
            decisionListYesCount = 0
            for option in decisionList:
                if(option=='yes'):
                    decisionListYesCount=decisionListYesCount+1
            #If there is more than 1 member in any group, check for same section (need this otherwise the column won't work)
            if(maxGroupSize>1):
                numberOfRows = int(len(spreadsheet.index))
                #Create the column for the excel string
                spreadsheet['Same Section?'] = ""
                #Makes the excel macro string
                for studentGroup in range(len(defaultColumns), numberOfRows+len(defaultColumns)):
                    excelQuery = "=IF(AND("
                    for studentEnrolledInSection in range(0, (maxGroupSize-1)*decisionListYesCount, decisionListYesCount):
                        #Yes I know it's ugly but it works. It will scale for each decision you give the user so you shouldn't need to modify it :)
                        excelQuery = excelQuery + 'OR('+numToLetter(len(defaultColumns)+decisionListYesCount)+str(studentGroup-1)+'='+numToLetter(studentEnrolledInSection+2+len(defaultColumns)+((decisionListYesCount-1)*2))+str(studentGroup-1)+', ISBLANK('+numToLetter(studentEnrolledInSection+2+len(defaultColumns)+((decisionListYesCount-1)*2))+str(studentGroup-1)+')),'
                    excelQuery = excelQuery[:-1]+'), "Same", "Different")'
                    #Once the query has been made, add it to that row for use
                    spreadsheet.at[studentGroup-len(defaultColumns), 'Same Section?'] = excelQuery
        #Remove any nan entries (gotta scrub)
        spreadsheet = spreadsheet.replace(np.nan, '', regex=True)
        #Ask user to enter name of prefered csv output (if blank uses their course name _GroupList.csv)
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
                    title = loopFileName(courseName)
        #Creates a csv with the given title name and tell user that the file has been created!
        spreadsheet.to_csv(title, encoding="utf-8", index=False)
        input("\nSuccess! CSV file named: " + title + " has been successfully created in the same directory as this script. Hit enter or close this window to exit:").strip()    
    #If the program fails in general, throw this error and ask user if they want to retry
    except Exception as e:
        print(e)
        decision = input("\nSomething went wrong. Perhaps you entered an invalid Canvas API Access Token or Course ID? Hit Enter to restart the program or type 'quit' to exit: ")
        if decision.lower() == "quit":
            return
        else:
            groupListGenerator()

#Checks to see if value is in checkAgainst (if value is enter than it will be in checkAgainst)           
def inputYNCheck(value, checkAgainst):
    if(value in checkAgainst):
        return(checkAgainst)
    else:
        return('no')

#Adds each student in a group to the spreadsheet        
def addStudentToList(spreadsheet, studentDic, student, columnSearch, counter, decisionList):
    #If spreadsheet doesn't have a column yet for this student, create one
    if 'Student Name ' + str(counter) not in spreadsheet:
        spreadsheet['Student Name ' + str(counter)] = ''
        if(decisionList[0]=='yes'):
            spreadsheet['Student Number ' + str(counter)] = ''
        if(decisionList[1]=='yes'):
            spreadsheet['Section ' + str(counter)] = ''
    #For the given studnet write to spreadsheet their name and if user wants their number and/or section
    try:
        StudentName = studentDic[student.get(columnSearch)][0]
        if(decisionList[0]=='yes'):
            StudentNumber = studentDic[student.get(columnSearch)][1]
        if(decisionList[1]=='yes'):
            Section=studentDic[student.get(columnSearch)][2]
    #If there is an issue writting student to spreadsheet, for that cell write their Canvas ID and state there was an issue
    except:
        StudentName = 'Canvas ID: ' + student.get(columnSearch) + '(Not the same as SIS ID)'
        if(decisionList[0]=='yes'):
            StudentNumber = 'Canvas ID: ' + student.get(columnSearch) + '(Not the same as SIS ID)'
        if(decisionList[1]=='yes'):
            Section = 'Unknown'
    #Once the varibales have been set change spreadsheet column for that student to match
    spreadsheet.at[spreadsheet.index[-1], 'Student Name ' + str(counter)] = StudentName
    if(decisionList[0]=='yes'):
        spreadsheet.at[spreadsheet.index[-1], 'Student Number ' + str(counter)] = StudentNumber
    if(decisionList[1]=='yes'):
        spreadsheet.at[spreadsheet.index[-1], 'Section ' + str(counter)] = Section

#Occurs only if user wants formatted name is already taken. Asks user if they want to correct or quit format, and if they want to correct it ensures they the file name is not blank and is a unique file name (otherwise it'd over write other files)   
def loopFileName(courseName):
    rename = input("\n\t(Invalid Name) The previous name ended up compliling into a name that the computer won't accept.\n\tWould you like to try again with a new name?\n\tHit Enter to try again or type 'quit' to exit:  ").strip()  
    if rename.lower() == "quit":
        return 'quit'
    else:
        title = input("\nPlease enter what you would like to name the completed file, including the extension (.csv), and then press Enter (or leave empty for "+courseName+"_GroupList.csv): ").strip()
        if (os.path.isfile(title)):
            while(os.path.isfile(title)):
                title = input("\n\t(Conflicting Name) The previous name ended up compliling into a name thats already taken.\n\tWould you like to try again with a new name?\n\tHit Enter to try again or type 'quit' to exit:  ").strip()  
                if(title.lower() == "quit"):
                    return 'quit'
        #If the title is blank ask the user for a non blank name. This is because otherwise it will create a csv file without a name and the file will not open.
        if not title:
            title = courseName+'_GroupList.csv'
        #Check to see if name includes .csv, if not change to .csv file
        if title.endswith('.csv'):
            pass
        else:
            print("\nIt seems like you forgot to add the .csv extension. Don't worry I've added it for you!")
            title = os.path.splitext(title)[0]+'.csv'
        return title

#Used to convert a given number in a letter (to track excel columns)
def numToLetter(number):
    #Create a dictionary based of off the ascii table, it relates a letter to a number
    numberToLetter = dict(enumerate(string.ascii_lowercase, 1))
    returnString = ""
    #If the number is between 1-26, return the proper letter
    if(number<=26):
        returnString = numberToLetter[number]
    #Else subtract 26 and add a 'a' to the return string. Repeat till the remaining number is between 1-26 and return the string
    else:
        while(number>26):
            returnString = returnString+'a' #Like this way due to how excel columns work
            number = number-26
            if(number<=26):
                returnString = returnString+numberToLetter[number]
    return(returnString)

#Starts code
if __name__ == '__main__':            
    groupListGenerator()