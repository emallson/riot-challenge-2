import sys
import glob
import errno,time,os
import couchdb,simplejson
import json
from pprint import pprint

couch = couchdb.Server() # Assuming localhost:5984
#couch.resource.credentials = (USERNAME, PASSWORD)
# If your CouchDB server is running elsewhere, set it up like this:

db = couch['league']


path = '../datasets/all-matches/*.json'
#dirPath = 'C:/Users/VijayKumar/Desktop/CouchDB_Python'   
files = glob.glob(path)
for file1 in files: 
    #dirs = os.listdir( dirPath )
    file2 = glob.glob(file1)
    myfile = open("FailedFiles.txt", "a")
    for name in file2: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        try:
            with open(name, encoding="utf8") as f: # No need to specify 'r': this is the default.
                #sys.stdout.write(f.read())
                json_data=f
                data = json.load(json_data)
                data["_id"] = "match" + str(data["matchId"])
                db.save(data)
                json_data.close()
                #time.sleep(2)
        except IOError as exc:
            if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
                raise # Propagate other kinds of IOError.
        except:
            myfile.write(name + '\n')