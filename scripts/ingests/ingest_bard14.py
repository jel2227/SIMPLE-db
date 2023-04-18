from scripts.ingests.ingest_utils import *
from scripts.ingests.utils import *

SAVE_DB = False # save the data files in addition to modifying the .db file
RECREATE_DB = False  # recreates the .db file from the data files

logger.setLevel(logging.DEBUG)

db = load_simpledb('SIMPLE.db', recreatedb=RECREATE_DB)

# url : https://docs.google.com/spreadsheets/d/11o5NRGA7jSbHKaTNK7SJnu_DTECjsyZ6rY3rcznYsJk/edit#gid=0
SHEET_ID = '11o5NRGA7jSbHKaTNK7SJnu_DTECjsyZ6rY3rcznYsJk'
SHEET_NAME = 'AAPL'
full = 'all'

url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={full}'
data = pd.read_csv(url)


for index, row in data.iterrows():
    original_spectrum = row['Original Spectrum'] #row is defined so it loops through each row to
    spectrum_url = row['Spectrum'] #goes to specific column entry finds the url
    object_name = row['Source']
    with db.engine.begin() as conn:
        conn.execute(db.Spectra.update().where(db.Spectra.c.source == object_name).values(spectrum = spectrum_url ))
        conn.execute(db.Spectra.update().where(db.Spinectra.c.source == object_name).values(original_spectrum = original_spectrum))

    # WRITE THE JSON FILES
    if SAVE_DB:
        db.save_database(directory='data/')
