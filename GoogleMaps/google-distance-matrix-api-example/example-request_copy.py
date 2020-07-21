# [START imports]
import urllib.request
import json



import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

file = open('key.txt', 'r')
key = file.read().strip()


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)

class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        origin = self.request.get('Origin',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

''' idek what this is oops
class MyHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
# <input name="name" type="text" />

'''

origin = self.request.get("Origin")




#origin = '111+Monument+Circle+Indianapolis+IN+46204'
destinations = ['1435+North+Illinois+Street+Indianapolis+IN+46202','701+North+Delaware+Street+Indianapolis+IN+46204', \
'952+North+Pennsylvania+Street+Indianapolis+IN+46204','964+North+Pennsylvania+Street+Indianapolis+IN+46204', \
'2325+East+New+York+Street+Indianapolis+IN+46201']
names = ['Catholic Charities Crisis Office','Central Christian Church','Metro Baptist Center', \
'Hoosier Veterans Assistance Foundation','Westminster Neighborhood Services']
count = 0

for a in destinations: 
    url = ('https://maps.googleapis.com/maps/api/distancematrix/json'
        + '?language=en-US&units=imperial'
        + '&origins={}'
        + '&destinations={}'
        + '&key={}'
        ).format(origin, a, key)

    response = urllib.request.urlopen(url)

    response_json = json.loads(response.read())

    #print("%s \n" %(response_json))

    distance_meters = response_json['rows'][0]['elements'][0]['distance']['value']
    distance_minutes = response_json['rows'][0]['elements'][0]['duration']['value'] / 60
    printorigin = origin.replace("+"," ")
    destination = a.replace("+"," ")
    '''
    print("Origin: %s\nDestination: %s\nFood Bank: %s\nDistance (Meters): %s\nDistance (Minutes): %s\n"
        % (printorigin, destination,names[count], distance_meters, round(distance_minutes,2)))
    '''
    if not count:
        besttime = distance_minutes
        best = 0
    else:
        if distance_minutes < besttime:
            besttime=distance_minutes
            best = count
    count = count+1

print("Recommendation:\nOrigin: %s\nDestination: %s\nFood Bank: %s\nDistance (Minutes): %s\n"
        % (origin.replace("+"," "), destinations[best].replace("+"," "),names[best], round(besttime,2)))

