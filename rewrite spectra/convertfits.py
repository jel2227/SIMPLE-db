from pandas import to_datetime
import warnings
warnings.filterwarnings('ignore')
from astropy.time import Time
import warnings
warnings.filterwarnings('ignore')
from astropy.nddata import StdDevUncertainty
from compileheader import *
from create_spectrum_table import *
from urllib.parse import unquote
import astropy.units as u
from astroquery.simbad import Simbad
from astropy.coordinates import Angle

def convert_to_fits(spectra_data_info):
    flux_unit = u.erg/u.cm/u.cm/u.s/u.Angstrom
    for row in spectra_data_info['data']:
        object_name = (unquote(row[spectra_data_info['object_name_column']])) #set as string and ascii name here- not in hdu1.header.set
        #might need to do string(row) for object name
        spectrum_url = row[spectra_data_info['spectrum_url_column']]
        file = os.path.basename(spectrum_url)
        full_name = (spectra_data_info['original_data_dir'] + file)


        history1 = ascii(f'Original file: {file}') #gives orginal name of file
        history2 = spectra_data_info['generated_history']  #shows where file came from
        history = (history1 +', ' + history2)

        comment1 = spectra_data_info['spectra_comments']
        comment = (comment1)

        spectrum_table = create_spectrum_table(spectrum_url, spectra_data_info['startline'])

        wavelength_data = spectrum_table[spectra_data_info['wavelength_column']] * spectra_data_info['wavelength_unit']
        #wavelength, flux = np.empty(0), np.empty(0)
        if spectra_data_info['flux_unit'] == u.Jy:
            flux = (spectrum_table[spectra_data_info['flux_column']])*u.Jy.to(u.erg / u.s / u.cm**2 / u.AA ,equivalencies=u.spectral_density(wavelength_data))
            flux_unc = (spectrum_table[spectra_data_info['flux_unc_column']])*u.Jy.to(u.erg / u.s / u.cm**2 / u.AA ,equivalencies=u.spectral_density(wavelength_data))
        elif spectra_data_info['flux_unit'] == flux_unit:
            flux = spectrum_table[spectra_data_info['flux_column']]

        #flux_unc_class = StdDevUncertainty(spectrum_table[spectra_data_info['flux_column']])
        # i just call the expression
      #gives arrays of flux w units

          #multiplying everythign by untis to convert

        spectrum_data_out = Table({'wavelength': spectrum_table[spectra_data_info['wavelength_column']] * spectra_data_info['wavelength_unit'] , 'flux':flux * flux_unit , 'flux_uncertainty':flux_unc * flux_unit})

        hdu1 = fits.BinTableHDU(data = spectrum_data_out)

        hdu1.header['EXTNAME'] = 'SPECTRUM' #prints out different headers
       # hdu1.header.set('Spectrum', str(ascii(object_name)), 'Object Name')
        hdu1.header.set('Spectrum', ascii(object_name).replace("'", ''), 'Object Name') #take out string and ascii

        try:
            ra = row[spectra_data_info['RA_column_name']]
        except KeyError:
            result_table = Simbad.query_object(object_name)
            ra_sexig = result_table['RA']
            ra_convert = [x +" hours" for x in ra_sexig]
            ra = Angle(ra_convert).degree[0]
        try:
            dec = row[spectra_data_info['dec_column_name']]
        except KeyError:
            result_table = Simbad.query_object(object_name)
            dec_sexig = result_table['DEC']
            dec_convert = [x +" degrees" for x in dec_sexig]
            dec = Angle(dec_convert).degree[0]

        try:
            time = (Time(to_datetime(row[spectra_data_info['start_time_column_name']])).jd + Time(to_datetime(row[spectra_data_info['stop_time_column_name']])).jd) /2
        except KeyError:
            time = None
        try:
            exposure_time = row[spectra_data_info['exposure_time_column_name']]
        except KeyError:
            exposure_time = None
        try:
            time_start = Time(to_datetime(row[spectra_data_info['start_time_column_name']])).jd
        except KeyError:
            time_start = None
        try:
            time_stop = Time(to_datetime(row[spectra_data_info['stop_time_column_name']])).jd
        except KeyError:
            time_stop = None
        try:
            instrument = row[spectra_data_info['instrument_column_name']]
        except KeyError:
            instrument = None
        try:
            obs_date = to_datetime(row[spectra_data_info['observation_date_column_name']])
        except KeyError:
            obs_date = None
        try:
            telescope = row[spectra_data_info['telescope_column_name']]
        except KeyError:
            telescope = None

        #turn these into a dictionary
        header_dict = {
            'VOCLASS' : spectra_data_info['voclass'],
            'VOPUB' : spectra_data_info['vopub'] ,
            'title' : spectra_data_info['title'] ,
            'RA' : ra ,
            'dec' : dec , #from the vizier catalog, put in csv table
            'time' : time,
            'exposure_time' : exposure_time ,
            'bandpass' : spectra_data_info['bandpass'] ,#get from paper
            'aperture' : spectra_data_info['aperture'] ,
            'object_name' : ascii(object_name),

            #OTHER KEYWORDS
            'time_start' : time_start , #turns dates into accepetable format then converts to Time object then to MJD
            'time_stop' : time_stop, #dates r orginally in month day, year
            'bibcode' : spectra_data_info['bibcode'],
            'instrument' : instrument ,
            'obs_date' : obs_date ,
            'author' : spectra_data_info['author'],
            'reference_doi' : spectra_data_info['doi'] ,
            'telescope' : telescope ,
            'history' : history ,
            'wavelength' : wavelength_data , #multiplying everythign by untis to convert
            'wavelength_units' : f"[{wavelength_data.unit:FITS}]",
            'width' : (max(wavelength_data).value - min(wavelength_data.value)),
            'min_wave' : min(wavelength_data).value,
            'max_wave' : max(wavelength_data).value,
            'flux' : tuple(spectrum_table[spectra_data_info['flux_column']].data) * spectra_data_info['flux_unit'],
            'flux_unc' : tuple(spectrum_table[spectra_data_info['flux_unc_column']].data) * spectra_data_info['flux_unit'],
            'comment': comment,
            'obs_location':spectra_data_info['obs_location']
            }
        print(spectra_data_info['stop_time_column_name'])
        hdu0 = fits.PrimaryHDU(header=compile_header(**header_dict))

        spectrum_mef = fits.HDUList([hdu0,hdu1])#hdu0 is header and hdu1 is data

        file_root = os.path.splitext(file)[0] #split the path name into a pair root and ext so the root is just the ext [0] is the name of the file wihtout the .csv
        fits_filename = spectra_data_info['fits_data_dir'] + object_name + '.fits' #turns into fits files by putting it in new folder that we defined at begining and adding name of file then .fits
        try:
            spectrum_mef.writeto(fits_filename, overwrite=True)
            # SHOULD BE: spectrum.write(fits_filename, format='tabular-fits', overwrite=True, update_header=True)
            #logger.info(f'Wrote {fits_filename}')
        except:
            raise ValueError

    return
