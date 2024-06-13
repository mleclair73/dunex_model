#!/usr/bin/env python3
import xarray as xr
import sys
from rich.console import Console
import os
import warnings; warnings.simplefilter("ignore", category=xr.SerializationWarning) 
from time import perf_counter
from contextlib import contextmanager

@contextmanager
def catchtime():
    start = perf_counter()
    yield lambda: perf_counter() - start

def compress_to_netcdf(ds, out_fname, compression):
    comp = dict(zlib=True, complevel=compression)
    encoding = {var: comp for var in ds.data_vars}
    ds.to_netcdf(out_fname, encoding=encoding)

if __name__ == "__main__":
    console = Console()
    args = (sys.argv + [None] * 4)
    in_fname = args[1]
    out_fname = args[2]
    compression = args[3] or 4
    if in_fname is None:
        console.print('Usage:\n\tcompress_netcdf.py input [output: default input] [0-10: default 5]')
        exit(1)
    if out_fname is None:
        out_fname = in_fname
        
    with console.status(f"[bold yellow]Loading {in_fname}", spinner='earth') as status:
        with catchtime() as t:
            ds = xr.load_dataset(in_fname)
        in_time = t()

    in_size = os.path.getsize(in_fname)
    with console.status(f"[bold green]Compressing {in_fname} complevel={compression}", spinner='earth') as status:
        with catchtime() as t:
            compress_to_netcdf(ds, out_fname, compression)
        time = t()
    
    out_size = os.path.getsize(out_fname)
    
    with console.status(f"[bold yellow]Loading {out_fname}", spinner='earth') as status:
        with catchtime() as t:
            xr.load_dataset(out_fname)
        load = t()

    console.print(f'[bold green]Compressed File {in_fname}->{out_fname} complevel={compression}')
    console.print(f'[italic dark_cyan]Shrunk file by {(in_size-out_size)/in_size*100:.0f}%')
    console.print(f'[italic dark_cyan]Shortened loading time by {(in_time-load)/in_time*100:.0f}%')
    