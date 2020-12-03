import _albedo.setmasks as setmasks
import param
import numpy as np

class RasterProducts(setmasks.SetMasks):
    '''
    @param.depends('dateIndex', 'resolution', 'sigma')
    def calc_meanM_list(self):
        col_count = self.dataframe.shape[0]
        meanM_list = []
        for row in range(0, col_count):
            img = self.M_calculation(df=self.dataframe, 
                                     row=row,
                                     choice='raster'
                                    )
            meanM = np.mean(img)
            meanM_list.append(meanM)
            self.meanM_list = meanM_list
        return 
    
    @param.depends('dateIndex', 'resolution', 'sigma',
                   'vertEx')
    def calc_meanAlpha_list(self):
        df = self.dataframe
        meanAlpha_list = []
        for row in range(0, df.shape[0]):
            meanAlpha_list.append(self.albedo(df, row, 
                                              choice = 'raster'))
            self.meanAlpha_list = meanAlpha_list
        return
    '''
    pass