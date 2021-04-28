#Made by William O'Keefe 
#For COMP 593
#Downloads NASA's picture of the day and makes it your background.
#To create the database used here you would use a statement like this:
#CREATE TABLE "imgdata" (
	#"Filename"	TEXT NOT NULL,
	#"Filesize"	TEXT NOT NULL,
	#"Date"	TEXT NOT NULL UNIQUE,
	#"Time"	TEXT NOT NULL,
	#"Hash"	INTEGER NOT NULL
#)

from http import client
import json
import sqlite3
import urllib.request
import os
import time


# the url with the api key
url = 'https://api.nasa.gov/planetary/apod?api_key=sBWOxwro6cszaxIoFrceVfKjNh9YBDAPZSlJuqyf'

# connect to NASA and wait for a response
ttc = client.HTTPSConnection('api.nasa.gov', 443)
ttc.request("GET", url)
respond = ttc.getresponse()

# check the response to see if something bad happened.
if respond.status is 200:
  print('Response:',respond.status, '🧨🧨🧨', '\n')
else:
  print('shite',respond.status)

# read and decode the response JSON string
Jsonrespo = respond.read().decode()
Pages = json.loads(Jsonrespo)
print (Pages['title'])

#create picture directory if it doesn't exist
image_dir = "Space_Images_1"
dir_res = os.path.exists(image_dir)
if (dir_res==False):
    os.makedirs(image_dir)

#download the picture.
urllib.request.urlretrieve(Pages['hdurl'], 'Space_Images_1/' + Pages['date'] + '.jpg')

#take the information and cram it into the api
myConnection = sqlite3.connect('stupiddb.db')
myCursor = myConnection.cursor()

addINFOQuery = """INSERT INTO imgdata (Filename, 
                      Filesize, 
                      Date, 
                      Time, 
                      Hash)                      
                  VALUES (?, ?, ?, ?, ?);"""

theinfo = (Pages['title'],
           os.path.getsize('Space_Images_1/' + Pages['date'] + '.jpg'),
           Pages['date'],
           time.strftime("%H:%M:%S"),
           hash('Space_Images_1/' + Pages['date'] + '.jpg'))

# set the changes in motion and then commit them.
myCursor.execute(addINFOQuery, theinfo)

myConnection.commit()
myConnection.close()

#the powershell file has to be executed it just changes your background in the registry.
execfile('module2.ps1')