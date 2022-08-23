import warnings
warnings.filterwarnings('ignore')
from datetime import date
import astropy.io.fits as fits
import warnings
warnings.filterwarnings('ignore')

def compile_header(**header_dict):
    """Creates a header from a dictionary of values. """
    header = fits.Header()
    header.set('EXTNAME', 'PRIMARY', 'name of this extension')
    # IVOA SpectrumDM keywords REQUIRED

    if header_dict['VOCLASS'] != None:
        header.set('VOCLASS', header_dict['VOCLASS'],'VO Data Model')
    if header_dict['VOPUB'] != None:
        header.set('VOPUB',header_dict['VOPUB'],'VO Publisher ID URI') # uniform research identifier
    if header_dict['title'] != None:
        header.set('TITLE', header_dict['title'], 'data set title')
    if header_dict['object_name'] != None:
        header.set('OBJECT', header_dict['object_name'].replace("'",''), 'name of observed object')
    if header_dict['RA'] != None:
        header.set('RA', header_dict['RA'] , '[deg] Pointing position')
    if header_dict['dec'] != None:
        header.set('DEC', header_dict['dec'] , '[deg] Pointing position')
    if header_dict['time'] != None:
        header.set('TMID', header_dict['time'], '[d] MJD mid expsoure')
    if header_dict['time_start'] != None:
        header.set('TSTART', header_dict['time_start'], '[d] MJD start time')
    if header_dict['time_stop'] != None:
        header.set('TSTOP', header_dict['time_stop'], '[d] MJD stop time')
    if header_dict['exposure_time'] != None:
        header.set('TELAPSE', header_dict['exposure_time'],'[s] Total elapsed time')
    if header_dict['bandpass'] != None:
        header.set('SPEC_VAL', header_dict['bandpass'], '[angstrom] Characteristic spec coord')
    if header_dict['width'] != None:
        header.set('SPEC_BW', header_dict['width'], f"[{header_dict['wavelength_units']}] Width of spectrum")
    if header_dict['min_wave'] != None:
       header.set('TDMIN1', header_dict['min_wave'], f"[{header_dict['wavelength_units']}] starting wavelength")
    if header_dict['min_wave'] != None:
         header.set('TDMAX1', header_dict['max_wave'], f"[{header_dict['wavelength_units']}] ending wavelength")
    if header_dict['aperture'] != None:
        header.set('APERTURE', header_dict['aperture'],'[arcsec]slit width') #from paper
    if header_dict['author'] != None:
        header.set('AUTHOR', header_dict['author'], 'author of the data')
    # Other IVOA SpectrumDM keywords
    if header_dict['bibcode'] != None:
        header.set('VOREF', header_dict['bibcode'], 'bibcode' )
    header.set('DATE', date.today().strftime("%Y-%m-%d"), 'date of file creation')
    if header_dict['instrument'] != None:
        header.set('INSTRUME', header_dict['instrument'], 'name of instrument')
    if header_dict['obs_date'] != None:
        header.set('DATE-OBS', header_dict['obs_date'].strftime("%Y-%m-%d"), 'date of the observation')
    if header_dict['reference_doi'] != None:
        header.set('REFERENC', header_dict['reference_doi'], 'bibliographic reference')
    if header_dict['telescope'] != None:
        header.set('TELESCOP', header_dict['telescope'], 'name of telescope')
    if  header_dict['history'] != None:
        header.set('HISTORY', header_dict['history'])
    if header_dict['comment'] != None:
        header.set('COMMENT', header_dict['comment'])
    if header_dict['obs_location'] != None:
        header.set('OBSERVAT', header_dict['obs_location'],'name of observatory')

#change header fun to if then statements if keyword exists
    return header

