"""
Run this on your machine:
    python extract_ncep.py

Reads a NCEP NetCDF file and writes a compressed JSON file
(ncep_data.json.gz) containing subsampled temperature data.

Requirements:
    pip install xarray netCDF4 numpy
"""

import xarray as xr
import numpy as np
import json
import gzip
import base64
import os

# ── FILES ─────────────────────────────────────────────
NC_FILE = "data.nc"
OUT_FILE = "ncep_data.json.gz"

# ── GRID SUBSAMPLING (reduce size) ────────────────────
LAT_STRIDE = 2
LON_STRIDE = 2

print(f"Opening {NC_FILE}...")

# disable datetime decoding (avoids warnings with year 0001)
ds = xr.open_dataset(NC_FILE, decode_times=False)

print(ds)

# ── SELECT AIR VARIABLE ───────────────────────────────
air = ds["air"]

# handle datasets that contain pressure levels
if "level" in air.dims:
    print("Dataset has pressure levels → selecting level 0")
    air = air.isel(level=0)

# now air should be (time, lat, lon)
print("\nAir dimensions:", air.dims)

# coordinates
lats = ds["lat"].values[::LAT_STRIDE].astype(np.float32)
lons = ds["lon"].values[::LON_STRIDE].astype(np.float32)
times = ds["time"].values

print(f"\nOriginal shape: {air.shape}")
print(f"Subsampled grid: {len(lats)} lat × {len(lons)} lon")

# ── SUBSAMPLE GRID ────────────────────────────────────
air_sub = air.values[:, ::LAT_STRIDE, ::LON_STRIDE].astype(np.float32)

# ── UNIT CONVERSION (Kelvin → Celsius) ────────────────
sample_val = float(air_sub[0, len(lats)//2, len(lons)//2])
print(f"Sample value: {sample_val}")

if sample_val > 100:
    print("Detected Kelvin → converting to Celsius")
    air_sub -= 273.15
else:
    print("Already Celsius")

# ── TIME STRINGS ──────────────────────────────────────
time_strs = [str(t)[:7] for t in times]
print(f"Time range: {time_strs[0]} → {time_strs[-1]} ({len(time_strs)} steps)")

# ── GLOBAL RANGE ──────────────────────────────────────
gmin = float(np.nanmin(air_sub))
gmax = float(np.nanmax(air_sub))

print(f"Temperature range: {gmin:.2f} → {gmax:.2f} °C")

# ── QUANTISE TO UINT8 ─────────────────────────────────
span = gmax - gmin
u8 = np.round((air_sub - gmin) / span * 255).clip(0, 255).astype(np.uint8)

# ── BASE64 ENCODE ─────────────────────────────────────
b64 = base64.b64encode(u8.tobytes()).decode("ascii")
print(f"Encoded size (before compression): {len(b64)/1e6:.2f} MB")

payload = {
    "lats": [round(float(v), 4) for v in lats],
    "lons": [round(float(v), 4) for v in lons],
    "times": time_strs,
    "tmin": round(gmin, 4),
    "tmax": round(gmax, 4),
    "nlat": len(lats),
    "nlon": len(lons),
    "nt": len(time_strs),
    "data_b64": b64
}

# ── WRITE COMPRESSED JSON ─────────────────────────────
json_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")

with gzip.open(OUT_FILE, "wb", compresslevel=9) as f:
    f.write(json_bytes)

raw_mb = len(json_bytes) / 1e6
gz_mb = os.path.getsize(OUT_FILE) / 1e6

print("\nOutput sizes:")
print(f"JSON raw: {raw_mb:.2f} MB")
print(f"Gzip:     {gz_mb:.2f} MB")

print(f"\nDone! File written: {OUT_FILE}")

# ── SANITY CHECK ──────────────────────────────────────
print("\nSpot checks:")

spots = [
    ("1948-01", "New York", 40.7, 286.0),
    ("2000-07", "Moscow", 55.8, 37.6),
    ("2023-01", "Sydney", -33.9, 151.2),
]

for t_str, name, la, lo in spots:
    if t_str not in time_strs:
        continue

    ti = time_strs.index(t_str)
    li = int(np.argmin(np.abs(lats - la)))
    lj = int(np.argmin(np.abs(lons - lo)))

    decoded = gmin + (int(u8[ti, li, lj]) / 255) * span

    print(f"{name} ({t_str}): {decoded:.1f} °C")

ds.close()
