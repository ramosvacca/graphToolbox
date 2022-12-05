import pandas as pd
import os

inputfile='/media/newbuntu/rdfal/ckg.csv'
cwd = os.path.dirname(os.path.realpath(__file__))

count=0
columnsList=pd.read_csv(inputfile, index_col=0, nrows=0).columns.tolist()

for chunk in pd.read_csv(inputfile,chunksize=1000):
    if count<1:
        filename = open(cwd+'/outputData/'+str(count)+'.csv', 'w+')
        chunk.to_csv(filename, header=True, columns=columnsList, mode='w')
        print(chunk)