from glob import glob
from astropy.io import fits
from matplotlib import pyplot as plt
from specutils import Spectrum1D
from astropy import units as u


files = glob('/Users/jolie/gitlocation/rewrite spectra/Manj14/*.fits')


for file_name in files:

    f = fits.open(file_name)
    name = file_name[48:-len('.fits')]
    specdata = f[1].data
    wavelength_unit = u.micron  #using astropy to defien units
    flux_unit = u.erg/u.cm/u.cm/u.s/u.Angstrom
    wavelength = specdata['wavelength'] * wavelength_unit # u.AA
    flux = specdata['flux'] * flux_unit #10**-17 * u.Unit('erg cm-2 s-1 AA-1')
    spec = Spectrum1D(spectral_axis=wavelength, flux=flux)
    f, ax = plt.subplots()
    ax.step(spec.spectral_axis, spec.flux)
    plt.xlabel('wavelength')
    plt.ylabel('flux ')
    plt.title(name)

    plt.show()
