#!/bin/bash

rsync -av --progress  --exclude='.DS_Store' /Users/damjan/Photoshooting/publish/ damjan@cvetan.si:/var/www/hosting/svstefan.si/download/