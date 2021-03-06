from datetime import datetime
from multiply_core.observations.data_validation import AWSS2L1Validator, ModisMCD43Validator, ModisMCD15A2HValidator,\
    CamsValidator, S2AEmulatorValidator, S2BEmulatorValidator, WVEmulatorValidator, AsterValidator, get_valid_types, \
    CamsTiffValidator
from shapely.geometry import Polygon
from shapely.wkt import loads

__author__ = "Tonio Fincke (Brockmann Consult GmbH)"

VALID_AWS_S2_DATA = './test/test_data/s2_aws/15/F/ZX/2016/12/31/1'
VALID_CAMS_TIFF_DATA = './test/test_data/2018_10_23/'


def test_aws_s2_validator_matches_pattern():
    validator = AWSS2L1Validator()

    assert validator._matches_pattern('/29/S/QB/2017/9/4/0')
    assert validator._matches_pattern(VALID_AWS_S2_DATA)
    assert not validator._matches_pattern('fcsfzvdbt/chvs/201')


def test_aws_s2_validator_is_valid():
    validator = AWSS2L1Validator()

    assert validator.is_valid(VALID_AWS_S2_DATA)


def test_aws_s2_validator_get_relative_path():
    validator = AWSS2L1Validator()

    assert '29/S/QB/2017/9/4/0' == validator.get_relative_path('/the/non/relative/part/29/S/QB/2017/9/4/0')


def test_modis_mcd_43_validator_is_valid():
    validator = ModisMCD43Validator()

    assert validator.is_valid('MCD43A1.A2017250.h17v05.006.2017261201257.hdf')
    assert validator.is_valid('MCD43A1.A2017250.h17v05.006.herebesomething.hdf')
    assert validator.is_valid('MCD43A1.A2001001.h00v00.006.herebesomething.hdf')
    assert validator.is_valid('MCD43A1.A2017365.h35v17.006.herebesomething.hdf')
    assert validator.is_valid('MCD43A1.A2016366.h35v17.006.herebesomething.hdf')
    assert validator.is_valid('some/path/MCD43A1.A2016366.h35v17.006.herebesomething.hdf')
    assert not validator.is_valid('MCD43A1.A1999275.h35v17.006.herebesomething.hdf')
    assert not validator.is_valid('MCD43A1.A2002475.h35v17.006.herebesomething.hdf')
    assert not validator.is_valid('MCD43A1.A2002275.h40v17.006.herebesomething.hdf')
    assert not validator.is_valid('MCD43A1.A2002275.h10v20.006.herebesomething.hdf')


def test_modis_mcd_15_validator_name():
    validator = ModisMCD15A2HValidator()

    assert 'MCD15A2H.006' == validator.name()


def test_modis_mcd_15_validator_is_valid():
    validator = ModisMCD15A2HValidator()

    assert validator.is_valid('MCD15A2H.A2017250.h17v05.006.2017261201257.hdf')
    assert validator.is_valid('MCD15A2H.A2017250.h17v05.006.herebesomething.hdf')
    assert validator.is_valid('MCD15A2H.A2001001.h00v00.006.herebesomething.hdf')
    assert validator.is_valid('MCD15A2H.A2017365.h35v17.006.herebesomething.hdf')
    assert validator.is_valid('MCD15A2H.A2016366.h35v17.006.herebesomething.hdf')
    assert validator.is_valid('some/path/MCD15A2H.A2016366.h35v17.006.herebesomething.hdf')
    assert not validator.is_valid('MCD15A2H.A1999275.h35v17.006.herebesomething.hdf')
    assert not validator.is_valid('MCD15A2H.A2002475.h35v17.006.herebesomething.hdf')
    assert not validator.is_valid('MCD15A2H.A2002275.h40v17.006.herebesomething.hdf')
    assert not validator.is_valid('MCD15A2H.A2002275.h10v20.006.herebesomething.hdf')


def test_modis_mcd_15_validator_get_relative_path():
    validator = ModisMCD15A2HValidator()

    assert '' == validator.get_relative_path('some/path/MCD15A2H.A2016366.h35v17.006.herebesomething.hdf')


