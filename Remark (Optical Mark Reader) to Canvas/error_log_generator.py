# -*- coding: utf-8 -*-

#create an error log if data within the OMR CSV file does not match a student in the course  
def logGenerator(df, errorNum, errorFName, errorLName, errorScore, errorPercent):
    
    if errorNum:
        
        #the code builds a text file with the relevant information AND prints out this information to the console
        f = open('ERROR_LOG.txt', 'w')
        f.write("The following rows did not match a student in your course: \n\n")
        
        if 'Percent Score' in df.columns:
            if 'First Name' in df.columns and 'Last Name' in df.columns:
                f.write('%-8s%-18s%-18s%-18s%-18s%-8s' % ("Row", "Student Number", "First Name", "Last Name", "Score", "Percent"))  
            else:
                f.write('%-8s%-18s%-18s%-8s' % ("Row", "Student Number", "Score", "Percent"))  
        else:
            if 'First Name' in df.columns and 'Last Name' in df.columns:
                f.write('%-8s%-18s%-18s%-18s%-18s' % ("Row", "Student Number", "First Name", "Last Name", "Score"))  
            else:
                f.write('%-8s%-18s%-18s' % ("Row", "Student Number", "Score")) 
                
        f.write('\n')
      
        print("\nERROR - The following rows did not a match a student in your course:\n")
        
        if 'Percent Score' in df.columns:
            if 'First Name' in df.columns and 'Last Name' in df.columns:
                print('%-8s%-18s%-18s%-18s%-18s%-8s' % ("Row", "Student Number", "First Name", "Last Name", "Score", "Percent"))  
            else:
                print('%-8s%-18s%-18s%-8s' % ("Row", "Student Number", "Score", "Percent"))  
        else:
            if 'First Name' in df.columns and 'Last Name' in df.columns:
                print('%-8s%-18s%-18s%-18s%-18s' % ("Row", "Student Number", "First Name", "Last Name", "Score"))  
            else:
                print('%-8s%-18s%-18s' % ("Row", "Student Number", "Score")) 
        
        for number in range(0, len(errorNum)):
            
            studentID = errorNum[number]
            
            if studentID != studentID:
                rowNum = "N/A"
            else:
                rowNum = df.loc[df['Student ID']== studentID].index[0] + 2
                
            if 'Percent Score' in df.columns:
                if 'First Name' in df.columns and 'Last Name' in df.columns:
                    print('%-8s%-18s%-18s%-18s%-18s%-8s' % (str(rowNum), str(int(errorNum[number])), str(errorFName[number]), str(errorLName[number]), str(errorScore[number]), str(errorPercent[number])))
                else:
                    print('%-8s%-18s%-18s%-2s' % (str(rowNum), str(int(errorNum[number])), str(errorScore[number]), str(errorPercent[number])))
                
                if 'First Name' in df.columns and 'Last Name' in df.columns:
                    f.write('%-8s%-18s%-18s%-18s%-18s%-8s' % (str(rowNum), str(int(errorNum[number])), str(errorFName[number]), str(errorLName[number]), str(errorScore[number]), str(errorPercent[number])))
                else:
                    f.write('%-8s%-18s%-18s%-8s' % (str(rowNum), str(int(errorNum[number])), str(errorScore[number]), str(errorPercent[number])))
            else:
                if 'First Name' in df.columns and 'Last Name' in df.columns:
                    print('%-8s%-18s%-18s%-18s%-18s' % (str(rowNum), str(int(errorNum[number])), str(errorFName[number]), str(errorLName[number]), str(errorScore[number])))
                else:
                    print('%-8s%-18s%-18s' % (str(rowNum), str(int(errorNum[number])), str(errorScore[number])))
                
                if 'First Name' in df.columns and 'Last Name' in df.columns:
                    f.write('%-8s%-18s%-18s%-18s%-18s' % (str(rowNum), str(int(errorNum[number])), str(errorFName[number]), str(errorLName[number]), str(errorScore[number])))
                else:
                    f.write('%-8s%-18s%-18s' % (str(rowNum), str(int(errorNum[number])), str(errorScore[number])))
                
            f.write('\n')  
        f.close()
        
        print("\nThis is likely due to an incorrect or missing student number. You can add in the grades for these students manually.")
        input("\nAn ERROR_LOG text file has been generated in the same folder as this script that contains the rows that did not match. Hit Enter to continue and a Canvas ready file will be generated that omits the rows with incorrect data: ")
    