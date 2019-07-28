import struct

from seabreeze.pyseabreeze.communication import USBCommOOI, USBCommOBP
from seabreeze.pyseabreeze.features._base import SeaBreezeFeature


# Definition
# ==========
#
class SeaBreezeNonlinearityCoefficientsFeature(SeaBreezeFeature):
    identifier = 'nonlinearity_coefficients'

    def get_nonlinearity_coefficients(self):
        raise NotImplementedError("implement in derived class")


# OOI implementation
# ==================
#
class NonlinearityCoefficientsEEPromFeatureOOI(SeaBreezeNonlinearityCoefficientsFeature):
    required_interface_cls = USBCommOOI
    required_features = ('eeprom',)

    def get_nonlinearity_coefficients(self):
        # The spectrometers store the wavelength calibration in slots 6..13
        coeffs = []
        order = int(float(self.device.f.eeprom.read_eeprom_slot(14)))
        for i in range(6, 6 + order + 1):
            coeffs.append(float(self.device.f.eeprom.read_eeprom_slot(i)))
        return coeffs


# OBP implementation
# ==================
#
class NonlinearityCoefficientsFeatureOBP(SeaBreezeNonlinearityCoefficientsFeature):
    required_interface_cls = USBCommOBP

    def get_nonlinearity_coefficients(self):
        # get number of nonlinearity coefficients
        data = self.device.query(0x00181100, "")
        N = struct.unpack("<B", data)[0]
        # now query the coefficients
        coeffs = []
        for i in range(N):
            data = self.device.query(0x00181101, struct.pack("<B", i))
            coeffs.append(struct.unpack("<f", data)[0])
        return coeffs
