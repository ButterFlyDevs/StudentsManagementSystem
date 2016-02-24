#!/bin/bash
echo "Downloading the Google App Engine SDK"
curl -O https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.30.zip
echo "Unzip SDK"
unzip google_appengine_1.9.30.zip 
echo "Deleting .zip"
rm google_appengine_1.9.30.zip 
