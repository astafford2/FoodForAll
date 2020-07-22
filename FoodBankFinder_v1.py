#@author: @alexparial
#By: Alex Parial
#Purdue Class of 2021
#aparial3.ap@gmail.com

#FoodBankFinder
#Explanation of code:
#v0 hardcoded in origin address and destination addresses
#v1 addresses from separate csv and html file allows for origin input

#Future versions
#Take input from 
#https://youtu.be/ub82Xb1C8os

import urllib.request
import json
import csv
from csv import reader


file = open('key.txt', 'r')
key = file.read().strip()

# origin = '111+Monument+Circle+Indianapolis+IN+46204'

def closestBanks(origin):
    address_arr = []
    dist_arr = []
    time_arr = []
    origin = origin.replace(" ", "+")

    with open('FoodBank Addresses.csv', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in data:
            a = ('+'.join(row))
            a = a.replace(",","")
            
            url = ('https://maps.googleapis.com/maps/api/distancematrix/json'
                + '?language=en-US&units=imperial'
                + '&origins={}'
                + '&destinations={}'
                + '&key={}'
                ).format(origin, a, key)
            response = urllib.request.urlopen(url)
            response_json = json.loads(response.read())

            distance_meters = response_json['rows'][0]['elements'][0]['distance']['value']
            distance_miles = round((distance_meters*0.000621371), 2)
            distance_minutes = response_json['rows'][0]['elements'][0]['duration']['value'] / 60
            distance_minutes = round(distance_minutes, 2)
            printorigin = origin.replace("+"," ")
            destination = a.replace("+"," ")
            address_arr.append(a)
            dist_arr.append(distance_miles)
            time_arr.append(distance_minutes)

    #print("%s\n %s\n %s\n %s\n"%(printorigin, bestbank.replace('"',''),bestdist,round(besttime,2)))

    #meant to be top5 of each respective result
    toptime_arr = [] #time
    topdist_arr = [] #distance
    topadd_arr = [] #address
    topname_arr = [] #name
    topnum_arr = [] #phone number
    topdesc_arr = [] #description

        
    for x in range(5):
        besttime = min(time_arr)
        index = time_arr.index(besttime)
        bestbank = address_arr[index]
        bestdist = dist_arr[index]

        toptime_arr.append(besttime)
        time_arr.remove(time_arr[index])
        topdist_arr.append(bestdist)
        dist_arr.remove(dist_arr[index])
        topadd_arr.append(bestbank)
        address_arr.remove(address_arr[index])

        bestbank = bestbank.replace("+", " ")
        bestbank = bestbank.replace('"', '')

        with open("FoodBank Info.csv") as csvfile2:
            data2 = reader(csvfile2)
            for row2 in data2:
                if row2[1] == bestbank:
                    topname_arr.append(row2[0])
                    topnum_arr.append(row2[2])
                    topdesc_arr.append(row2[3])

    for addr in topadd_arr:
        addr = addr.replace("+", " ")


    return topname_arr, topadd_arr, topnum_arr, topdesc_arr, topdist_arr, toptime_arr