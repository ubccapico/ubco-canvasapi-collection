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
def getAssignments(courseID):
    assignments = []
    page = 1
    while True:
        request_url = url + '/courses/' + str(courseID) + '/assignments'
        params = {"per_page": str(per_page), "page": str(page)}
        r = requests.get(request_url, headers=auth_header, params=params)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            break
        assignments += data
        page+=1
        if len(assignments) == 0:
            print("No students found to report on.")
            exit()
    return assignments

def getAssignmentSubmission(courseID, assignmentID):
    assignments = []
    page = 1
    while True:
        request_url = url + '/courses/' + str(courseID) + '/assignments/' + str(assignmentID) + '/submissions'
        params = {"per_page": str(per_page), "page": str(page), 'include[]': ['submission_comments', 'user']}
        r = requests.get(request_url, headers=auth_header, params=params)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            break
        assignments += data
        page+=1
        if len(assignments) == 0:
            print("No students found to report on.")
            exit()
    return assignments   

def getCourseDetails(courseID):
    courseDetails = requests.get(url + '/courses/' + str(courseID),
                                 headers = {'Authorization': 'Bearer ' + token})
    return courseDetails.json()
	
def getCourseStudents(courseID):
    courseStudents = []
    page = 1
    while True:
        request_url = url + '/courses/' + str(courseID) + '/users'
        params = {"per_page": str(per_page), "page": str(page), 'enrollment_type': 'student'}
        r = requests.get(request_url, headers=auth_header, params=params)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            break
        courseStudents += data
        page+=1
        if len(courseStudents) == 0:
            print("No students found to report on.")
            exit()
    return courseStudents
