from astropy.io import ascii
from scripts.ingests.utils import *
from specutils import Spectrum1D
import astropy.units as u
from datetime import date


bard14_url = []
bard14_names = []
# get meta data from SIMPLE -> modify query
#spot check to make sure its accurate

table = '/Users/jolie/gitlocation/SIMPLE-db/not_working_txt_table_2023-03-01.dat'
data = ascii.read(table)
for row in data:
    if row['reference'] == 'Bard14':
        bard14_names.append(row['source'])
        bard14_url.append(row['spectrum'])
    else:
        pass

print(bard14_url)

bard14_table = Table([bard14_names,bard14_url],
                       names=('source','spectrum')) #add column names source and url
#ascii.write(bard14_table, f'not_working_table_{date}.dat', overwrite=False)

print(bard14_table['spectrum'])
