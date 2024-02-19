import os
import sys
import urllib
import datetime as dt
from .utils import *
from .warnings import *


class MSWEP():
    """
    MSWEP class object for downloading and managing precipitation data of 
    Multi-Source Weighted-Ensemble Precipitation (MSWEP)
    """
    def __init__(self, root:str = ".") -> None:
        # Ignore warnings produced by Fiona Deprecation
        ignoreWarnings()
    
    def download(self, date:dt.datetime, timestep:str, dataset:str, outpath:str, 
                 extent:list = None) -> None:
        """
        Download MSWEP precipitation data

        Args:
            date: A datetime object representing the date.
            timestep: A string specifying the timestep: "3hourly","daily", "monthly".
            dataset: A string especifying the mswep dataset: "NTR", "Past", "Past_nogauge".
            outpath: A string specifying the path for output file.
            extent: An optional list specifying the extent.
        """
        # Validate timestep variable
        if timestep not in ["3hourly","daily", "monthly"]:
            err = "Invalid timestep. Please provide '3hourly', 'daily', or 'monthly'."
            raise ValueError(err)
        
        # Validate dataset variable
        if dataset not in ["NTR", "Past", "Past_nogauge"]:
            err = "Invalid dataset. Please provide 'NTR', 'Past', or 'Past_nogauge'."
            raise ValueError(err)
        
        # Validate extent variable
        if extent == None:
            extent = (90, -90, -180, 180)
        else:
            if not len(extent) == 4:
                err = "Invalid extent. Please provide a list with coordinates:"
                err = f"{err} 'north', 'south', 'east', 'west'"
                raise ValueError(err)
        
        # Determine filedate based on timestep
        if timestep == "3hourly":
            file_name = date.strftime('%Y%j.%H.nc')
        
        if timestep ==  "daily":
            file_name = date.strftime('%Y%j.nc')
            timestep = "Daily"
        
        if timestep == "monthly":
            file_name = date.strftime('%Y%m.nc')
            timestep = "Monthly"

        # Construct the command and download data
        cmd = "rclone sync -v --drive-shared-with-me GoogleDrive:/MSWEP_V280"
        cmd = f"{cmd}/{dataset}/{timestep}/{file_name} ./"
        outcmd = os.system(cmd)

        if not outcmd==0:
            err = "Error occurred while downloading: No exist data for selected date"
            raise(err)
        else:
            os.rename(file_name, "temporal.nc")

        # Parse NC to TIFF
        netcdf2TIFF("temporal.nc", var="precipitation", time=date.strftime("%Y-%m-%d %M:00"), 
                    isflip=False, correction=False)
        
        # Mask the raster file to required extent
        mask = createMask(north=extent[0], south=extent[1], 
                          east=extent[2], west=extent[3])
        raster, meta = maskTIFF("temporal.tif", mask)
        raster[raster<0] = np.nan
        writeRaster(raster, meta, path=outpath)
        
        # Remove the temporal file
        os.remove("temporal.tif")
        #os.remove("temporal.nc")

        # Print status mensages
        print(f"Downloaded CMORPH {timestep} file: {date}", end='\r')
        sys.stdout.flush()



