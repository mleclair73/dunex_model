#!/usr/bin/env python3
import xarray as xr
import sys
from rich.console import Console
import os
import warnings; warnings.simplefilter("ignore", category=xr.SerializationWarning) 
from tempfile import NamedTemporaryFile
from time import perf_counter
from contextlib import contextmanager

@contextmanager
def catchtime():
    start = perf_counter()
    yield lambda: perf_counter() - start

def compress_to_netcdf(ds, out_fname, compression=5):
    comp = dict(zlib=True, complevel=compression)
    encoding = {var: comp for var in ds.data_vars}
    ds.to_netcdf(out_fname, encoding=encoding)

if __name__ == "__main__":
    console = Console()
    args = (sys.argv + [None] * 4)
    in_fname = args[1]
    if in_fname is None:
        console.print('Usage:\n\tprofile_compression.py input')
        exit(1)
        
    with console.status(f"[bold yellow]Loading {in_fname}", spinner='earth') as status:
        with catchtime() as t:
            ds = xr.load_dataset(in_fname)
        start_time = t()

    in_size = os.path.getsize(in_fname)

    with NamedTemporaryFile() as tmp:
        out_fname = tmp.name
        for i in range(0, 10):
            with console.status(f"[bold green]Compressing {in_fname} complevel={i}", spinner='earth') as status:
                with catchtime() as t:
                    compress_to_netcdf(ds, out_fname, i)
                time = t()
            
            out_size = os.path.getsize(out_fname)
            
            with console.status(f"[bold yellow]Loading {out_fname}", spinner='earth') as status:
                with catchtime() as t:
                    xr.load_dataset(out_fname)
                load = t()
            
            print(f'level={i}    filesize={out_size/1000/1000:.0f}mb   compression={(in_size-out_size)/in_size*100:.2f}%    time:{time:.2f}s   load:{load:.2f}s -- {(start_time-load)/start_time * 100:2f}% Faster')
