"""Visualization helpers using PIL (matplotlib-free)."""

import numpy as np
from PIL import Image


SEVERITY_COLORS = {
    0: (34, 139, 34),
    1: (255, 255, 0),
    2: (255, 165, 0),
    3: (255, 0, 0),
    4: (139, 0, 0),
}


def severity_to_rgb(severity):
    """Convert classified severity (uint8, H x W) to RGB (H x W x 3)."""
    h, w = severity.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for value, color in SEVERITY_COLORS.items():
        rgb[severity == value] = color
    return rgb


def array_to_rgb(arr, vmin, vmax, mode='fire'):
    """Simple colormap: 'fire' or 'ndvi'."""
    norm = np.clip((arr - vmin) / (vmax - vmin + 1e-10), 0, 1)
    if mode == 'ndvi':
        norm = 1 - norm
    h, w = norm.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    rgb[..., 0] = (norm * 255).astype(np.uint8)
    rgb[..., 1] = ((1 - np.abs(norm - 0.5) * 2) * 255).astype(np.uint8)
    return rgb


def save_png(rgb_array, path):
    """Save an RGB numpy array as a PNG file."""
    Image.fromarray(rgb_array).save(str(path))