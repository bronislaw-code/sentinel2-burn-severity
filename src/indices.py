"""Spectral indices for burn severity and vegetation analysis."""

import numpy as np


def nbr(nir, swir):
    """Normalized Burn Ratio: (NIR - SWIR) / (NIR + SWIR)"""
    return (nir - swir) / (nir + swir + 1e-10)


def nbr2(swir1, swir2):
    """Normalized Burn Ratio 2: (SWIR1 - SWIR2) / (SWIR1 + SWIR2)"""
    return (swir1 - swir2) / (swir1 + swir2 + 1e-10)


def dnbr(nbr_pre, nbr_post):
    """Differenced NBR. Positive values indicate burned areas."""
    return nbr_pre - nbr_post


def ndvi(nir, red):
    """Normalized Difference Vegetation Index: (NIR - RED) / (NIR + RED)"""
    return (nir - red) / (nir + red + 1e-10)


def classify_severity(dnbr_array):
    """Classify dNBR into USGS burn severity classes (0-4)."""
    severity = np.zeros_like(dnbr_array, dtype=np.uint8)
    severity[(dnbr_array >= 0.10) & (dnbr_array < 0.27)] = 1
    severity[(dnbr_array >= 0.27) & (dnbr_array < 0.44)] = 2
    severity[(dnbr_array >= 0.44) & (dnbr_array < 0.66)] = 3
    severity[dnbr_array >= 0.66] = 4
    return severity


SEVERITY_LABELS = ['Unburned', 'Low', 'Moderate', 'High', 'Very High']