import pathlib

import numpy as np
import pandas as pd
import xarray as xr

from scipy.interpolate import (
    RegularGridInterpolator,
    LinearNDInterpolator,
    NearestNDInterpolator,
)
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class GridOperation:

    
    def lon_n2g(self, x):
        """
        Change parts of observational latitude [100, 180] to GENIE longitude [-260, -180]
        Note it isn't axisymmetric!
        """
        # TBD: add value range checker

        if x > 100 and x < 180:
            return x - 360
        else:
            return x

    def lon_g2n(self, x):
        """
        Change parts of observational latitude [100, 180] to GENIE longitude [-260, -180]
        CANNOT simply use +80, or -80! It isn't axisymmetric!
        """
        # TBD: add value range checker

        if x < -180:
            return x + 360
        else:
            return x

    def normalise_obs_lon(self, data: xr.Dataset) -> xr.Dataset:
        return data.assign_coords(
            {"lon": list(map(self.lon_n2g, data.lon.values))}
        ).sortby("lon")

    def normalise_GENIE_lon(self, data: xr.Dataset) -> xr.Dataset:
        """
        Change parts of observational latitude [100, 180] to GENIE longitude [-260, -180]
        """
        ## if hasattr(data, "assign_coords"):
        return data.assign_coords(
            {"lon": list(map(self.lon_g2n, data.lon.values))}
        ).sortby("lon")

    def mask_Arctic_Med(self, array, policy="na"):
        """
        mask Arctic and Meditterean Sea in cGENIE modern continent configuration
        """
        if policy == "na":
            array[34:36, :] = np.nan
            array[27:30, 25:30] = np.nan
        elif policy == "zero":
            array[34:36, :] = 0
            array[27:30, 25:30] = 0

        return array

    def GENIE_grid_mask(
        self, base="worjh2", basin="ALL", subbasin="", mask_Arc_Med=False, invert=False
    ):
        """
        Get a modern GENIE 36x36 mask array from input data.
        The input array is flipped (left/right flip -> up/down flip) for easy recognition

        :continent: worjh2, worlg4, worbe2, GIteiiaa, GIteiiaa, p0055c
        :basin: Atlantic/Pacific/Indian/ALL/Tanzania
        :subbasin: N/S/ALL, ALL means Southern Ocean section included

        :returns: GENIE grid array where continent/ice cap is 0 and ocean is 1, default is 'worjh2'
        """

        file_path = (
            pathlib.Path(__file__).parent.parent
            / f"data/mask_{base}_{basin}{subbasin}.txt"
        )
        grid_mask_raw = np.loadtxt(file_path, dtype=int)
        grid_mask = np.flip(np.fliplr(grid_mask_raw))

        if mask_Arc_Med:
            grid_mask = mask_Arctic_Med(grid_mask, policy="zero")

        if invert:
            grid_mask = ~grid_mask + 2

        return grid_mask

    def normal_lon(self, N=36, edge=False):
        """
        Normal longitude in 10 degree resolution,
        if edge is False, then return midpoint
        """
        if edge:
            lon_edge = np.linspace(-180, 180, N + 1)
            return lon_edge
        else:
            lon = np.linspace(-175, 175, N)
            return lon

    def regrid_lat(self, x):

        """
        Transform <latitude> into cGENIE resolution to facilitate comparison between
        model and observational data.
        """
        if x >= -90 and x <= 90:
            lat_edge = np.rad2deg(np.arcsin(np.linspace(-1, 1, 37)))
            lat = np.rad2deg(np.arcsin(np.linspace(-1, 1, 36)))

            for i in range(36):
                if x > lat_edge[i] and x <= lat_edge[i + 1]:
                    x = lat[i]
        else:
            raise ValueError("Latitude must be in [-90,90]")

        return x

    def regrid_lon(self, x):

        """
        Transform <longitude> into cGENIE resolution to facilitate comparison between
        model and observational data.
        """

        if x >= -180 and x <= 180:
            lon_edge = np.linspace(-180, 180, 37)
            for i in range(36):
                if x > lon_edge[i] and x <= lon_edge[i + 1]:
                    x = (lon_edge[i] + lon_edge[i + 1]) / 2  # middle value in the bin
        else:
            raise ValueError("Longitude must be in [-180,180]")

        return x

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the Haversine distance between two points.

        :param lat1: latitude of point 1
        :param lon1: longitude of point 1
        :param lat2: latitude of point 2
        :param lon2: longitude of point 2
        
        :returns: distance in km
        """
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        # Radius of the Earth in kilometers
        earth_radius = 6371.0
        distance = earth_radius * c

        return distance

    def geo_dis3d(self, point1, point2):
        """
        include the vertical distance

        :param point1: tuple/list of coordinates (z, lat, lon) or (lat, lon)
        :param point2: tuple/list of coordinates (z, lat, lon) or (lat, lon)
        :returns: distance in km
        """
        if len(point1) != 3 or len(point2) != 3:
            raise ValueError("Incompatible coordinates between two points")
        
        z1, lat1, lon1 = point1
        z2, lat2, lon2 = point2
        hor_dis = self.haversine_distance(lat1, lon1, lat2, lon2)
        ver_dis = abs(z1 - z2)/1000
        return np.sqrt(hor_dis**2 + ver_dis**2)

    def geo_dis2d(self, point1, point2):
        """
        include the vertical distance

        :param point1: tuple/list of coordinates (z, lon, lat) or (lon, lat)
        :param point2: tuple/list of coordinates (z, lon, lat) or (lon, lat)
        :returns: distance in km
        """
        if len(point1) != 2 or len(point2) != 2:
            raise ValueError("Incompatible coordinates between two points")
        
        lat1, lon1 = point1
        lat2, lon2 = point2
        return self.haversine_distance(lat1, lon1, lat2, lon2)


class Interporaltor:
    
    def __init__(self, dims, coordinates, values, grid_number=200, method="r-linear"):
        """
        initialize regridder

        :param array: xr data array or dataframe
        :param grid_number: number of target grid points
        :param method: interpolation method, only linear is supported
        """
        self.dims = dims
        self.coords = coordinates
        self.values = values

        ## number of grid points
        self.grid_number = grid_number
        ## create new coordinates
        self.gridded_coord = self.new_coordinate(n=grid_number)
        ## create meshgrid
        self.meshgrid = self.new_meshgrid(*self.gridded_coord, indexing="ij")
        ## interpolation function
        self.interp_function = self._create_interp_function(method=method)
        ## interpolate data
        self.gridded_data = self.interpolate_data(tuple(self.meshgrid))

    def _create_interp_function(self, method):
        """
        create interpolation function

        :param method: interpolation method, use "x-y" format. where x is strcutre or not, y is the algorithm
        """

        data_class = method.split("-")[0]
        ## regular grid interpolation
        if data_class == "r":
            true_method = method.split("-")[1]
            interp_function = RegularGridInterpolator(
                self.coords, self.values, method=true_method
            )
        ## irregular grid
        elif data_class == "ir":
            true_method = method.split("-")[1]
            if true_method == "linear":
                interp_function = LinearNDInterpolator(self.coords, self.values)
            elif true_method == "nearest":
                interp_function = NearestNDInterpolator(self.coords, self.values)
        else:
            raise ValueError("Method not supported")

        return interp_function

    def new_coordinate(self, n):
        "create new coordinates for regridding"
        new_coords = []
        for coord_values in self.coords:
            min_val, max_val = np.min(coord_values), np.max(coord_values)
            new_values = np.linspace(min_val, max_val, n)
            new_coords.append(new_values)
        return new_coords

    def new_meshgrid(self, *args, **kwargs):
        "regrid to finer dimensions"
        return np.meshgrid(*args, **kwargs)

    def interpolate_data(self, *args, **kwargs):
        "Use the interpolation function to get regridded values"
        return self.interp_function(*args, **kwargs)

    def to_xarray(self):
        """
        convert numpy array to xr data array
        """
        return xr.DataArray(
            self.gridded_data, dims=self.dims, coords=self.gridded_coord
        )
