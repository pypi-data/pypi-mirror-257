import numpy as np
from scipy.spatial import distance
from netCDF4 import Dataset
from .data import obs_data
from .grid import mask_Arctic_Med


def safe_unveil(model_data):
    "get pure array from a numpy masked array object"
    if model_data.__class__ != np.ma.core.MaskedArray:
        return model_data
    else:
        return model_data.filled(np.nan)


def intersect_index(array1, array2, verbose=False):
    """
    Return the index where corresponding values are not
    nan in both input arrays. One then can filter the array
    by the output boolean array.
    """

    # If both are not NaN, return it
    array1 = safe_unveil(array1)
    array2 = safe_unveil(array2)

    indx_array = np.logical_and(~np.isnan(array1), ~np.isnan(array2))

    if verbose is True:
        num = indx_array.flatten()[indx_array.flatten() == True].shape[0]
        print("Summary: {} elements simultaneously exist.".format(num))

    return indx_array


def cal_mscore(data1, data2):
    """
    Calculate skill metric M-score. See more in the paper Watterson, I. G. (1996)

    Use 2D array as input, order causes no difference.
    NA will be removed.

    :param data1: data to compare, order does not count
    :param data2: data to compare, order does not count

    :type data1: numpy array
    :type data2: numpy array

    :returns: A float number
    """
    # get common set
    indx = intersect_index(data1, data2)
    sub_data1 = data1[indx]
    sub_data2 = data2[indx]

    # calculate M-score
    mse = np.square(np.subtract(sub_data1, sub_data2)).mean()
    v1 = sub_data1.var()
    v2 = sub_data2.var()
    g1 = sub_data1.mean()
    g2 = sub_data2.mean()

    mscore = (2 / np.pi) * np.arcsin(1 - mse / (v1 + v2 + np.square(g1 - g2)))

    return mscore


def cal_corr(data1, data2):
    """
    calculate pearson correlation coefficient for 2D array
    """
    indx = intersect_index(data1, data2)
    sub_data1 = data1[indx].ravel()
    sub_data2 = data2[indx].ravel()

    corr = pearson_r(sub_data1, sub_data2)
    return corr


def cal_cosine_similarity(data1, data2):
    """
    Calculate metric cosine similarity of two input arrays.

    Use 2D array as input, order causes no difference.
    """
    indx = intersect_index(data1, data2)
    sub_data1 = data1[indx]
    sub_data2 = data2[indx]

    if sub_data1.mean() != 0 and sub_data2.mean() != 0:
        cos_sim = 1 - distance.cosine(sub_data1.flatten(), sub_data2.flatten())
    else:
        cos_sim = np.nan

    return cos_sim


def cal_rmse(data1, data2):
    """
    Calculate Root Mean Sqaure Error (rmse, or rmsd) between two input arrays.

    Use 2D array as input, order causes no difference.
    """

    error_2d = data1 - data2
    error_1d = error_2d.ravel()[~np.isnan(error_2d.ravel())]
    rmse = np.sqrt(np.square(error_1d).mean())

    return rmse


def cal_crmse(data1, data2):
    """
    Calculate centred Root Mean Sqaure Error (rmse, or rmsd) between two input arrays. See Talor, K. E. (2001) JGR

    Use 2D array as input, order causes no difference.
    """
    indx = intersect_index(data1, data2)
    sub_data1 = data1[indx].ravel()
    sub_data2 = data2[indx].ravel()

    sigma1 = np.std(sub_data1)
    sigma2 = np.std(sub_data2)
    corr = pearson_r(sub_data1, sub_data2)
    crmse = sigma1**2 + sigma2**2 - 2 * sigma1 * sigma2 * corr

    return crmse


def get_foram_prop(file_path, var):
    """
    Quick calculation of [modelled] relative abundance, based on carbon export flux
    because of little difference between biomass and export.

    :param file_path: an netcdf file with all foram-related varialbes
    :param var: foram group abbrev: bn, bs, sn, ss

    :returns: a scalar value
    """

    f = Dataset(file_path)

    bn = safe_unveil(f.variables["eco2D_Export_C_016"][-1, :, :])
    bs = safe_unveil(f.variables["eco2D_Export_C_017"][-1, :, :])
    sn = safe_unveil(f.variables["eco2D_Export_C_018"][-1, :, :])
    ss = safe_unveil(f.variables["eco2D_Export_C_019"][-1, :, :])

    total_foram = bn + bs + sn + ss

    # ignore divided by 0
    with np.errstate(divide="ignore", invalid="ignore"):
        one_foram = locals()[var]
        proportion = np.divide(
            one_foram, total_foram, out=np.zeros_like(one_foram), where=total_foram != 0
        )

    f.close()

    return proportion


def quick_rmse(model, obs_source, var, *args, **kwargs):
    "A wrapper function to calculate RMSE"

    if hasattr(model, "values"):
        model = model.values

    masked_model = mask_Arctic_Med(model, policy="na")
    masked_data = mask_Arctic_Med(
        obs_data(obs_source, var, *args, **kwargs), policy="na"
    )

    return cal_rmse(masked_model, masked_data)


def quick_mscore(model, obs_source, var, *args, **kwargs):
    "A wrapper function to calculate M-Score"

    if hasattr(model, "values"):
        model = model.values

    masked_model = mask_Arctic_Med(model, policy="na")
    masked_data = mask_Arctic_Med(
        obs_data(obs_source, var, *args, **kwargs), policy="na"
    )

    return cal_mscore(masked_model, masked_data)


def quick_cos_sim(model, obs_source, var, *args, **kwargs):
    "A wrapper function to calculate cosine cimilarity"
    if hasattr(model, "values"):
        model = model.values

    masked_model = mask_Arctic_Med(model, policy="na")
    masked_data = mask_Arctic_Med(
        obs_data(obs_source, var, *args, **kwargs), policy="na"
    )

    return cal_cosine_similarity(masked_model, masked_data)


def quick_corr(model, obs_source, var, *args, **kwargs):
    "A wrapper function to calculate Pearson's correlation coefficient"
    if hasattr(model, "values"):
        model = model.values
        masked_model = mask_Arctic_Med(model, policy="na")
        masked_data = mask_Arctic_Med(
            obs_data(obs_source, var, *args, **kwargs), policy="na"
        )

    return cal_corr(masked_model, masked_data)


def pearson_r(data1, data2):
    """
    compute pearson correlation coefficient, which reflect linear similarity between two 1D arrays

    :param data1: 1D array
    :param data2: 1D array
    """

    # Compute corr matrix
    corr_mat = np.corrcoef(data1, data2)
    return corr_mat[0, 1]
