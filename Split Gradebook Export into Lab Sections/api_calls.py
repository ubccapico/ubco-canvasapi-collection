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
    
#api calls
def getAssignmentGroups(courseID):
    group_set = []
    
    groups = requests.get(url + '/courses/' + str(courseID) + '/assignment_groups',
                          headers = {'Authorization': 'Bearer ' + token})
    
    rawGroups = groups.json()
    
    for group in rawGroups:
        group_set.append(group)
        
    while groups.links['current']['url'] != groups.links['last']['url']:
        
        groups = requests.get(groups.links['next']['url'],
                              headers = {'Authorization': 'Bearer ' + token})
        
        rawGroups = groups.json()
        
        for group in rawGroups:
            group_set.append(group)
            
    return group_set
   

def getCourseDetails(courseID):
    courseDetails = requests.get(url + '/courses/' + str(courseID),
                                 headers = {'Authorization': 'Bearer ' + token})
    return courseDetails.json()

def getCourseSections(courseID):
    section_set = []
    
    sections = requests.get(url + '/courses/' + str(courseID) + '/sections', 
                            headers = {'Authorization': 'Bearer ' + token})
    
    rawSections = sections.json()
    
    for section in rawSections:
        section_set.append(section)
    
    while sections.links['current']['url'] != sections.links['last']['url']:
        
        sections = requests.get(sections.links['next']['url'], 
                                headers = {'Authorization': 'Bearer ' + token})
        
        rawSections = sections.json()
        
        for section in rawSections:
            section_set.append(section)
                
    return section_set