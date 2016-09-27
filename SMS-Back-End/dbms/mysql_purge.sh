#!/usr/bin/env bash

# Script to delete all about mysql if some problem is found.

sudo apt-get remove --purge mysql*
sudo apt-get autoremove
sudo apt-get autoclean