#!/usr/bin/python3
# a simple script to download video thumbnails from
# youtube-dl JSON data

import binascii, json, os, pathlib, subprocess

# a config.  This should set defaults and then read in a JSON file: ~/.config/bb/config
# for now it is static
class Config( dict ) :
    def __init__( self ) :
        self['root'] = '/home/tsingi/Videos/bitchute/channels'
        self['getJson'] = [ 'youtube-dl', '-i', '--write-info-json', '--skip-download' ]

class JsonFile( dict ) :
    def __init__( self, path ) :
        self.filepath = path
        js = json.loads( self.filepath.open().read())
        self.update( js )

# for the file name "Groupon--yABgb7HW3M.info.json" the file id is '-yABgb7HW3M'
# I hate this, dashes are delimiters and also allowed in variable length identifiers.
class Video( dict ) :
    def __init__( self, path ) :
        self['path'] = path
        tok = self['path'].as_posix().split( '-' )
        thistok = -1
        ident = tok[thistok][:-4] # drop ".mp4"
        while len( ident ) < 11 : # this hack works on all identifiers so far but it WILL fail eventually
            thistok = thistok - 1
            ident = tok[thistok] + '-' + ident
        self['id'] = ident

class Channel :
    def __init__( self, directory ) :
        self.directory = directory
        self.jsonPath = self.directory.as_posix() + '/json'
        self.videos = {} # videos in channel directory
        self.json = {} # jsonfiles in <channel>/json
        json = None
        for dirent in self.directory.glob( 'json' ) :
            for jsonfile in dirent.glob( '*.json' ) :
                jsf = JsonFile( jsonfile )
                ident = jsf['id']
                self.json[ident] = jsf
        for videopath in self.directory.glob( '*.mp4' ) :
            video = Video( videopath )
            self.videos[video['id']] = video

    def updateJson( self ) : 
        """look for videos that do not have an assosciated json file"""
        jsonPath = pathlib.Path( self.jsonPath );
        if not jsonPath.exists() :
            jsonPath.mkdir()
        elif not jsonPath.is_dir() :
            print( 'ERROR: "' + jsonPath.as_posix() + '" exists but is not a directory' )
            exit( 2 )
        os.chdir( self.jsonPath )
        # print( self.jsonPath )
        for vid in self.videos : # vid is the id, not the object
            if not vid in self.json :
                url = 'https://www.bitchute.com/video/' + vid + '/'
                print( 'retrieving json data for: ' + url )
                subprocess.run( [ 'ytdl-getJson', url ] )

class BB( list ) : # list contains channels
    def __init__( self ) :
        self.ytdlVersion = None
        try :
            data = subprocess.run( [ 'youtube-dl', '--version' ], capture_output = True )
        except:
            print( 'Could not locate youtube-dl, is it installed and in your path?' )
            exit( 1 )
        self.ytdlVersion = data.stdout.decode().split( '\n' )[0] # convert to ascii and drop trailing newline (if any)
        self.config = Config() # load config file
        root = pathlib.Path( self.config['root'] )
        for directory in root.iterdir() :
            if directory.is_dir() :
                self.append( Channel( directory ))

    def updateJson( self ) : 
        """look for videos that do not have an assosciated json file"""
        for channel in self :
            channel.updateJson()

if __name__ == '__main__' :
    bb = BB()
    bb.updateJson()





# read files
# allfiles = os.listdir()
# separate json files
# jsonfiles = [ f for f in allfiles if f.endswith( '.json' )]
# separate jpeg files
# jpegfiles = [ f for f in allfiles if f.endswith( '.jpg' )]
# iterate through json files downloading thumbnails if they do not already exist
# count = 0
# suffix = 's'
# for f in jsonfiles :
    # j = json.loads( open( f, 'r' ).read())
    # thumb = j['thumbnail'].split( '/' )[-1]
    # if thumb in jpegfiles :
        # print( 'already have ' + thumb + ', skipping')
    # else :
        # subprocess.run([ 'wget', j['thumbnail'] ] )
        # count = count + 1
# 
# if count == 1 :
    # suffix = ''
 
# print( 'retrieved ' + str( count ) + ' image' + suffix + '\n' )



