import _albedo.timeseries as timeseries
import param
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist


class SetFrame(timeseries.TimeSeries):
    
    @param.depends('dateIndex')
    def set_dataframe(self):
        self.dataframe = self.df_add_Ap()
        self.param.timePoint.bounds = (0, self.dataframe.shape[0]-1)
        return
    
    @param.depends('dateIndex', 'resolution', 'sigma', 'vertEx')
    def set_raster(self):
        self.elevRast, self.slopeRast, self.aspectRast = self.griddata_transforms()
        return
    
    def set_axes(self, figsize=(15,4), topMargin=0.95, 
                 bottomMargin=0.1, leftMargin=0.05, rightMargin=0.745):
        '''
        instantiates the axes for the timeSeries_Plot.
        broken into a separate function to reduce the line count for timeSeries_Plot
        '''
        fig = plt.figure(figsize=figsize)
        ax = host_subplot(111, axes_class=axisartist.Axes)
        
        par1 = ax.twinx()
        par2 = ax.twinx()
        par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(50, 0))
        par1.axis["right"].toggle(all=True)
        par2.axis["right"].toggle(all=True)
        ax.set_ylabel(r"$Radiation  (watts/m^2)$")
        par1.set_ylabel("Terrain Correction Factor")
        par2.set_ylabel("Albedo")
        
        ax.set_ylim(0, 1200) #radiation y-range
        par1.set_ylim(0, 3) #terrain correction y-range
        par2.set_ylim(0.1, 0.9) #albedo y-range
                
        ax.axis["left"].label.set_color('darkorange') #label color, radiation y-axis
        par1.axis["right"].label.set_color('darkmagenta') #label color, M y-axis
        par2.axis["right"].label.set_color('darkturquoise') #label color, Albedo y-axis

        ax.margins(0, tight=True)
        plt.subplots_adjust(top=topMargin, bottom=bottomMargin,
                            left=leftMargin, right=rightMargin)
        ax.grid()
        par1.grid(alpha=0.5)
        
        self.fig, self.ax = fig, ax
        self.par1, self.par2 = par1, par2
        return