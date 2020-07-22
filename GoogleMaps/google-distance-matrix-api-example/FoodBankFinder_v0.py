#@author: @alexparial
#By: Alex Parial
#Purdue Class of 2021
#aparial3.ap@gmail.com

#FoodBankFinder
#Explanation of code:
#v0 hardcoded in origin address and destination addresses

#Future versions
#Take input from 


import urllib.request
import json

file = open('key.txt', 'r')
key = file.read().strip()

# origin = '111+Monument+Circle+Indianapolis+IN+46204'

def closestBank(origin):
    origin = origin.replace(" ", "+")

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
            ).format(origin, a.replace("", "+"), key)

        response = urllib.request.urlopen(url)

        response_json = json.loads(response.read())

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
            closestdist=distance_meters
            best = 0
        else:
            if distance_minutes < besttime:
                besttime=distance_minutes
                closestdist= distance_meters
                best = count
        count = count+1
    
    return (destinations[best].replace("+"," "),names[best], round(besttime,2),closestdist)

# print("Recommendation:\nOrigin: %s\nDestination: %s\nFood Bank: %s\nDistance (Minutes): %s\n"
 #        % (origin.replace("+"," "), destinations[best].replace("+"," "),names[best], round(besttime,2)))

