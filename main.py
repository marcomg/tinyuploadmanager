#!/usr/bin/python3

########################################################################
# This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.#
#                                                                      #
# Copyright (C) 2014 by marcomg                                        #
########################################################################

# From std library
import argparse
import os

# From mglibrary
import libhjsplit

# From local library
import thinyuploadmanagerlib

# @var float The version of the program
VERSION = 1.0;

argParse = argparse.ArgumentParser(description='A program to upload big files to tinyupload.com', prog='thiniuploadmanager')
argParse.add_argument('-v', '--version', action='version', version='%(prog)s version ' + str(VERSION))
argParse.add_argument('command', action='store', type=str, help='The possibily commands are upload or download');
argParse.add_argument('-f', '--file', action='store', type=str, help='the file to upload or the database file')
args = argParse.parse_args()

if args.command == 'upload':
    # Pass 1 split files
    print('Splitting files, please wait...')
    try:
        libhjsplit.split(args.file, 10 * 1000000)
        #libhjsplit.split(args.file, 100000)
    except TypeError:
        print('ALERT: You must use the -f argument to select the file to upload!')
        exit()
    # Pass 2 upload file
    print('Uploading files, please wait...')
    i = 1
    uploadedLinks = []
    while True:
        try:
            fileToUpload = args.file + str('.%03d' % (i))
            result = thinyuploadmanagerlib.upload(fileToUpload)
            uploadedLinks.append(result)
            print('\tuploaded file %s' % (fileToUpload))
            i += 1
        except FileNotFoundError:
            break
        except ResourceWarning:
            print('\tALERT: Error during upload %s...' % (fileToUpload))
    
    # Pass 3 clean tmp files
    print('Cleaning tmp files, please wait...')
    for f in range(1, i):
        delfile = args.file + str('.%03d' % (f))
        try:
            os.remove(delfile)
        except FileNotFoundError:
            print('ALERT: file %s not found, you have already deleted it?' % (delfile))
    
    # Pass 4 print links
    print('Writing a file containing links to download (tum.db):')
    with open('tum.db', 'w') as db:
        for link in uploadedLinks:
            db.write(link + '\n')
    print('\tdone.')
elif args.command == 'download':
    print('Reading the database, please wait...')
    try:
        with open(args.file, 'r') as db:
            tmp = db.readlines()
            urls = []
            for t in tmp:
                urls.append(t.rstrip('\n'))
            del t, tmp
    except FileNotFoundError:
        print('ALERT: The database %s esists?' % (args.file))
    downloaded_files = []
    print('Downloading files, please wait...')
    for url in urls:
        try:
            download = thinyuploadmanagerlib.download(url)
            downloaded_files.append(download)
            print('\tdownloaded file %s' % (download))
        except ResourceWarning:
            print('ALERT: Problems during download %s' % (url))
            exit()
    
    print('Joining files, please wait...')
    libhjsplit.join(downloaded_files[0])
    
    print('Cleaning tmp files, please wait...')
    for delfile in downloaded_files:
        try:
            os.remove(delfile)
        except FileNotFoundError:
            print('ALERT: file %s not found, you have already deleted it?' % (delfile))
else:
    print('Fatal error: command "%s" does not recognized, show --help for more details' % (args.command))