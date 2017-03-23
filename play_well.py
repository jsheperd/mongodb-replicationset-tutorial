#!/usr/bin/env python

dbs = {'10.0.0.1': {'status': 'needed', 'name': 'db01'},
       '10.0.0.2': {'status': 'needed', 'name': 'db02'},
       '10.0.0.3': {'status': 'needed', 'name': 'db03'}}

import os, sys, time

##### Check the Network

def isActive(ip, ip_addr):
    return len([row for row in ip_addr if ip in row])

def isNetOk():
    current_interfaces = os.popen("ip addr").readlines()
    for ip in dbs.keys():
        if isActive(ip, current_interfaces):
            dbs[ip]['status'] = "UP"
        else:
            return False
    return True

if isNetOk():
    print "# Net is OK"
else:
    print "# Set UP the interfaces as root by: sudo ./prepare_network.sh"

##### End of the Network Check out
##### Database clean up

print "# Set up the mongods"
clean = raw_input("Would you like to clear the current databases ? Y/[N]:  ")
if 'y' in clean.lower():
    for db in dbs.keys():
        print "cleaning %s" % dbs[db]['name']
        print "rm -rf data/%s/*" % dbs[db]['name']
        os.system("rm -rf data/%s/*" % dbs[db]['name'])

print "# Cleaning out the db folders to start with a blank state"

##### End of Database clean up
##### Starting the databases

for db in dbs.keys():
    print "start mongod %s" % dbs[db]['name']
    print "mongod --config %s.config" % dbs[db]['name']
    os.system("mongod --config %s.config &" % dbs[db]['name'])

##### We have three running mongod instance now
##### Kill our mongod instances

time.sleep(2)
print " IT is time to play with your instances "
time.sleep(2)

print "# Kill the mongods"
clean = raw_input("Would you like kill the running mongods? Y/[N]:  ")
if 'y' in clean.lower():
    print os.popen("killall mongod").readlines()

##### End of cleaning






