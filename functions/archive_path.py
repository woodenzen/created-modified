# #!/usr/bin/env python3
# # encoding: utf-8

from urllib.parse import urlparse
import os, pathlib
from plistlib import load
    
def TheArchivePath():
#  Variables that ultimately revel The Archive's plist file.
    bundle_id = "de.zettelkasten.TheArchive"
    team_id = "FRMDA3XRGC"
    #`fileName` is the path to the plist file that contains the path to the ZK.
    fileName = os.path.expanduser(
        "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
    with open(fileName, 'rb') as fp:
        # load is a special function for use with a plist
        pl = load(fp) 
        # 'archiveURL' is the key that pairs with the zk path
        path = urlparse(pl['archiveURL']) 
    # path is the part of the path that is formatted for use as a path.
    return (path.path) 

if __name__ == "__main__":
    zettelkasten = pathlib.Path(TheArchivePath())
    print(f'The Current ZK Directory. {zettelkasten}')