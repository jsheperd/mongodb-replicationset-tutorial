#!/bin/bash
xterm -hold -e 'mongod --config db01.config' &
xterm -hold -e 'mongod --config db02.config' &
xterm -hold -e 'mongod --config db03.config' &
