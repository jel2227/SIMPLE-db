from datetime import date
import astropy.io.fits as fits
import warnings
warnings.filterwarnings('ignore')
#change to if then statements


def compile_header(**header_dict):
    """Creates a header from a dictionary of values. """
    header = fits.Header()
    header.set('EXTNAME', 'PRIMARY', 'name of this extension')
    # IVOA SpectrumDM keywords REQUIRED
    header.set('VOCLASS', header_dict['VOCLASS'],'VO Data Model')
    header.set('VOPUB',header_dict['VOPUB'],'VO Publisher ID URI') # uniform research identifier
    header.set('TITLE', header_dict['title'], 'data set title')
    header.set('OBJECT', header_dict['object_name'], 'name of observed object')
    header.set('RA', header_dict['RA'] , '[deg] Pointing position')
    header.set('DEC', header_dict['dec'] , '[deg] Pointing position')
    header.set('TMID', header_dict['time'], '[d] MJD mid expsoure')
    header.set('TSTART', header_dict['time_start'], '[d] MJD start time')
    header.set('TSTOP', header_dict['time_stop'], '[d] MJD stop time')
    header.set('TELAPSE', header_dict['exposure_time'],'[s] Total elapsed time')
    header.set('SPEC_VAL', header_dict['bandpass'], '[angstrom] Characteristic spec coord')

    header.set('SPEC_BW', header_dict['width'], f"[{header_dict['wavelength_units']}] Width of spectrum")
    header.set('TDMIN1', header_dict['min_wave'], f"[{header_dict['wavelength_units']}] starting wavelength")
    header.set('TDMAX1', header_dict['max_wave'], f"[{header_dict['wavelength_units']}] ending wavelength")
    header.set('APERTURE', header_dict['aperture'],'[arcsec]slit width') #from paper
    header.set('AUTHOR', header_dict['author'], 'author of the data')
    # Other IVOA SpectrumDM keywords
    header.set('VOREF', header_dict['bibcode'], 'bibcode' )
    header.set('DATE', date.today().strftime("%Y-%m-%d"), 'date of file creation')
    header.set('INSTRUME', header_dict['instrument'], 'name of instrument')
    header.set('DATE-OBS', header_dict['obs_date'].strftime("%Y-%m-%d"), 'date of the observation')
    header.set('REFERENC', header_dict['reference_doi'], 'bibliographic reference')
    header.set('TELESCOP', header_dict['telescope'], 'name of telescope')
    header.set('HISTORY', header_dict['history'])
    header.set('COMMENT', header_dict['comment'])


    return header











