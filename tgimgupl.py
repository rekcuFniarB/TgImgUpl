#!/usr/bin/env python3.5

##  Tgimgupl: upload images to telegra.ph from command line.
##  Copyright (C) 2018  BrainFucker <retratserif@gmail.com>
##  
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.

import requests, sys, os

info = '''
Usage:
    tgimgupl image_file

Tgimgupl © 2018  BrainFucker
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome
to redistribute it under certain conditions.
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/57.0',
    'Referer': 'http://telegra.ph/',
    }

uplurl = 'http://telegra.ph/upload'

types = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'svg': 'image/svg+xml',
    #'ogg': 'application/ogg',
    #'mp3': 'audio/mpeg',
    #'txt': 'text/plain',
    #'html': 'text/html'
    }

def err(msg):
    sys.stderr.write('%s\n' % msg)

def getType(filename):
    _f = filename.split('.')
    ext = _f[len(_f) - 1].lower()
    if ext in types:
        return types[ext]
    else:
        err('Unsupported filetype %s.' % ext)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        err('Error: no file specified.')
        err(info)
        sys.exit(1)

    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        ## show help
        err(info)
        sys.exit(0)

    if len(sys.argv) > 2:
        err('Error: batch mode not supported.')
        err(info)
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        err('File %s not found.' % sys.argv[1])
        sys.exit(1)

    filename = os.path.basename(sys.argv[1])
    filetype = getType(filename)
    fileToUpl = {'file': (filename, open(sys.argv[1], 'rb'), filetype)}
    r = requests.post(uplurl, files=fileToUpl, headers=headers)
    if r.ok:
        result = r.json()
        if type(result) == list:
            ## print link to uploaded image to stdout
            print('%s%s' % (os.path.dirname(headers['Referer']), result[0]['src']))
        elif type(result) == dict:
            if 'error' in result:
                err('Error: %s' % result['error'])
            else:
                err(result)
                sys.exit(1)
        else:
            err('Unknown error')
            sys.exit(2)
