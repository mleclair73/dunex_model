Worklog:
    
06/12/24
    Mission 32
        - SWAN timestep changed to 60s
        - Coupling timestep changed to 60s
        - Added ROLLER_SVENDSEN to dunex.h
            - Can only have one roller code active?
            - Or there's a bug with both
        - Changed cores to 10-WAV 30-OCN
            - NtileI == 5 NtileJ == 6
06/13/24
    Looking into output filesize. 
        - 3D files are big
        - Compression/Deflation seems to save a huge amount of space which makes sense, also possible changing shuffle could help with this?
        - NC_DLEVEL = 4 seems like the best (in agreement with some people online)
    Wrote scripts/compress_netcdf.py and scripts/profile_compression.py
    Trying to get an idea of what changing the parameters does to the results
    Set up git