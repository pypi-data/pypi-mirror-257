import pytest
from pytest import fixture
import importlib
from ... import navigation
import numpy as np
from distutils import dir_util
import os
import shutil
from ...utils import Body
from astropy.io import fits
import cartopy.crs as ccrs


@fixture
def datadir(request, tmpdir):
    rootdir = request.config.rootdir
    path = os.path.join(rootdir, 'pylanetary', 'navigation', 'tests', 'data')
    return path


def test_navigation(datadir):

    # load data, ephem, lat_g, lon_w, mu
    obs_time = '2019-10-28 08:50:50'
    obs_code = 568  # Keck Horizons observatory code
    pixscale_arcsec = 0.009971  # arcsec, keck
    flux = 2000
    a = 0.1
    beam = 0.5
    keck_uranus = np.load(os.path.join(datadir, 'keck_uranus.npy'))

    ura = Body('Uranus', epoch=obs_time, location=obs_code)
    nav = navigation.Nav(keck_uranus, ura, pixscale_arcsec)

    ldmodel = nav.ldmodel(flux, a, beam=beam, law='exp')
    ldmodel_expected = np.load(os.path.join(datadir, 'ldmodel.npy'))
    assert np.allclose(ldmodel, ldmodel_expected, rtol=1e-5, equal_nan=True)

    # test co-location algorithms
    (dx, dy, dxerr, dyerr) = nav.colocate(
        tb=flux,
        a=a,
        mode='convolution',
        diagnostic_plot=False,
        beam=beam)
    assert np.allclose([dx, dy], [133.455078125, -8.943359375],
                       atol=1.0)  # absolute 1-pixel tolerance
    (dx_canny,
     dy_canny,
     dxerr_canny,
     dyerr_canny) = nav.colocate(mode='canny',
                                 diagnostic_plot=False,
                                 tb=flux,
                                 a=a,
                                 low_thresh=1e-5,
                                 high_thresh=0.01,
                                 sigma=5)
    assert np.allclose([dx_canny, dy_canny], [126.830078125, -
                                              8.416015625], atol=1.0)  # absolute 1-pixel tolerance

    # test shifting of model to same loc as data
    nav.xy_shift_model(dx, dy)
    shifted_lat_expected = np.load(os.path.join(datadir, 'lat_g_keck.npy'))
    assert np.allclose(
        nav.lat_g,
        shifted_lat_expected,
        rtol=1e-3,
        equal_nan=True)

    # ensure no longitudes are below 0 or above 360
    nanfree_lon = nav.lon_w[~np.isnan(nav.lon_w)]
    assert np.all(nanfree_lon >= 0)
    assert np.all(nanfree_lon <= 360)

    # test re-projection onto lat-lon grid
    projected, mu_projected, mu0_projected, _, _ = nav.reproject()
    projected_expected = np.load(os.path.join(datadir, 'projected.npy'))
    mu_projected_expected = np.load(os.path.join(datadir, 'mu_projected.npy'))
    mu0_projected_expected = np.load(
        os.path.join(datadir, 'mu0_projected.npy'))
    assert np.allclose(
        projected,
        projected_expected,
        rtol=1e-2,
        equal_nan=True)
    assert np.allclose(
        mu_projected,
        mu_projected_expected,
        rtol=1e-2,
        equal_nan=True)
    assert np.allclose(
        mu0_projected,
        mu0_projected_expected,
        rtol=1e-2,
        equal_nan=True)

    # test re-projection to polar
    projected_polar, _, _, _, _ = nav.reproject('polar')
    projected_expected = np.load(os.path.join(datadir, 'projected_polar.npy'))
    assert np.allclose(
        projected_polar,
        projected_expected,
        rtol=1e-2,
        equal_nan=True)

    # test custom re-projection
    img_globe = ccrs.Globe(
        semimajor_axis=nav.req,
        semiminor_axis=nav.rpol,
        ellipse=None)
    custom_projection = ccrs.Robinson(central_longitude=0, globe=img_globe)
    custom_shape = (600, 300)
    projected_custom, _, _, _, _ = nav.reproject(
        projection=custom_projection, shape=custom_shape)
    projected_expected = np.load(os.path.join(datadir, 'projected_custom.npy'))
    assert np.allclose(
        projected_custom,
        projected_expected,
        rtol=1e-2,
        equal_nan=True)

    # ensure raise if custom projection and shape are not specified together
    with pytest.raises(ValueError):
        nav.reproject(projection=custom_projection)

    # test diagnostic plot
    import matplotlib
    fig, ax = navigation.colocate_diagnostic_plot(ldmodel, nav.data, 'canny')
    assert isinstance(fig, matplotlib.figure.Figure)


