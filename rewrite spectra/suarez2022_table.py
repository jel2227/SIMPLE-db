
from astropy.table import Table


def create_suarez22_table(spectrum_url):
    spectrum_table = Table.read(spectrum_url, format='ascii',names=['col1', 'col2', 'col3'])
    return spectrum_table
