import _albedo.rasterproducts as rasterproducts
import param
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class PlotMethods(rasterproducts.RasterProducts):
    
    @param.depends('run', 'modelComplete',
                   'date', 'elev', 'azim', 'choose3d')
    def axes3d(self, figsize=(6,6), topMargin=1.2, bottomMargin=0):
        if self.run==True and self.modelComplete == 'Incomplete':
            pass
        else:
            plt.close()
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection='3d')

            if self.choose3d:
                if 'Pointcloud' in self.choose3d:
                    xyz = self.datetime2xyz()
                    Easting, Northing, Elevation = xyz[:,0], xyz[:,1], xyz[:,2]
                    ax.scatter(Easting, Northing, Elevation, cmap='viridis', c=Elevation)

                if 'Planar Fit' in self.choose3d:
                    XYZ = self.pFit()
                    X, Y, Z = XYZ[:,:,0], XYZ[:,:,1], XYZ[:,:,2]
                    ax.plot_surface(X, Y, Z, color='r', rstride=1, cstride=1, alpha=0.5)

            ax.view_init(elev=self.elev, azim=self.azim)
            ax.set_xlim(320977, 320980)
            ax.set_xlabel('Easting')
            ax.set_ylim(4168144, 4168147)
            ax.set_ylabel('Northing')
            ax.set_zlim(2941.977, 2948.356)
            ax.set_zlabel('Elevation')
            plt.subplots_adjust(top=topMargin, bottom=bottomMargin) 
            plt.close()
            return fig
    
    @param.depends('run', 'modelComplete',
                   'date', 'resolution', 'sigma', 'vertEx',
                   'time', 'activateMask')
    def tryptic(self, figsize=(12,5), wspace=0.1, hspace=0, 
                leftMargin=0.05, rightMargin=1, topMargin=0.8, bottomMargin=0.1):
        if self.run==True and self.modelComplete=='Incomplete':
            pass
        else:
            plt.close()
            #fig = plt.figure(figsize=figsize)
            #grid = plt.GridSpec(1, 3, wspace=wspace, hspace=hspace)
            fig, ax = plt.subplots(1,3, figsize=figsize)
            
            ds = self.date_string
            titles = [f'{ds}: Elevation', f'{ds}: Slope',f'{ds}: Aspect']
            
            if self.activateMask == 'Overlay':
                imgs = [self.masked_elev, self.masked_slope, self.masked_aspect]
            elif self.activateMask == 'Remove':
                imgs = [self.elevRast, self.slopeRast, self.aspectRast]
            
            cmaps = ['viridis', 'YlOrBr', 'hsv']
            cmapRanges = [(np.min(self.elevRast), np.max(self.elevRast)),
                          (np.min(self.slopeRast), np.max(self.slopeRast)),
                          (-180, 180)]
            
            ims = []
            for i in range(3):
                img, cmap = imgs[i], cmaps[i]
                im = ax[i].imshow(img, origin='lower', cmap=cmap,
                                  vmin=cmapRanges[i][0], vmax=cmapRanges[i][1])
                ims.append(im)
                ax[i].set_aspect("equal")

            #plt.draw()
            plt.subplots_adjust(left=leftMargin, right=rightMargin,
                                top=topMargin, bottom=bottomMargin,
                                wspace=wspace, hspace=hspace)
            
            for i in range(3):
                p = ax[i].get_position().get_points().flatten()
                ax_cbar = fig.add_axes([p[0], 0.88, p[2]-p[0], 0.05])
                ax_cbar.set_title(titles[i], loc='left')
                plt.colorbar(ims[i], cax=ax_cbar, orientation='horizontal')
            
             
            plt.close()

            return fig
    
    @param.depends('run', 'modelComplete', 'date', 'time')
    def polarAxes(self, figsize=(4,4), topMargin=1, bottomMargin=0):
        if self.run==True and self.modelComplete=='Incomplete':
            pass
        else:
            dataframe = self.dataframe
            
            plt.close()
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection='polar')
            ax.set_title('sun position', fontsize=12)

            ax.set_theta_zero_location('N')
            ax.set_xticks(([np.deg2rad(0), np.deg2rad(45), np.deg2rad(90),
                            np.deg2rad(135), np.deg2rad(180), np.deg2rad(225),
                            np.deg2rad(270), np.deg2rad(315)]))
            xlbls = np.array(['N','45','E','135','S','225','W','315'])
            ax.set_xticklabels(xlbls, rotation="vertical", size=12)
            ax.tick_params(axis='x', pad = 0.5)
            ax.set_theta_direction(-1)

            ax.set_rmin(0)
            ax.set_rmax(90)
            ax.set_rlabel_position(90)

            xs, ys = dataframe['solarAzimuth'], dataframe['solarAltitude']
            xs, ys = np.deg2rad(xs), ys
            ax.scatter(xs,ys, s=10, c='orange',alpha=0.5)

            x, y = dataframe['solarAzimuth'].iloc[self.time], dataframe['solarAltitude'].iloc[self.time]
            x, y = np.deg2rad(x), y
            ax.scatter(x,y, s=500, c='gold',alpha=1)

            plt.subplots_adjust(top=topMargin, bottom=bottomMargin)
            plt.close()

            return fig 
        
    @param.depends('run', 'modelComplete',
                   'date', 'chooseTimeSeries', 
                   'resolution', 'sigma', 'vertEx')
    def timeSeries_Plot(self):
        '''
        plots a time series, given set of times and a tuple of y's.
        '''
        if self.run==True and self.modelComplete == 'Incomplete':
            pass
        else:
            fig, ax = self.fig, self.ax
            par1, par2 = self.par1, self.par2

            times = self.dataframe['UTC_datetime']

            df = self.dataframe
            vals, keys = [], ['downward looking', 'upward looking diffuse', 
                              'upward looking solar', 'M_planar', 'Albedo_planar']  
            for entry in keys:
                for col in df.columns:
                    if col.startswith(entry):
                        vals.append(df[col])            
            upGlobal, downDiffuse, downDirect, M_planar, Albedo_planar = vals    
            downDirect = downDirect - downDiffuse

            #meanM = self.meanM_list
            #maskedmeanM = self.maskedmeanM_list

            #meanAlpha = self.meanAlpha_list

            IDR_Recon_Planar = M_planar*downDirect
            #IDR_Recon_RasterMean = meanM*downDirect
            #TODO: radRecon_maskedmeanM = maskedmeanM*downDirect

            d = {'Rad_Meas: Global Up': [upGlobal, 'salmon'], 
                'Rad_Meas: Direct Down': [downDirect, 'orange'], 
                'Rad_Meas: Diffuse Down': [downDiffuse, 'peachpuff'],
                'M: Planar': [M_planar, 'mediumorchid'],
                #'M: Raster Mean': [meanM, 'indigo'], 
                #'M: Horizon Mean' : [maskedmeanM, 'green'],
                'Alpha: Planar': [Albedo_planar, 'darkturquoise'],
                #'Alpha: Raster Mean': [meanAlpha, 'darkcyan'],
                #'Albedo: Horizon Mean': [maskedmeanAlpha, 'orange'], 
                'IDR_Recon: Planar': [IDR_Recon_Planar, 'orange'], 
                #'IDR_Recon: Raster Mean': [IDR_Recon_RasterMean, 'red']#,
                #'Mean Raster M (Masked) Direct' 
                }

            #raw measurements
            ax_vals, ax_colors = [], []
            for series in self.chooseTimeSeries:
                if series.startswith('Rad') or series.startswith('IDR'):
                    ax_vals.append(d[series][0])
                    ax_colors.append(d[series][1])
            for ax_val, ax_color in zip(ax_vals, ax_colors):
                ax.plot(times, ax_val, c=ax_color)

            #terrain correction values
            par1_vals, par1_colors = [], []
            for series in self.chooseTimeSeries:
                if series.startswith('M'):
                    par1_vals.append(d[series][0])
                    par1_colors.append(d[series][1])
            for par1_val, par1_color in zip(par1_vals, par1_colors):
                par1.plot(times, par1_val, c=par1_color, alpha=0.6)

            #albedoes
            par2_vals, par2_colors = [], []
            for series in self.chooseTimeSeries:
                if series.startswith('Alpha'):
                    par2_vals.append(d[series][0])
                    par2_colors.append(d[series][1])
            for par2_val, par2_color in zip(par2_vals, par2_colors):
                par2.plot(times, par2_val, c=par2_color)

            #vertical time marker
            #ylims = ax.get_ylim()
            #ax.vlines(x=times.iloc[time], ymin=0, ymax=ylims[1],
            #          color='k', linestyles='dotted')

            plt.close()

            return fig
    
    @param.depends('run', 'modelComplete',
                   'date', 'time', 
                   'resolution', 'sigma', 'vertEx', 'activateMask')
    def plotMRaster(self, colormapRange=(0,2), figsize=(4,4), 
                    topMargin=0.95, bottomMargin=0.05, 
                    leftMargin=0.05, rightMargin=0.95):
        '''
        generates and plots a 'magma' themed M raster
        '''
        if self.run==True and self.modelComplete == 'Incomplete':
            pass
        else:
            plt.close()
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

            if self.activateMask == 'Overlay':
                img = self.masked_m
                ax.imshow(img, origin='lower', cmap='magma', 
                          vmin=colormapRange[0], vmax=colormapRange[1])
            elif self.activateMask == 'Remove':        
                img = self.m
                ax.imshow(img, origin='lower', cmap='magma', 
                          vmin=colormapRange[0], vmax=colormapRange[1])

            plt.subplots_adjust(top=topMargin, bottom=bottomMargin, 
                                left=leftMargin, right=rightMargin)
            plt.close()

            return fig
        
    @param.depends('run', 'modelComplete',
                   'date', 'time', 'resolution', 'sigma')
    def plotMask(self,figsize=(4,4), 
                 topMargin=0.95, bottomMargin=0.05, 
                 leftMargin=0.05, rightMargin=0.95):
        '''
        plots the direct rad shade mask for the given date & time
        '''
        if self.run==True and self.modelComplete == 'Incomplete':
            pass
        else:
            plt.close()
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

            img = self.mask

            ax.imshow(img, origin='lower', cmap='binary')

            plt.subplots_adjust(top=topMargin, bottom=bottomMargin, 
                                left=leftMargin, right=rightMargin)
            plt.close()

            return fig   