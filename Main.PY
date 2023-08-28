# Author: Nyla Gaston
# Student ID:004928444
# Title: WGUPS Project
# Submission 1: 8/24/2023

import csv
import datetime

#import HashTable.PY


#Loading the CSV files
with open("CSVFiles/addressCSV.csv") as addyCSV:
    AddressCSV = csv.reader(addyCSV)
    AddressCSV = list(AddressCSV)
with open("CSVFiles/distanceCSV.csv") as disCSV:
    DistanceCSV = csv.reader(disCSV)
    DistanceCSV = list(DistanceCSV)   

#Creating the hash table
#Source: W-1_ChainingHashTable_zyBooks_Key-Value.py
class HashTableWChains:
    def __init__(self, initialcapacity=40):
        self.table = []
        for i in range(initialcapacity):
            self.table.append([])

    #Inserts a new item into the hash table and will update an item in the list already
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #update key if it is already in the bucket
        for kv in bucket_list:
            #print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True
        #if not in the bucket, insert item to the end of the list    
        key_value = [key, item]
        bucket_list.append(key_value)
        return True
    #Searches the hash table for an item with the matching key
    #Will return the item if founcd, or None if not found
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #print(bucket_list)
        #search key in bucket
        for kv in bucket_list:
            #print(key_value)
            if kv[0] == key:
                return kv[1]  #value
        return None 
        
    #Removes an item with matching key from the hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #removes the item if it is present
        if key in bucket_list:
            bucket_list.remove(key)

#where the criteria needed for/about the package is stored    
class Packages:
    def __init__(self, ID, street, city, state, zip,deadline,weight, notes, status,departureTime,deliveryTime):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departureTime = None #departureTime
        self.deliveryTime = None #deliveryTime

    def __str__(self):
        return "ID: %s, %-20s, %s, %s,%s, Deadline: %s,%s,%s,Departure Time: %s,Delivery Time: %s" % (self.ID, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status, self.departureTime, self.deliveryTime)   
    #This method will update the status of a package depending on the time entered
    def statusUpdate(self, timeChange):
        if self.deliveryTime == None:
            self.status = "At the hub"
        elif timeChange < self.departureTime:
            self.status = "At the hub"   
        elif timeChange < self.deliveryTime:
            self.status = "En route"     
        else:
            self.status = "Delivered" 
        if self.ID == 9:          #will change the address for package 9 to the correct address once it's been received
            if timeChange > datetime.timedelta (hours=10, minutes= 20):
                self.street = "410 S State St"  
                self.zip = "84111"  
            else:
                self.street = "300 State St"
                self.zip = "84103"     



    #Creating the Packages with info from the CSV to go into the Hash Table
def loadPackageData(filename):
    with open(filename) as packagess:
        packageInfo = csv.reader(packagess,delimiter=',')
        next (packageInfo)
        for package in packageInfo:
            pID = int(package[0])
            #print(pID)
            pStreet = package[1]
            #print(pStreet)
            pCity = package[2]
            #print(pCity)
            pState = package[3]
            #print(pState)
            pZip = package[4]
            #print(pZip)
            pDeadline = package[5]
            #print(pDeadline)
            pWeight = package[6]
            #print(pWeight)
            pNotes = package[7]
            #print(pNotes)
            pStatus = "At the Hub"
            pDepartureTime = None
            pDeliveryTime = None

            #Inserting Package info into the hash
            p = Packages(pID, pStreet, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus, pDepartureTime, pDeliveryTime)
            #print (p)
            packageHash.insert(pID, p)

#Hash table for the packages
packageHash = HashTableWChains() 


#the requirements to create a truck
class Trucks:
    def __init__(self, speed, miles, currentLocation, departTime, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packages = packages

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.speed, self.miles, self.currentLocation, self.time, self.departTime, self.packages)

#finds the minimum distance for the next address
def addresss(address):
    for row in AddressCSV:
        if address in row[2]:
           return int(row[0])


#finds the distance between two addresses
def Betweenst(addy1,addy2):
    distance = DistanceCSV[addy1][addy2]
    if distance == '':
        distance = DistanceCSV[addy2][addy1]
    return float(distance)


#pulls data from CSV into the function
loadPackageData('CSVFiles/packageCSV.csv')

#manually loading the trucks and assigning them a departure time
truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),[1,13,14,15,16,19,20,27,29,30,31,34,37,40])
truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),[2,3,4,5,9,18,26,28,32,35,36,38])
truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),[6,7,8,10,11,12,17,21,22,23,24,25,33,39])


#algorithm to deliver the packages on the truck
def truckDeliverPackages(truck):
    print("Hello!")
    #creates a list for all the packages that need to be delivered
    enroute = []
    #puts packages from the hash table into the enroute list
    for packageID in truck.packages:
        package = packageHash.search(packageID)
        enroute.append(package)

    truck.packages.clear()
    #while there are packages left to be delivered the algorithm will run
    while len(enroute) > 0:
        nextAddy = 2000
        nextPackage = None
        for package in enroute:
            if package.ID in [25, 6]:
                nextPackage = package
                nextAddy = Betweenst(addresss(truck.currentLocation), addresss(package.street))
                break
            if Betweenst(addresss(truck.currentLocation), addresss(package.street)) <= nextAddy:
                nextAddy = Betweenst(addresss(truck.currentLocation), addresss(package.street))
                nextPackage = package
        truck.packages.append(nextPackage.ID)    
        enroute.remove(nextPackage)
        truck.miles += nextAddy
        truck.currentLocation = nextPackage.street
        truck.time += datetime.timedelta(hours=nextAddy / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departTime

     
        #enroute.remove(nextPackage)
        #print(nextPackage.street)
                      
    

#Actually calls the trucks to leave to being delivering packages
truckDeliverPackages(truck1)
truckDeliverPackages(truck3)
#ensures truck 2 won't leave until either truck 1 or 2 have returned
truck2.departTime = min(truck1.time, truck3.time)
truckDeliverPackages(truck2)

#title
print("Western Governors University Parcel Service")
#total miles for all of the trucks
print ("The overall miles are:", (truck1.miles + truck2.miles + truck3.miles))

while True:
    
    #print(truck1.miles + truck2.miles + truck3.miles)
    #pazzazz
    userTime = input("Please enter a time for which you'd like to see the status of each package. Format: HH:MM. ")
    (h, m) = userTime.split(":")
    timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
    try:
        singleEntry = [int(input("Enter the Package ID or nothing at all."))]
    except ValueError:
        singleEntry =  range(1, 41)
    for packageID in singleEntry:
        package = packageHash.search(packageID)
        package.statusUpdate(timeChange)
        print(str(package))                    
          
#Sincerely: Nyla Gaston