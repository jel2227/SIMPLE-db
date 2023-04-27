from scripts.ingests.ingest_utils import *
from scripts.ingests.utils import *

SAVE_DB = True # save the data files in addition to modifying the .db file
RECREATE_DB = False  # recreates the .db file from the data files

logger.setLevel(logging.DEBUG)

db = load_simpledb('SIMPLE.db', recreatedb=RECREATE_DB)

# url : https://docs.google.com/spreadsheets/d/1ojsNF59GvdFhf-lgwJaCwiHPfaRx4fmCpyzKEonrVbw/edit#gid=0
SHEET_ID = '1ojsNF59GvdFhf-lgwJaCwiHPfaRx4fmCpyzKEonrVbw'
SHEET_NAME = 'AAPL'
full = 'all'

url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={full}'
data = pd.read_csv(url)


for index, row in data.iterrows():
    spectrum_url = row['spectrum'] #goes to specific column entry finds the url
    object_name = row['Source']
    with db.engine.begin() as conn:
        conn.execute(db.Spectra.update().where(db.Spectra.c.reference == 'Suar22', db.Spectra.c.source == object_name ).values(spectrum = spectrum_url ))

    # WRITE THE JSON FILES
    if SAVE_DB:
        db.save_database(directory='data/')
