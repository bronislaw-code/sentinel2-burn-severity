"""Visualization helpers using PIL (matplotlib-free, cross-platform safe)."""

import numpy as np
from PIL import Image


SEVERITY_COLORS = {
    0: (34, 139, 34),    # Unburned  — green
    1: (255, 255, 0),    # Low       — yellow
    2: (255, 165, 0),    # Moderate  — orange
    3: (255, 0, 0),      # High      — red
    4: (139, 0, 0),      # Very High — dark red
}


def severity_to_rgb(severity: np.ndarray) -> np.ndarray:
    """Convert classified severity (uint8, H×W) to RGB (H×W×3)."""
    h, w = severity.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for value, color in SEVERITY_COLORS.items():
        rgb[severity == value] = color
    return rgb


def array_to_rgb(arr: np.ndarray, vmin: float, vmax: float,
                 mode: str = 'fire') -> np.ndarray:
    """Simple colormap without matplotlib.

    mode='fire' → green → yellow → red (for dNBR)
    mode='ndvi' → red   → yellow → green (inverted, for dNDVI)
    """
    norm = np.clip((arr - vmin) / (vmax - vmin + 1e-10), 0, 1)
    if mode == 'ndvi':
        norm = 1 - norm
    h, w = norm.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    rgb[..., 0] = (norm * 255).astype(np.uint8)
    rgb[..., 1] = ((1 - np.abs(norm - 0.5) * 2) * 255).astype(np.uint8)
    return rgb


def save_png(rgb_array: np.ndarray, path) -> None:
    """Save an RGB numpy array as a PNG file."""
    Image.fromarray(rgb_array).save(str(path))