import pathlib

import numpy as np
import pandas as pd
import cartopy.crs as ccrs
from cartopy.feature import LAND

import matplotlib.pyplot as plt
from matplotlib.projections import PolarAxes
from matplotlib.ticker import AutoMinorLocator
from matplotlib.colors import ListedColormap
import mpl_toolkits.axisartist.floating_axes as fa
import mpl_toolkits.axisartist.grid_finder as gf

from .data import efficient_log
from .grid import GENIE_lat, GENIE_lon, GENIE_depth

# separate functions in plot_genie()

def scatter_map(
    df: pd.DataFrame,
    var,
    ax,
    x="Longitude",
    y="Latitude",
    add_layer=True,
    log=False,
    *args,
    **kwargs,
):
    """plot map based on dataframe with latitude/longitude
    using cartopy as engine

    :param df: pandas dataframe
    :param var: variable (column) in dataframe to plot
    :param x: coordinate attribute, default "Longitude"
    :param y: coordinate attribute, default "Latitude"
    :param add_layer: whether to add basic costal lines, and land feature

    :returns: a map
    """

    if add_layer:
        ax.set_global()
        ax.coastlines()
        ax.add_feature(
            LAND, zorder=0, facecolor="#B1B2B4", edgecolor="white"
        )  # zorder is drawing sequence

    if "Latitude" not in df.columns or "Longitude" not in df.columns:
        raise ValueError("Input data lack Latitude/Longitude column")

    if log:
        df[var] = efficient_log(df[var])

    p = ax.scatter(
        x=df[x],
        y=df[y],
        c=df[var],
        linewidths=0.5,
        edgecolors="black",
        transform=ccrs.PlateCarree(),
        *args,
        **kwargs,
    )

    return p


def genie_cmap(cmap_name, N=256, reverse=False):
    """
    Get a self-defined colormap

    :param cmap_name: Zissou1, FantasticFox, Rushmore, Darjeeling, ODV
    :type cmap_name: str

    :returns: colormap
    """
    file_name = f"data/{cmap_name}.txt"
    file_path = pathlib.Path(__file__).parent.parent / file_name

    colors = pd.read_csv(file_path, header=None).values.tolist()
    colors = [colors[i][0] for i in range(len(colors))]

    c = ListedColormap(colors, N=N)

    if reverse:
        return c.reversed()
    return c


def cbar_wrapper(plotting_func):
    """a decorator to add color bar

    :param plotting_func: function returning a mappable object
    :returns: plotting function with colorbar
    """

    def wrappered_func(*args, **kwargs):
        p = plotting_func(*args, **kwargs)
        cbar = plt.colorbar(p, fraction=0.05, pad=0.04, orientation="horizontal")
        cbar.ax.tick_params(color="k", direction="in")
        cbar.outline.set_edgecolor('black')
        cbar.minorticks_on()

    return wrappered_func

## TODO: add more layers: quiver,

## colorbar option
## mask basin option

