tinyuploadmanager
=================

tinyuploadmanager: a shell program to download and upload big files on tinyupload.com

# How download #
First download this repository, then you need to download the libhjsplit library form _openhjsplit_ [here] (https://raw.githubusercontent.com/marcomg/openhjsplit/master/libhjsplit.py).

# How install #
On GNU/Linux copy the _main.py_ in _/usr/local/bin_ directory with excutable permissions as tum (or the name you want) and the two libraries (libhjsplit.py and thinyuploadmanagerlib.py) in _/usr/local/lib/python3.4_ (or another version you use of python3) *make sure you have compiled the libraries!*

# How use #
To use the program enter in the directory where you want to work and do this to upload a big file:
    tum upload -f yourFile/inDirectory/f.extension
It will be split (in the same directory where it is) and it is prompt what happen (if there is an error during upload the program will try until the operation has success).
After the upload it will be created a file called tum.db containing all links to download the file (it is a text database and you can open it with kate or another text editor to a manual download) and the temporaney files will be removed.

To download a file:
    tum download -f yourDir/tum.db
The program will download every file, join them and remove the temporaney files. All files are created in the working directory.
