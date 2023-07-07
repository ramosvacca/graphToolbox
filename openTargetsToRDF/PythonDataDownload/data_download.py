# from pyspark import SparkConf
# from pyspark.sql import SparkSession
# import pyspark.sql.functions as F
#
# # path to ClinVar (EVA) evidence dataset
# # directory stored on your local machine
# evidencePath = "/media/newbuntu/rdfal/NEW AGE/OpenTargets/python_download/"
# #
# # import subprocess
# # version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
# #
# # print(version)
#
# # establish spark connection
# spark = (
#     SparkSession.builder
#     .master('local[*]')
#     .getOrCreate()
# )
#
# # read evidence dataset
# evd = spark.read.parquet(evidencePath)
#
# # Browse the evidence schema
# evd.printSchema()

from ftplib import FTP
import os

# connect to the FTP server
FTP_SERVER = 'ftp.ebi.ac.uk'
FTP_USERNAME = 'anonymous'
FTP_PASSWORD = 'PASS'

# connect to the FTP server
ftp = FTP(FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)

# specify the directory you want to change to
# ftp.cwd('/pub/databases/opentargets/platform/latest/output/etl/json/')

# function to download a file
def grabFile(filename, localpath):
    localfile = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    localfile.close()

BASE_PATH = '/pub/databases/opentargets/platform/23.06/output/etl/json'

def walk_dir(ftp, path, local_path):
    # Change to the target directory on the FTP server
    ftp.cwd(path)
    print(f'Changed directory to: {path}')

    # Here we use path instead of ftp.pwd() since the cwd has been changed
    if path.startswith(BASE_PATH):
        # Calculate the subdirectory path relative to BASE_PATH
        subdirectory = os.path.relpath(path, BASE_PATH)
        if subdirectory == '.':
            subdirectory = ''
        print(f'Subdirectory: {subdirectory}')

        # Construct the local path for this subdirectory
        local_subdirectory = os.path.join(local_path, subdirectory)
        print(f'Local subdirectory: {local_subdirectory}')

        # Create the local subdirectory if it does not already exist
        if not os.path.exists(local_subdirectory):
            print(f'Creating local directory: {local_subdirectory}')
            os.makedirs(local_subdirectory)

        # Get the list of files/directories for the current directory on the FTP server
        items = ftp.nlst()
        print(f'Listing directory: {items}')

        for item in items:
            print(f'Processing item: {item}')
            try:
                # Try changing to the item directory
                ftp.cwd(item)
                print(f'Changed directory to: {item}')
                # If we successfully changed to the directory, then this item is a directory. We should recursively walk it.
                new_path = path + "/" + item
                walk_dir(ftp, new_path, local_subdirectory)
            except:
                # If changing to the directory failed, this item is a file. Download it.
                print(f'Downloading file: {item}')
                grabFile(item, os.path.join(local_subdirectory, item))

    # Reset the current FTP directory to the parent directory
    ftp.cwd("..")
    print(f'Returned to parent directory: {ftp.pwd()}')




# call the recursive function
walk_dir(ftp, '/pub/databases/opentargets/platform/23.06/output/etl/json/', '/media/newbuntu/rdfal/NEW AGE/OpenTargets/from_ftp')

ftp.quit()
