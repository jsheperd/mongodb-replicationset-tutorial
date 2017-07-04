#!/bin/bash

# Create some new interfaces to run the instances on different ip adresses
ifconfig lo:1 10.0.0.1/24
ifconfig lo:2 10.0.0.2/24
ifconfig lo:3 10.0.0.3/24
ifconfig lo:4 10.0.0.4/24
