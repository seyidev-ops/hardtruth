#!/usr/bin/env python3
"""Make a transparent-background cut-out of the hero book mockup.

The supplied thumbnail sits on a flat dark-brown ground (#160700). We remove only the
ground that is connected to the image border (so the dark author band on the cover is kept),
soften the edge, and decontaminate edge colours. Output: assets/the-house-book-cutout.png
"""
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
src = Image.open(ROOT / "assets" / "the-house-book-thumbnail.jpg").convert("RGB")
a = np.asarray(src).astype(np.float32)
bg = np.array([22, 7, 0], np.float32)
dist = np.sqrt(((a - bg) ** 2).sum(-1))

near = dist < 26                                   # candidate background
lab, _ = ndimage.label(near)
border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
border = border[border > 0]
ground = np.isin(lab, border)
# grow slightly so the soft edge ramp covers the anti-aliased rim
ground = ndimage.binary_dilation(ground, iterations=1)  # eat the 1px dark JPEG fringe
rim = ndimage.binary_dilation(ground, iterations=3) & ~ground

alpha = np.ones(dist.shape, np.float32)
alpha[ground] = 0.0
ramp = np.clip((dist - 16) / 40, 0, 1)
alpha[rim] = np.minimum(alpha[rim], ramp[rim])
# the original JPEG cast shadow is blocky; drop it (CSS draws a clean shadow instead)
alpha = ndimage.gaussian_filter(alpha, 0.7)
alpha[~(ground | rim)] = 1.0

# decontaminate: remove the brown ground bleeding into edge pixels
a_safe = np.clip(alpha, 1e-3, 1)[..., None]
rgb = np.clip((a - bg * (1 - a_safe)) / a_safe, 0, 255)
rgb[alpha < 0.6] = np.array([10, 5, 2])          # shadow pixels: neutral dark

out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
img = Image.fromarray(out, "RGBA")
bbox = img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
pad = 24
bbox = (max(bbox[0] - pad, 0), max(bbox[1] - pad, 0), min(bbox[2] + pad, img.width), min(bbox[3] + pad, img.height))
img = img.crop(bbox)
img.save(ROOT / "assets" / "the-house-book-cutout.png", optimize=True)
print("saved", img.size)
