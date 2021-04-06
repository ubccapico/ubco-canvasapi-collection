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

def getCourseSections(courseID):
    sections = []
    page = 1
    while True:
        request_url = url + '/courses/' + str(courseID) + '/sections'
        params = {"per_page": str(per_page), "page": str(page)}
        r = requests.get(request_url, headers=auth_header, params=params)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            break
        sections += data
        page+=1
        if len(sections) == 0:
            print("No students found to report on.")
            exit()
    return sections

def getGroupCategory(courseID):
    groupSet = []
    page = 1
    while True:
        request_url = url + '/courses/' + str(courseID) +'/group_categories'
        params = {"per_page": str(per_page), "page": str(page)}
        r = requests.get(request_url, headers=auth_header, params=params)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            break
        groupSet += data
        page+=1
        if len(groupSet) == 0:
            print("No students found to report on.")
            exit()
    return groupSet

def getGroups(groupCategoryID):
    group = []
    page = 1
    while True:
        request_url = url + '/group_categories/' + str(groupCategoryID) + '/groups'
        params = {"per_page": str(per_page), "page": str(page), '"followed_by_user"': 'True'}
        r = requests.get(request_url, headers=auth_header, params=params)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            break
        group += data
        page+=1
        if len(group) == 0:
            print("No students found to report on.")
            exit()
    return group

def getGroupMembers(courseID, groupID):
    groupMembers = []
    page = 1
    while True:
        request_url = url + '/groups/' + str(groupID) + '/memberships'
        params = {"per_page": str(per_page), "page": str(page)}
        r = requests.get(request_url, headers=auth_header, params=params)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            break
        groupMembers += data
        page+=1
        if len(groupMembers) == 0:
            print("No students found to report on.")
            exit()
    return groupMembers

def getUnassignedGroup(groupCategoryID):
    unassignedGroup = []
    page = 1
    while True:
        request_url = url + '/group_categories/' + str(groupCategoryID) + '/users'
        params = {"per_page": str(per_page), "page": str(page), 'unassigned': 'True'}
        r = requests.get(request_url, headers=auth_header, params=params)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            break
        unassignedGroup += data
        page+=1
        if len(unassignedGroup) == 0:
            print("No students found to report on.")
            exit()
    return unassignedGroup