def test_nav_nonsquare(datadir):
    '''
    test for issue where non-square and/or odd-sided
    nav.colocate fails
    also represents a Neptune test case
    '''
    obs_code = 568  # Keck Horizons observatory code
    pixscale_arcsec = 0.009971  # arcsec, keck
    hdul = fits.open(os.path.join(datadir, 'nepk99_IF.fits'))
    obs_time = hdul[0].header['DATE-OBS'] + \
        ' ' + hdul[0].header['EXPSTART'][:-4]

    nep = Body('Neptune', epoch=obs_time, location=obs_code)
    nep.ephem['NPole_ang'] = 0.0
    nav = navigation.Nav(hdul[0].data, nep, pixscale_arcsec)
    (dx, dy, dxerr, dyerr) = nav.colocate(
        tb=1.5e-4,
        a=0.01,
        mode='disk',
        diagnostic_plot=False,
        beam=0.5)

    assert dx == -1.5
    assert dy == 7.5


def test_nav_jupiter_minnaert(datadir):

    # hst parameters
    flux = 1.15e4  # surface brightness in whatever units are in the fits file
    a = 0.9  # exponential limb-darkening law exponent
    fwhm = 3  # approximate FWHM of the point-spread function in pixels
    hdul = fits.open(
        os.path.join(
            datadir,
            'hlsp_wfcj_hst_wfc3-uvis_jupiter-2017-pj07_f631n_v2_0711ut0947-nav.fits'))
    data = hdul[1].data
    obs_time = hdul[0].header['DATE-OBS'] + ' ' + hdul[0].header['TIME-OBS']
    rotation = float(hdul[0].header['ORIENTAT'])
    pixscale_arcsec = float(hdul[0].header['PIXSCAL'])

    # instantiate the nav object
    jup = Body('Jupiter', epoch=obs_time, location='@hst')
    jup.ephem['NPole_ang'] = jup.ephem['NPole_ang'] - rotation
    data[np.isnan(data)] = 0.0
    nav = navigation.Nav(data, jup, pixscale_arcsec)
    ldmodel = nav.ldmodel(flux, a, beam=fwhm, law='minnaert')

    ldmodel_expected = np.load(
        os.path.join(
            datadir,
            'ldmodel_jupiter_minnaert.npy'))
    assert np.allclose(ldmodel, ldmodel_expected, rtol=1e-3, equal_nan=True)

    dx, dy, dxerr, dyerr = nav.colocate(mode='disk',
                                        tb=flux,
                                        a=a,
                                        law='minnaert',
                                        beam=fwhm,
                                        diagnostic_plot=False,
                                        )
    print(dx, dy)
    assert np.isclose(dx, 6.048828125, rtol=1e-1)
    assert np.isclose(dy, -8.791015625, rtol=1e-1)


def test_write(datadir):

    # bring in the Jupiter data from Mike Wong
    hdul = fits.open(
        os.path.join(
            datadir,
            'hlsp_wfcj_hst_wfc3-uvis_jupiter-2017-pj07_f631n_v2_0711ut0947-nav.fits'))
    data = hdul[1].data
    obs_time = hdul[0].header['DATE-OBS'] + ' ' + hdul[0].header['TIME-OBS']
    rotation = float(hdul[0].header['ORIENTAT'])
    pixscale_arcsec = float(hdul[0].header['PIXSCAL'])
    jup = Body('Jupiter', epoch=obs_time, location='@hst')
    jup.ephem['NPole_ang'] = jup.ephem['NPole_ang'] - rotation
    data[np.isnan(data)] = 0.0
    nav = navigation.Nav(data, jup, pixscale_arcsec)

    # manually change all the quantities according to what's in Mike's file
    nav.lat_g = hdul[2].data
    nav.lon_w = hdul[3].data
    nav.mu = np.cos(np.deg2rad(hdul[4].data))
    nav.mu0 = np.cos(np.deg2rad(hdul[5].data))

    # write it, then reload it
    nav.write(os.path.join(datadir, 'tmp.fits'), header={}, flux_unit='I/F')
    hdul_new = fits.open(os.path.join(datadir, 'tmp.fits'))

    # assert header info propagated
    assert np.isclose(
        hdul_new[0].header['TRG_LON'],
        hdul[0].header['TRG_LON'],
        rtol=1e-3)

    # assert data are in correct places
    for i in range(1, 6):
        assert np.allclose(
            hdul_new[i].data,
            np.array(
                hdul[i].data),
            atol=1e-2,
            equal_nan=True)

    # cleanup
    os.remove(os.path.join(datadir, 'tmp.fits'))
