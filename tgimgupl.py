#!/usr/bin/env python3

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

## This is the copy of this util: https://github.com/rekcuFniarB/TgImgUpl#readme

import requests, sys, os

info = '''
Usage:
    tgimgupl image_file

Tgimgupl © 2018  BrainFucker
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome
to redistribute it under certain conditions.
'''

class conf:
    domain = 'https://telegra.ph'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Referer': os.path.join(domain, ''),
        }
    uplurl = os.path.join(domain, 'upload');

    types = {
        'png':  'image-/png',
        'jpg':  'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif':  'image/gif',
        'svg':  'image/svg+xml',
        #'ogg':  'application/ogg',
        #'mp3':  'audio/mpeg',
        #'txt':  'text/plain',
        #'html': 'text/html'
    }

class UploadError(BaseException):
    pass

sys.path.insert(0, os.path.join(os.path.expanduser('~'), '.config', 'tgimgupl'))

try:
    ## Override config with local version if exists
    import localconf
    for key in localconf.__dict__.keys():
        if not '__' in key:
            setattr(conf, key, localconf.__dict__[key])
except ModuleNotFoundError:
    pass

def err(msg):
    sys.stderr.write(f'{msg}\n')

def getType(filename):
    _f = filename.split('.')
    ext = _f[len(_f) - 1].lower()
    if ext in conf.types:
        return conf.types[ext]
    else:
        raise UploadError(f'Unsupported filetype {ext}')

def upload(filePath):
    '''Uploads file'''
    if not os.path.exists(filePath):
        raise UploadError(f'File "{filePath}" does not exist.')
    
    filename = os.path.basename(filePath)
    ## replace non ascii chars with '?' otherwise upload fails
    ascii_filename = filename.encode('ascii', 'replace').decode('utf-8')
    filetype = getType(filename)
    fileToUpl = {'file': (ascii_filename, open(filePath, 'rb'), filetype)}
    r = requests.post(conf.uplurl, files=fileToUpl, headers=conf.headers)
    if r.ok:
        result = r.json()
        if type(result) is list:
            return {'base': conf.headers['Referer'], 'src': result[0]['src']}
        elif type(result) is dict:
            if 'error' in result:
                err('Error: %s' % result['error'])
                raise UploadError(result['error'])
            else:
                raise UploadError(result)
        else:
            raise UploadError(result)
    else:
        raise UploadError(r)


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
    
    try:
        result = upload(sys.argv[1])
        print(os.path.join(result["base"].strip('/'), result["src"].strip('/')))
    except BaseException as e:
        err(f'ERROR: {e}')
        sys.exit(1)
