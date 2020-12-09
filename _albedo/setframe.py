import _albedo.horizonmethods as horizonmethods
import param
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import panel as pn
from datetime import timedelta
import numpy.ma as ma
import numpy as np

class SetFrame(horizonmethods.HorizonMethods):
    
    @param.depends('date')
    def set_dataframe(self):
        self.dataframe = self.sun_position()
        filler = filler = ['' for i in range(len(self.dataframe))]
        self.dataframe.insert(7, 'bin_assignment', filler)
        self.date_string = self.enabledDays[self.date].strftime("%Y-%m-%d")
        
        self.time_dict = {
            (t-timedelta(hours=self.UTC_offset)).strftime("%H:%M:%S"):index
            for index, t in enumerate(self.dataframe['UTC_datetime'])
        }
        
        self.param.time.objects = sorted(self.time_dict.values())
        self.param.time.names = self.time_dict
        return
    
    @param.depends('date', 'resolution', 'sigma', 'bins')
    def update_config(self):
        
        if self.bins != 'Max':
            bin_array       = np.linspace(0,360,self.bins,endpoint=True)
            real_azis       = self.dataframe['solarAzimuth'].to_numpy(copy=True)
            bin_assignment  = np.digitize(real_azis, bin_array)
            self.dataframe['bin_assignment'] = bin_assignment
            
            bin_angle = bin_array[1] # the angle width of a bin
            first_angle = bin_angle/2 
            last_angle = 360 - first_angle
            angle_array = np.linspace(first_angle, last_angle,
                                      self.bins-1, endpoint=True)
            self.angle_dict = dict(zip(np.arange(self.bins), angle_array))
            
        else:
            self.bin_dict = 'bins == Max: bin_dict not defined.'
        
        self.dictionary = {
            'Date': self.date_string,
            'Raster': {'Resolution': self.resolution,
                       'Geotransform': self.geotransform,
                       'Sigma': self.sigma,
                       'Vert Exag': self.vertEx
                      },
            'Azimuth': {'Count': self.bins,
                        'Bins': (bin_array.tolist()
                                 if self.bins != 'Max' else 'N/A')
                       }
        }        
        return 
    
    @param.depends('date', 'resolution', 'sigma', 'vertEx')
    def set_raster(self):
        self.elevRast, self.slopeRast, self.aspectRast = self.griddata_transforms()
        return
    
    def set_axes(self, figsize=(15,4), topMargin=0.9, 
                 bottomMargin=0.1, leftMargin=0.05, rightMargin=0.645):
        '''
        instantiates the axes for the timeSeries_Plot.
        broken into a separate function to reduce the line count for timeSeries_Plot
        '''
        fig = plt.figure(figsize=figsize)
        ax = host_subplot(111, axes_class=axisartist.Axes)
        
        par1 = ax.twinx()
        par2 = ax.twinx()
        par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(50, 0))
        par3 = ax.twinx()
        par3.axis["right"] = par3.new_fixed_axis(loc="right", offset=(100, 0))
        
        par1.axis["right"].toggle(all=True)
        par2.axis["right"].toggle(all=True)
        par3.axis["right"].toggle(all=True)
        
        ax.set_ylabel(r"$Radiation  (watts/m^2)$")
        par1.set_ylabel("M")
        par2.set_ylabel("Albedo")
        par3.set_ylabel(r"$Visible Surface (m^2)$")
        
        ax.set_ylim(0, 1200) #radiation y-range
        par1.set_ylim(0, 3) #terrain correction y-range
        par2.set_ylim(0.2, 0.8) #albedo y-range
        par3.set_ylim(0.0, 3.0) #vis% y-range
                
        ax.axis["left"].label.set_color('darkorange') #label color, radiation y-axis
        par1.axis["right"].label.set_color('darkmagenta') #label color, M y-axis
        par2.axis["right"].label.set_color('darkturquoise') #label color, Albedo y-axis
        par3.axis["right"].label.set_color('k') #label color, viz y-axis

        ax.margins(0, tight=True)
        plt.subplots_adjust(top=topMargin, bottom=bottomMargin,
                            left=leftMargin, right=rightMargin)
        ax.grid()
        par1.grid(alpha=0.5)
        
        self.fig, self.ax = fig, ax
        self.par1, self.par2, self.par3 = par1, par2, par3
        return
    
    @param.depends('date', 'time', 'resolution', 'sigma', 'vertEx')
    def set_m(self):
        self.m = self.M_calculation(df=self.dataframe, 
                                    row=self.time,
                                    choice='raster'
                                   )
        return
    
    @param.depends('date', 'time', 'resolution', 'sigma', 'vertEx')
    def set_masks(self):
        self.mask = self.rerotM_2()
        self.masked_elev = ma.masked_where(self.mask == 1, self.elevRast)
        self.masked_slope = ma.masked_where(self.mask == 1, self.slopeRast)
        self.masked_aspect = ma.masked_where(self.mask == 1, self.aspectRast)
        self.masked_m = ma.masked_where(self.mask == 1, self.m)
        return