def test_modis_mcd_15_validator_get_file_pattern():
    validator = ModisMCD15A2HValidator()

    assert 'MCD15A2H.A20[0-9][0-9][0-3][0-9][0-9].h[0-3][0-9]v[0-1][0-9].006.*.hdf' == validator.get_file_pattern()


def test_cams_tiff_name():
    validator = CamsTiffValidator()
    assert 'CAMS_TIFF' == validator.name()


def test_cams_tiff_is_valid():
    validator = CamsTiffValidator()

    assert validator.is_valid(VALID_CAMS_TIFF_DATA)
    assert not validator.is_valid('./test/test_data/2018_10_24/')


def test_cams_tiff_validator_get_relative_path():
    validator = CamsTiffValidator()

    assert '2016_04_21' == validator.get_relative_path('/the/non/relative/part/2016_04_21/')


def test_cams_tiff_get_file_pattern():
    validator = CamsTiffValidator()

    assert '20[0-9][0-9]_[0-1][0-9]_[0-3][0-9]' == validator.get_file_pattern()


def test_cams_tiff_is_valid_for():
    validator = CamsTiffValidator()

    assert validator.is_valid_for(VALID_CAMS_TIFF_DATA, Polygon(), datetime(2018, 10, 20), datetime(2018, 10, 25))
    assert not validator.is_valid_for(VALID_CAMS_TIFF_DATA, Polygon(), datetime(2018, 10, 20), datetime(2018, 10, 22))
    assert not validator.is_valid_for('/some/path/2016-09-14', Polygon(), datetime(2016, 9, 1), datetime(2016, 9, 10))


def test_cams_name():
    validator = CamsValidator()
    assert 'CAMS' == validator.name()


def test_cams_is_valid():
    validator = CamsValidator()

    assert validator.is_valid('2017-09-14.nc')
    assert validator.is_valid('/some/path/2017-09-14.nc')
    assert not validator.is_valid('2017-09-14')
    assert not validator.is_valid('1000-29-34.nc')


def test_cams_get_file_pattern():
    validator = CamsValidator()

    assert '20[0-9][0-9]-[0-1][0-9]-[0-3][0-9].nc' == validator.get_file_pattern()


def test_cams_is_valid_for():
    validator = CamsValidator()

    assert validator.is_valid_for('2017-09-14.nc', Polygon(), datetime(2017, 9, 14), datetime(2017, 9, 14))
    assert validator.is_valid_for('2017-09-14.nc', Polygon(), datetime(2017, 9, 13), datetime(2017, 9, 15))
    assert validator.is_valid_for('/some/path/2017-09-14.nc', Polygon(), datetime(2017, 9, 13), datetime(2017, 9, 15))
    assert not validator.is_valid_for('2017-09-14.nc', Polygon(), datetime(2017, 9, 10), datetime(2017, 9, 12))


def test_s2a_emulator_name():
    validator = S2AEmulatorValidator()

    assert 'ISO_MSI_A_EMU' == validator.name()


def test_s2a_is_valid():
    validator = S2AEmulatorValidator()

    assert validator.is_valid('isotropic_MSI_emulators_correction_xap_S2A.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_correction_xbp_S2A.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_correction_xcp_S2A.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_optimization_xap_S2A.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_optimization_xbp_S2A.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_optimization_xcp_S2A.pkl')
    assert validator.is_valid('/some/path/isotropic_MSI_emulators_optimization_xcp_S2A.pkl')
    assert not validator.is_valid('isotropic_MSI_emulators_optimization_xdp_S2A.pkl')


def test_s2a_get_file_pattern():
    validator = S2AEmulatorValidator()

    assert 'isotropic_MSI_emulators_(?:correction|optimization)_x[a|b|c]p_S2A.pkl' == validator.get_file_pattern()


def test_s2b_emulator_name():
    validator = S2BEmulatorValidator()

    assert 'ISO_MSI_B_EMU' == validator.name()


