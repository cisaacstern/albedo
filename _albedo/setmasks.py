import _albedo.horizonmethods as horizonmethods
import param
import numpy.ma as ma

class SetMasks(horizonmethods.HorizonMethods):
    
    @param.depends('date', 'time', 
                   'resolution', 'sigma', 'vertEx')
    def set_m(self):
        self.m = self.M_calculation(df=self.dataframe, 
                                    row=self.time,
                                    choice='raster'
                                   )
        return
    
    @param.depends('date', 'time', 
                   'resolution', 'sigma', 'vertEx')
    def set_masks(self):
        self.mask = self.rerotM_2()
        self.masked_elev = ma.masked_where(self.mask == 1, self.elevRast)
        self.masked_slope = ma.masked_where(self.mask == 1, self.slopeRast)
        self.masked_aspect = ma.masked_where(self.mask == 1, self.aspectRast)
        self.masked_m = ma.masked_where(self.mask == 1, self.m)
        return