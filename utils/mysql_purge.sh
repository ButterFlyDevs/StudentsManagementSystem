#!/usr/bin/env bash

# Script to delete all about mysql if some problem appear.

sudo apt-get remove --purge mysql*
sudo apt-get autoremove
sudo apt-get autoclean