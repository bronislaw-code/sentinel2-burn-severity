"""Spectral indices for burn severity and vegetation analysis."""

import numpy as np


def nbr(nir: np.ndarray, swir: np.ndarray) -> np.ndarray:
    """Normalized Burn Ratio.

    NBR = (NIR - SWIR) / (NIR + SWIR)

    Uses Sentinel-2 B08 (NIR) and B12 (SWIR 2190 nm).
    """
    return (nir - swir) / (nir + swir + 1e-10)


def dnbr(nbr_pre: np.ndarray, nbr_post: np.ndarray) -> np.ndarray:
    """Differenced NBR. Positive values indicate burned areas."""
    return nbr_pre - nbr_post


def ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """Normalized Difference Vegetation Index.

    NDVI = (NIR - RED) / (NIR + RED)

    Uses Sentinel-2 B08 (NIR) and B04 (RED).
    """
    return (nir - red) / (nir + red + 1e-10)


def classify_severity(dnbr_array: np.ndarray) -> np.ndarray:
    """Classify dNBR into USGS burn severity classes.

    Returns a uint8 array with values:
        0 = Unburned
        1 = Low        (0.10 – 0.27)
        2 = Moderate   (0.27 – 0.44)
        3 = High       (0.44 – 0.66)
        4 = Very High  (>= 0.66)
    """
    severity = np.zeros_like(dnbr_array, dtype=np.uint8)
    severity[(dnbr_array >= 0.10) & (dnbr_array < 0.27)] = 1
    severity[(dnbr_array >= 0.27) & (dnbr_array < 0.44)] = 2
    severity[(dnbr_array >= 0.44) & (dnbr_array < 0.66)] = 3
    severity[ dnbr_array >= 0.66]                        = 4
    return severity

def nbr2(swir1: np.ndarray, swir2: np.ndarray) -> np.ndarray:
    """Normalized Burn Ratio 2 (sensitive to soil moisture and char).

    NBR2 = (SWIR1 - SWIR2) / (SWIR1 + SWIR2)

    Uses Sentinel-2 B11 (SWIR 1610 nm) and B12 (SWIR 2190 nm).
    """
    return (swir1 - swir2) / (swir1 + swir2 + 1e-10)

SEVERITY_LABELS = ['Unburned', 'Low', 'Moderate', 'High', 'Very High']