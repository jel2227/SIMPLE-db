import os
from astropy.table import Table
from w3lib.url import safe_url_string
from astropy.io import fits

def create_spectrum_table(spectrum_url,startline):
    #fomat = string =! None (have it be csv or somehting)
    '''Doc string with what u excpet the varibales to be and what it returns '''
    file = os.path.basename(spectrum_url)
    file_root = os.path.splitext(file)[1]
    if file_root == '.dat':
        spectrum_table = Table.read(spectrum_url, format='ascii',names=['col1', 'col2', 'col3'])
    elif file_root == '.fits':
        url_data = fits.getdata(spectrum_url)
        spectrum_table = Table(url_data, names=['col1', 'col2', 'col3'])
    elif file_root == '.csv':
        spectrum_table = Table.read(spectrum_url, format = 'ascii',names=['col1', 'col2', 'col3'])
    elif file_root == '.txt':
        data = safe_url_string(spectrum_url, encoding="utf-8")
        spectrum_table = Table.read(data,format = 'ascii',guess=False,fast_reader=False,header_start = None,data_start=startline,delimiter=',',names=['col1', 'col2', 'col3'])
    else:
        print("file not found")

    return spectrum_table
