#!/bin/bash

# Create some new interfaces to run the instances on different ip adresses
ifconfig lo:1 127.0.0.11/24
ifconfig lo:2 127.0.0.12/24
ifconfig lo:3 127.0.0.13/24
