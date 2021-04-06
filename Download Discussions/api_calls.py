# -*- coding: utf-8 -*-
 
#library needed for api calls
import requests
from configparser import ConfigParser

#read url and token from config file
config = ConfigParser()
config.read('canvas.cfg')
environment = config['default']['env']
url = config[environment]['url']
token = config[environment]['token']
auth_header = {'Authorization': 'Bearer ' + token}
per_page = 100
    
#api calls
def getCourseDetails(courseID):
    courseDetails = requests.get(url + '/courses/' + str(courseID),
                                 headers = {'Authorization': 'Bearer ' + token})
    return courseDetails.json()

def getCourseStudents(courseID):
    students = []
    page = 1
    while True:
        request_url = url + '/courses/' + str(courseID) + '/users'
        params = {"per_page": str(per_page), "page": str(page), 'enrollment_type': 'student', 'include[]': 'enrollments'}
        r = requests.get(request_url, headers=auth_header, params=params)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            break
        students += data
        page+=1
        if len(students) == 0:
            print("No students found to report on.")
            exit()
    return students

def getSingleTopic(courseID, topicID):
    request_url = url + '/courses/' + str(courseID) + '/discussion_topics/' + str(topicID) + '/view'
    r = requests.get(request_url, headers=auth_header)
    r.raise_for_status()
    data = r.json() 
    return(data)