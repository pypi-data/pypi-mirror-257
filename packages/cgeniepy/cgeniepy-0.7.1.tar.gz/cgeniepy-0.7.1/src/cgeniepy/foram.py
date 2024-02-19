import numpy as np
from functools import reduce
from . import ureg
from .chem import molecular_weight

from .ecology import PlanktonBiomass, PlanktonExport
from .model import GenieVariable, GenieModel
from .data import foram_groups, obs_data
from .scores import ModelSkill
from .fd import modern_foram_community
from .grid import GENIE_grid_area


class ForamModel(GenieModel):
    """A further customized GenieModel subclass"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def select_foramtype(self, foram_type, *args, **kwargs):
        "a optimised version of get_var, can be int or a list/tuple"
        return ForamType(foram_type=foram_type, model_path=self.model_path,  *args, **kwargs)

    def select_foram_community(self, abundance="relative_abundance", time_index=-1):
        bn = self.select_foramtype("bn")._run_method(abundance).isel(time=time_index).array.values
        bs = self.select_foramtype("bs")._run_method(abundance).isel(time=time_index).array.values
        sn = self.select_foramtype("sn")._run_method(abundance).isel(time=time_index).array.values
        ss = self.select_foramtype("ss")._run_method(abundance).isel(time=time_index).array.values
        return modern_foram_community(bn, bs, sn, ss)


    def calcite(self,  *args, **kwargs):
        export_C_var = self.export(element="C").full_varstr
        return ForamCalcite(foram_type = self.foram_type, var=export_C_var, model_path=self.model_path,  *args, **kwargs)

    def relative_abundance(self, element="C",  *args, **kwargs):
        biomass_var = self.biomass(element=element).full_varstr
        return ForamAbundance(foram_type = self.foram_type, var=biomass_var, model_path=self.model_path,  *args, **kwargs)

    def _run_method(self, method: str, *args, **kwargs):
        return getattr(self, method)(*args, **kwargs)

class ForamBiomass(PlanktonBiomass):
    obs = "net"

    def __init__(self, foram_type, element, model_path,  *args, **kwargs):
        self.foram_type = foram_type
        # convert foram type to pft index
        
        # pass pft_index to father class
        super().__init__(pft_index = self.pft_index,
                         element=element,
                         model_path=model_path,
                         *args, **kwargs)

    def compare_obs(self, **kwargs):
        if "obs" in kwargs:
            data = obs_data(source = kwargs["obs"], var=self.foram_type)
        else:
            data = obs_data(source = self.obs, var=self.foram_type)

        if "mask_MedArc" in kwargs:
            return ModelSkill(model=self.pure_array(), observation=data, mask_MedArc=kwargs["mask_MedArc"])
        else:
            return ModelSkill(model=self.pure_array(), observation=data)


class ForamExport(PlanktonExport):
    obs = "trap"

    def __init__(self, foram_type, element, model_path,  *args, **kwargs):
        self.foram_type = foram_type
        # convert foram type to pft index
        if isinstance(self.foram_type, list) or isinstance(self.foram_type, tuple):
            self.pft_index = [foram_groups().get(foram)[0] for foram in self.foram_type]
        else:
            self.pft_index = foram_groups()[self.foram_type][0]
        # pass pft_index to father class
        super().__init__(pft_index = self.pft_index,
                         element=element,
                         model_path=model_path,  *args, **kwargs)

    def compare_obs(self, **kwargs):
        if "obs" in kwargs:
            data = obs_data(source = kwargs["obs"], var=self.foram_type)
        else:
            data = obs_data(source = self.obs, var=self.foram_type)

        if "mask_MedArc" in kwargs:
            return ModelSkill(model=self.pure_array(), observation=data, mask_MedArc=kwargs["mask_MedArc"])
        else:
            return ModelSkill(model=self.pure_array(), observation=data)


class ForamCalcite(GenieVariable):

    unit = "mmol m$^-2$ d$^-1$"

    def __init__(self, foram_type, *args, **kwargs):
        self.foram_type = foram_type
        super().__init__(*args, **kwargs)

    def _set_array(self):
        """
        convert POC to Calcite (in mmol m-2 d-1) given POC:PIC:CaCO3 mol ratio = 100:36:36 (mass ratio = 100:36:300)
        """
        array = super()._set_array() * 0.36
        return array

    @ureg.with_context("bgc")
    def sum(self):
        CaCO3 = molecular_weight("CaCO3")
        c = self.uarray().to_base_units()
        v = GENIE_grid_area().to_base_units()
        s = c * v
        s = (
            s.to("mol d^-1")
            .to("g d^-1", "bgc", mw=CaCO3 * ureg("g/mol"))
            .to("Gt yr^-1")
        )

        return np.nansum(s)


class ForamAbundance(GenieVariable):
    obs = "coretop"

    def __init__(self, foram_type, *args, **kwargs):
        self.foram_type = foram_type
        # setting data with passed arguments
        super().__init__(*args, **kwargs)        

    def _total_foram(self):
        "if total foram is ptf No.16 to 19"
        # get the source data
        gm = GenieModel(model_path=self.model_path)
        path2nc = gm._auto_find_path(var=self.var)
        src_data = gm._open_nc(path2nc)

        # get all the foram variables
        # variable_template is the "eco2D_XXXX" format
        variable_template = self.var[:-2]
        foram_variables = [variable_template + str(i) for i in range(16, 20)]

        # use foram variables to get data
        target_data = []
        for i in foram_variables:
            target_data.append(src_data[i])

        # filter for each foram
        if hasattr(self, 'threshold'):
            for i, idata in enumerate(target_data):
                x = idata.values.copy()
                np.putmask(x, x < self.threshold, 0)
                target_data[i] = x
        
        total_foram = reduce(np.add, target_data)

        return total_foram

    def _set_array(self):
        # one foram
        one_foram = super()._set_array()

        # total foram
        total_foram = self._total_foram()

        # ignore divided by 0
        # and set grid with total_foram == 0 to 0 instead of NA
        with np.errstate(divide="ignore", invalid="ignore"):
            proportion = np.divide(
                one_foram,
                total_foram,
                out=np.zeros_like(one_foram),
                where=total_foram != 0,
            )

        return proportion

    def compare_obs(self, **kwargs):
        if "obs" in kwargs:
            data = obs_data(source = kwargs["obs"], var=self.foram_type)
        else:
            data = obs_data(source = self.obs, var=self.foram_type)

        if "mask_MedArc" in kwargs:
            return ModelSkill(model=self.pure_array(), observation=data, mask_MedArc=kwargs["mask_MedArc"])
        else:
            return ModelSkill(model=self.pure_array(), observation=data)


def scd(x, y):
    """
    squared chord distance to represent dissimilarity between
    the communities in different time. SCD ranges from 0 to 2, with
    0 meaning identical, and 2 most different.
    
    :parameter
    x: assemblage in numpy array
    y: assemblage in numpy array

    Example
    x = np.array([sp1, sp2, ..., sp_n])
    y = np.arra([sp1, sp2, ..., sp_n])
    scd(x, y)
    """

    x_sqrt = np.sqrt(x)
    y_sqrt = np.sqrt(y)
    scd = np.sum(np.square(x_sqrt - y_sqrt), axis=0)

    ga = GenieArray()
    ga.array = scd
    return ga        
