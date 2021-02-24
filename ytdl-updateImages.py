#!/usr/bin/python3
# a simple script to download video thumbnails from
# youtube-dl JSON data

import os, json, subprocess

# read files
allfiles = os.listdir()
# separate json files
jsonfiles = [ f for f in allfiles if f.endswith( '.json' )]
# separate jpeg files
jpegfiles = [ f for f in allfiles if f.endswith( '.jpg' )]
# iterate through json files downloading thumbnails if they do not already exist
count = 0
suffix = 's'
for f in jsonfiles :
    j = json.loads( open( f, 'r' ).read())
    thumb = j['thumbnail'].split( '/' )[-1]
    if thumb in jpegfiles :
        print( 'already have ' + thumb + ', skipping')
    else :
        subprocess.run([ 'wget', j['thumbnail'] ] )
        count = count + 1

if count == 1 :
    suffix = ''

print( 'retrieved ' + str( count ) + ' image' + suffix + '\n' )



