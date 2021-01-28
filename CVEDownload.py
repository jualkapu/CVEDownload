import requests
import re
from zipfile import ZipFile
import os

#Gets filenames of zipped JSON files containing CVEs
def getFilenames(url):
    r = requests.get(url)
    filenames = []
    for filename in re.findall("nvdcve-1.1-[0-9]*\.json\.zip",r.text):
        filenames.append(filename)
    return filenames

#Downloads every .zip file that was found with getFilenames()
def downloadFile(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

#Unzips given file. In this case input file is the JSON just downloaded by downloadFile()
def unzip(filename):
    with ZipFile(filename, 'r') as zip:
        zip.extractall()

#Removes .zip files from location
def removeZipped():
    dir_name = os.getcwd()
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".zip"):
            os.remove(os.path.join(dir_name, item))

filenames = getFilenames('https://nvd.nist.gov/vuln/data-feeds#JSON_FEED')
print('Loading and unzipping data....')
for filename in filenames:
    downloadFile('https://nvd.nist.gov/feeds/json/cve/1.1/'+filename, filename)
    unzip(filename)

removeZipped()
print('Done!')