class GeniePlottable:

    transform_crs = ccrs.PlateCarree()  # do not change

    grid_dict = {
    "lon": GENIE_lon(edge=False),
    "lat": GENIE_lat(edge=False),
    "zt":GENIE_depth(edge=False)/1000,

    "lon_edge": GENIE_lon(edge=True),
    "lat_edge": GENIE_lat(edge=True),
    "zt_edge": GENIE_depth(edge=True)/1000,
    }

    def __init__(self, array, dim):
        self.array = array
        self.dim = dim

    def plot_1d(self, ax=None, x=None, *args, **kwargs):
        """plot 1D data, e.g., zonal_average, time series
        x: time/lon/lat
        """

        if not x:
            fig, ax = self._init_fig()
            self._set_borderline(ax, geo=False, width=0.8)
            ax.grid(which='major', color='#DDDDDD', linewidth=0.8)
            ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
            ax.tick_params(axis="both", direction="out", which="both", left=True, top=True, bottom=True, right=True)
            ax.minorticks_on()
            p = ax.plot(self.array, *args, **kwargs)
        else:
            p = ax.plot(x, self.array, *args, **kwargs)

        return p

    @cbar_wrapper
    def plot_map(self, ax=None, x_edge="lon_edge", y_edge="lat_edge", contour=False, *args, **kwargs):

        if not ax:
            fig, ax = self._init_fig(subplot_kw={'projection': ccrs.EckertIV()})

        x_edge_arr = self.grid_dict.get(x_edge)
        y_edge_arr = self.grid_dict.get(y_edge)

        self._set_facecolor(ax)
        self._set_borderline(ax)
        p = self._add_pcolormesh(ax, x_edge=x_edge_arr, y_edge=y_edge_arr, transform=self.transform_crs, *args, **kwargs)
        self._add_outline(ax, x_edge=x_edge_arr, y_edge=y_edge_arr,  transform=self.transform_crs)

        if contour:
            x_arr = self.grid_dict.get(x_edge[:3:1])
            y_arr = self.grid_dict.get(y_edge[:3:1])
            p = self._add_contour(ax, x=x_arr, y=y_arr, transform=self.transform_crs)

        return p

    @cbar_wrapper
    def plot_polar(self, ax=None, hemisphere="South", x_edge="lon_edge", y_edge="lat_edge", contour=False, *args, **kwargs):

        if not ax:
            match hemisphere:
                case "North":
                    fig, ax = self._init_fig(subplot_kw={'projection': ccrs.Orthographic(0, 90)})
                case "South":
                    fig, ax = self._init_fig(subplot_kw={'projection': ccrs.Orthographic(180, -90)})

        x_edge_arr = self.grid_dict.get(x_edge)
        y_edge_arr = self.grid_dict.get(y_edge)

        self._set_facecolor(ax)
        self._set_borderline(ax)
        p = self._add_pcolormesh(ax, x_edge=x_edge_arr, y_edge=y_edge_arr, transform=self.transform_crs, *args, **kwargs)
        self._add_outline(ax, x_edge=x_edge_arr, y_edge=y_edge_arr, transform=self.transform_crs)
        self._add_gridline(ax,
            transform=self.transform_crs,
            draw_labels=False,
            linewidth=0.5,
            color="gray",
            alpha=0.5,
            linestyle="-",
        )

        if contour:
            x_arr = self.grid_dict.get(x_edge[:3:1])
            y_arr = self.grid_dict.get(y_edge[:3:1])
            p = self._add_contour(ax, x=x_arr, y=y_arr, transform=self.transform_crs)

        return p

    @cbar_wrapper
    def plot_transection(self, ax=None, x_edge="lat_edge", y_edge="zt_edge", contour=False, *args, **kwargs):
        if not ax:
            fig, ax = self._init_fig(figsize=(5, 2.5))

        x_edge_arr = self.grid_dict.get(x_edge)
        y_edge_arr = self.grid_dict.get(y_edge)

        self._set_facecolor(ax)
        self._set_borderline(ax, geo=False)


        p = self._add_pcolormesh(ax, x_edge=x_edge_arr, y_edge=y_edge_arr, *args, **kwargs)
        self._add_outline(ax, x_edge=x_edge_arr, y_edge=y_edge_arr)
        ax.set_ylim(ax.get_ylim()[::-1])
        ax.set_xlabel(x_edge[:3:1], fontsize=13)
        ax.set_ylabel("Depth (km)", fontsize=12)

        if contour:
            x_arr = self.grid_dict.get(x_edge[:3:1])
            y_arr = self.grid_dict.get(y_edge[:3:1])
            p = self._add_contour(ax, x=x_arr, y=y_arr, linewidths=0.6, colors="black", linestyles="solid")
            ax.clabel(p, p.levels[::1], colors=["black"], fontsize=8.5, inline=False)

        return p


    ## ------- Below is implementations -------------------------

    def _init_fig(self, *args, **kwargs):
        self._init_style()
        return plt.subplots(dpi=120, *args, **kwargs)

    def _init_style(self):
        plt.rcParams['image.cmap'] = 'viridis'
        plt.rcParams['grid.linestyle'] = ':'
        plt.rcParams['figure.figsize'] = [4.0, 3.0]
        plt.rc('font', family='serif')
        plt.rc('xtick', labelsize='x-small')
        plt.rc('ytick', labelsize='x-small')

    def _add_pcolormesh(self, ax, x_edge, y_edge, *args, **kwargs):
        return ax.pcolormesh(
            x_edge,
            y_edge,
            self.array,
            shading="flat",
            *args,
            **kwargs
        )

    def _add_contour(self, ax, x, y, *args, **kwargs):
        cs = ax.contour(x, y, self.array, *args, **kwargs)
        # label every three levels
        ax.clabel(cs, cs.levels[::3], colors=["black"], fontsize=8, inline=False)
        return cs

    def _add_gridline(self, ax, *args, **kwargs):
        ax.gridlines(*args, **kwargs)

    def _set_borderline(self, ax, geo=True, width=1):
        if geo:
            ax.spines["geo"].set_edgecolor("black")
            ax.spines["geo"].set_linewidth(width)
        else:
            for direction in ['top','bottom','left','right']:
                ax.spines[direction].set_linewidth(width)
                ax.spines[direction].set_edgecolor("black")
                # vertical layer order
                ax.spines[direction].set_zorder(0)

    def _set_facecolor(self, ax):
        ax.patch.set_color("silver")

    def _add_outline(self, ax, x_edge, y_edge, *args, **kwargs):
        outline_color = "black"
        outline_width = 1
        mask_array = np.where(~np.isnan(self.array), 1, 0)

        Ny_edge = len(y_edge)
        Nx_edge = len(x_edge)
        # dimension of array
        Ny_array = Ny_edge - 1
        Nx_array = Nx_edge - 1
        # index of array
        Ny_index = Ny_array - 1
        Nx_index = Nx_array - 1

        # i stands for yitude index, j stands for xgitude index
        # e.g., mask_array[0, ] is Antarctic ice cap
        # i,j are for mask array and will be converted to x/y edge lines
        for i in range(Ny_array):
            for j in range(Nx_array):
                # compare with the right grid, and plot vertical line if different
                if j < Nx_index and mask_array[i, j] != mask_array[i, j + 1]:
                    ax.vlines(
                        x_edge[j + 1],
                        y_edge[i],
                        y_edge[i + 1],
                        color=outline_color,
                        linewidth=outline_width,
                        *args, **kwargs
                    )

                # connect the circular xgitude axis
                if j == Nx_index and mask_array[i, j] != mask_array[i, 0]:
                    ax.vlines(
                        x_edge[j + 1],
                        y_edge[i],
                        y_edge[i + 1],
                        color=outline_color,
                        linewidth=outline_width,
                        *args, **kwargs
                    )

                # compare with the above grid, and plot horizontal line if different
                if i < Ny_index and mask_array[i, j] != mask_array[i + 1, j]:
                    ax.hlines(
                        y_edge[i + 1],
                        x_edge[j],
                        x_edge[j + 1],
                        colors=outline_color,
                        linewidth=outline_width,
                        *args, **kwargs
                    )

    def plot_quiver(x,y):
        pass

