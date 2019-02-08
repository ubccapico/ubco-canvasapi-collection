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

def getCourseDetails(courseID):
    courseDetails = requests.get(url + '/courses/' + str(courseID),
                                 params = {'include': 'total_students'},
                                 headers = {'Authorization': 'Bearer ' + token})
    return courseDetails.json()

def getCourseStudents(courseID):
    student_set = []
    courseStudents = requests.get(url + '/courses/' + str(courseID) + '/users?per_page=50',
                                  params = {'enrollment_type': 'student'},
                                  headers = {'Authorization': 'Bearer ' + token})
    
    rawCourseStudents = courseStudents.json()
    for student in rawCourseStudents:
        student_set.append(student)
        
    while courseStudents.links['current']['url'] != courseStudents.links['last']['url']:
        courseStudents = requests.get(courseStudents.links['next']['url'],
                                      headers = {'Authorization': 'Bearer ' + token})
        
        rawCourseStudents = courseStudents.json()
        for student in rawCourseStudents:
            student_set.append(student)
            
    return student_set
    