def test_s2b_is_valid():
    validator = S2BEmulatorValidator()

    assert validator.is_valid('isotropic_MSI_emulators_correction_xap_S2B.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_correction_xbp_S2B.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_correction_xcp_S2B.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_optimization_xap_S2B.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_optimization_xbp_S2B.pkl')
    assert validator.is_valid('isotropic_MSI_emulators_optimization_xcp_S2B.pkl')
    assert validator.is_valid('/some/path/isotropic_MSI_emulators_optimization_xcp_S2B.pkl')
    assert not validator.is_valid('isotropic_MSI_emulators_optimization_xdp_S2B.pkl')


def test_s2b_get_file_pattern():
    validator = S2BEmulatorValidator()

    assert 'isotropic_MSI_emulators_(?:correction|optimization)_x[a|b|c]p_S2B.pkl' == validator.get_file_pattern()


def test_wv_emulator_name():
    validator = WVEmulatorValidator()

    assert 'WV_EMU' == validator.name()


def test_wv_is_valid():
    validator = WVEmulatorValidator()

    assert validator.is_valid('wv_MSI_retrieval_S2A.pkl')
    assert validator.is_valid('wv_MSI_retrieval_S2A.pkl')
    assert validator.is_valid('/some/path/wv_MSI_retrieval_S2A.pkl')
    assert not validator.is_valid('wv_MSI_ratrieval_S2A.pkl')


def test_wv_get_file_pattern():
    validator = WVEmulatorValidator()

    assert 'wv_MSI_retrieval_S2A.pkl' == validator.get_file_pattern()


def test_aster_name():
    validator = AsterValidator()

    assert 'ASTER' == validator.name()


def test_aster_is_valid():
    validator = AsterValidator()

    assert validator.is_valid('ASTGTM2_N00E000_dem.tif')
    assert validator.is_valid('ASTGTM2_S11W111_dem.tif')
    assert validator.is_valid('/some/path/ASTGTM2_S11W111_dem.tif')
    assert not validator.is_valid('ASTGTM2_W11S111_dem.tif')
    assert not validator.is_valid('ASTGTM2_N90E200_dem.tif')


def test_aster_get_file_pattern():
    validator = AsterValidator()

    assert 'ASTGTM2_[N|S][0-8][0-9][E|W][0|1][0-9][0-9]_dem.tif' == validator.get_file_pattern()


def test_aster_is_valid_for():
    validator = AsterValidator()

    polygon = loads('POLYGON((134.20 12.09, 133.91 12.09, 133.91 11.94, 134.2 11.94, 134.20 12.09))')
    assert validator.is_valid_for('ASTGTM2_N12E134_dem.tif', polygon, datetime(1000, 1, 1), datetime(1000, 1, 3))
    assert validator.is_valid_for('ASTGTM2_N11E134_dem.tif', polygon, datetime(1000, 1, 1), datetime(1000, 1, 3))
    assert validator.is_valid_for('ASTGTM2_N11E133_dem.tif', polygon, datetime(1000, 1, 1), datetime(1000, 1, 3))
    assert validator.is_valid_for('ASTGTM2_N12E133_dem.tif', polygon, datetime(1000, 1, 1), datetime(1000, 1, 3))
    assert validator.is_valid_for('/some/path/ASTGTM2_N12E133_dem.tif', polygon, datetime(1000, 1, 1), datetime(1000, 1, 3))
    assert not validator.is_valid_for('ASTGTM2_N13E133_dem.tif', polygon, datetime(1000, 1, 1), datetime(1000, 1, 3))


def test_get_valid_types():
    valid_types = get_valid_types()

    assert 10 == len(valid_types)
    assert 'AWS_S2_L1C' in valid_types
    assert 'AWS_S2_L2' in valid_types
    assert 'MCD43A1.006' in valid_types
    assert 'MCD15A2H.006' in valid_types
    assert 'CAMS' in valid_types
    assert 'CAMS_TIFF' in valid_types
    assert 'ISO_MSI_A_EMU' in valid_types
    assert 'ISO_MSI_B_EMU' in valid_types
    assert 'WV_EMU' in valid_types
    assert 'ASTER' in valid_types
