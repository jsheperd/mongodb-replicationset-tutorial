#!/bin/bash

# start three instances to shape a replicationset
mongod --config db01.config &
mongod --config db02.config &
mongod --config db03.config &