class TaylorDiagram(object):
    """
    Taylor diagram.
    Plot model standard deviation and correlation to reference data in a single-quadrant polar plot,
    with r=stddev and theta=arccos(correlation).

    modified from Yannick Copin, https://gist.github.com/ycopin/3342888
    reference: https://matplotlib.org/stable/gallery/axisartist/demo_floating_axes.html
    """

    def __init__(
        self,
        fig=None,
        figscale=1,
        subplot=111,
        xmax=None,
        tmax=np.pi / 2,
        ylabel="Standard Deviation",
        rotation=None,
    ):

        """
        Set up Taylor diagram axes, i.e. single quadrant polar
        plot, using `mpl_toolkits.axisartist.floating_axes`.

        Parameters:

        * fig: input Figure or None
        * subplot: subplot definition
        * xmax: the length of radius, xmax can be 1.5* reference std
        """

        # --------------- tickers --------------------------
        # Correlation labels (if half round)
        cor_label = np.array([0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 1])

        # add the negative ticks if more than half round
        excess_theta = tmax - np.pi / 2
        if excess_theta > 0:
            cor_label = np.concatenate((-cor_label[:0:-1], cor_label))

        # convert to radian
        rad = np.arccos(cor_label)
        # tick location
        gl = gf.FixedLocator(rad)
        # tick formatting: bind radian and correlation coefficient
        tf = gf.DictFormatter(dict(zip(rad, map(str, cor_label))))

        # --------------- coordinate -----------------------
        # Standard deviation axis extent (in units of reference stddev)
        # xmin must be 0, which is the centre of round

        self.xmin = 0
        self.xmax = xmax
        self.tmax = tmax

        # ------- curvilinear coordinate definition -------
        # use built-in polar transformation (i.e., from theta and r to x and y)
        tr = PolarAxes.PolarTransform()
        ghelper = fa.GridHelperCurveLinear(
            tr,
            extremes=(0, self.tmax, self.xmin, self.xmax),
            grid_locator1=gl,
            tick_formatter1=tf,
        )

        # ------- create floating axis -------
        if fig is None:
            fig_height = 4.5 * figscale
            fig_width = fig_height * (1 + np.sin(excess_theta))
            fig = plt.figure(figsize=(fig_width, fig_height), dpi=100)

        ax = fa.FloatingSubplot(fig, subplot, grid_helper=ghelper)
        fig.add_subplot(ax)

        # Adjust axes
        # Angle axis
        ax.axis["top"].label.set_text("Correlation")
        ax.axis["top"].toggle(ticklabels=True, label=True)
        # inverse the direction
        ax.axis["top"].set_axis_direction("bottom")
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].label.set_axis_direction("top")

        # X axis
        ax.axis["left"].set_axis_direction("bottom")

        # Y axis direction & label
        ax.axis["right"].toggle(all=True)
        ax.axis["right"].label.set_text(ylabel)
        ax.axis["right"].set_axis_direction("top")
        # ticklabel direction
        ax.axis["right"].major_ticklabels.set_axis_direction("left")

        ax.axis["bottom"].set_visible(False)

        # ------- Set instance attribute ----------
        self.fig = fig
        # Graphical axes
        self._ax = ax
        # grid line
        self._ax.grid(True, zorder=0, linestyle="--")
        # aspect ratio
        self._ax.set_aspect(1)
        # A parasite axes for further plotting data
        self.ax = ax.get_aux_axes(tr)
        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = []

    def add_ref(self, refstd, reflabel="Observation", linestyle="-", color="k"):
        """add a reference point"""
        self.refstd = refstd
        # Add reference point
        # slightly higher than 0 so star can be fully seen
        l = self.ax.plot(0.01, self.refstd, "k*", ls="", ms=10)
        # xy for the point, xytext for the text (the coordinates are
        # defined in xycoords and textcoords, respectively)
        self.ax.annotate(
            reflabel,
            xy=(0.01, self.refstd),
            xycoords="data",
            xytext=(-25, -30),
            textcoords="offset points",
        )
        # add stddev contour
        t = np.linspace(0, self.tmax)
        r = np.zeros_like(t) + self.refstd
        self.ax.plot(t, r, linestyle=linestyle, color=color)
        self.samplePoints.append(l)

    def add_scatter(self, stddev, corrcoef, *args, **kwargs):
        """
        Add sample (*stddev*, *corrcoeff*) to the Taylor
        diagram. *args* and *kwargs* are directly propagated to the
        `Figure.plot` command.
        """

        l = self.ax.scatter(
            np.arccos(corrcoef), stddev, *args, **kwargs
        )  # (theta, radius)
        self.samplePoints.append(l)

        return l

    def add_contours(self, levels=5, **kwargs):
        """
        Add constant centered RMS difference contours, defined by *levels*.
        """

        rs, ts = np.meshgrid(
            np.linspace(self.xmin, self.xmax), np.linspace(0, self.tmax)
        )
        # Compute centered RMS difference
        crmse = np.sqrt(self.refstd**2 + rs**2 - 2 * self.refstd * rs * np.cos(ts))
        contours = self.ax.contour(ts, rs, crmse, levels, linestyles="--", **kwargs)
        self.ax.clabel(contours, contours.levels[::1], inline=False)

        return contours

    def add_legend(self, *args, **kwargs):
        return self.ax.legend(*args, **kwargs)

    def add_annotation(self, *args, **kwargs):
        return self.ax.annotation(*args, **kwargs)

    def savefig(self, *args, **kwargs):
        self.fig.savefig(*args, **kwargs)
