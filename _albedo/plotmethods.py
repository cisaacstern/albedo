import _albedo.setframe as setframe
import param
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from datetime import timedelta

class PlotMethods(setframe.SetFrame):
    
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
    
    @param.depends('run', 'modelComplete', 'date', 'time', 
                   'resolution', 'sigma', 'vertEx', 'activateMask')
    def tryptich(self, figsize=(12,5), wspace=0.05, hspace=0, leftMargin=0.05, 
                 rightMargin=0.97, topMargin=0.79, bottomMargin=0.1):
        if self.run==True and self.modelComplete=='Incomplete':
            pass
        else:
            plt.close()
            fig, ax = plt.subplots(1,3, figsize=figsize)
            
            ds = self.date_string
            line2 = f'\nR, S, V ={(self.resolution,self.sigma,self.vertEx)}'

            titles = [f'{ds}: Elevation'+line2, f'{ds}: Slope'+line2,
                      f'{ds}: Aspect (South=0, East +)'+line2]
            
            if self.activateMask == 'Overlay':
                imgs = [self.masked_elev, self.masked_slope, self.masked_aspect]
            elif self.activateMask == 'Remove':
                imgs = [self.elevRast, self.slopeRast, self.aspectRast]
            
            cmaps = ['viridis', 'YlOrBr', 'hsv']
            cmapRanges = [(np.min(self.elevRast), np.max(self.elevRast)),
                          (np.min(self.slopeRast), np.max(self.slopeRast)),
                          (-180, 180)]
            
            ticks = np.linspace(0, self.resolution-1, 4)
            xlabels = [str(self.eastMin)[-2:], str(self.eastMin+1)[-2:],
                       str(self.eastMin+2)[-2:], str(self.eastMax)[-2:]]
            ylabels = [str(self.northMin)[-2:], str(self.northMin+1)[-2:],
                       str(self.northMin+2)[-2:], str(self.northMax)[-2:]]
            
            ims = []
            for i in range(3):
                img, cmap = imgs[i], cmaps[i]
                im = ax[i].imshow(img, origin='lower', cmap=cmap,
                                  vmin=cmapRanges[i][0], vmax=cmapRanges[i][1])
                ims.append(im)
                ax[i].set_xticks(ticks=ticks)
                ax[i].set_xticklabels(labels=xlabels)
                ax[i].set_yticks(ticks=ticks)
                if i == 0:
                    ax[i].set_yticklabels(labels=ylabels)
                    ax[i].set_ylabel(f'Northing (+{str(self.northMin)[:-2]}e2)')
                else:
                    ax[i].set_yticklabels(labels=[])
                if i == 1:
                    ax[i].set_xlabel(f'Easting (+{str(self.eastMin)[:-2]}e2)')
                ax[i].set_aspect("equal")

            plt.subplots_adjust(left=leftMargin, right=rightMargin,
                                top=topMargin, bottom=bottomMargin,
                                wspace=wspace, hspace=hspace)
            
            for i in range(3):
                p = ax[i].get_position().get_points().flatten()
                ax_cbar = fig.add_axes([p[0], 0.85, p[2]-p[0], 0.05])
                ax_cbar.set_title(titles[i], loc='left')
                cb = plt.colorbar(ims[i], cax=ax_cbar, orientation='horizontal')
                if i == 2:
                    cbar_ticks = [-180, -135, -90, -45, 0, 45, 90, 135, 180]
                    cb.set_ticks(cbar_ticks)
            
            plt.close()

            return fig
    
    @param.depends('run', 'modelComplete', 'date', 'time')
    def polarAxes(self, figsize=(3.5,5), topMargin=1, bottomMargin=0,
                  leftMargin=0.1, rightMargin=0.92):
        if self.run==True and self.modelComplete=='Incomplete':
            pass
        else:
            dataframe = self.dataframe
            
            plt.close()
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection='polar')
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

            x, y = (dataframe['solarAzimuth'].iloc[self.time], 
                    dataframe['solarAltitude'].iloc[self.time])
            
            self.dt_str = self.dataframe['MeasDateTime'].iloc[self.time]
            line1=f'{self.dt_str} Sun Position'
            line2=f'Azi, SZA={np.around((x,y),1)}, Bins={self.bins}'
            
            x, y = np.deg2rad(x), y
            ax.scatter(x,y, s=500, c='gold',alpha=1)
            
            plt.subplots_adjust(top=topMargin, bottom=bottomMargin,
                                left=leftMargin, right=rightMargin)
            
            p = ax.get_position().get_points().flatten()
            ax_cbar = fig.add_axes([p[0]+0.085, 0.85, p[2]-p[0], 0.05])
            ax_cbar.set_title(line1+'\n'+line2, loc='left')
            ax_cbar.axis('off')
            
            plt.close()

            return fig
        
    @param.depends('run', 'modelComplete', 'date', 'time', 
                   'resolution', 'sigma', 'vertEx', 'activateMask')
    def diptych(self, figsize=(8.25,5), topMargin=0.85, bottomMargin=0.05,
                leftMargin=0.095, rightMargin=0.95, wspace=0.1, hspace=0):
        '''
        generates and plots a 'magma' themed M raster and 
        the direct rad shade mask for the given date & time
        '''
        if self.run==True and self.modelComplete == 'Incomplete':
            pass
        else:
            plt.close()
            fig, ax = plt.subplots(1,2, figsize=figsize)
            
            line2 = f'\nR, S, V, Bins={(self.resolution,self.sigma,self.vertEx,self.bins)}'
            title1 = f'{self.dt_str}: Terrain Correction'+line2
            title2 = f'{self.dt_str}: Current Visibility'+line2
            titles = [title1, title2]
            
            if self.activateMask == 'Overlay':
                imgs = [self.masked_m, self.mask]
            elif self.activateMask == 'Remove':
                imgs = [self.m, self.mask]
            
            cmaps = ['magma', 'binary']
            cmapRanges = [(0,2), (0, 1)]
            
            ticks = np.linspace(0, self.resolution-1, 4)
            xlabels = [str(self.eastMin)[-2:], str(self.eastMin+1)[-2:],
                       str(self.eastMin+2)[-2:], str(self.eastMax)[-2:]]
            ylabels = [str(self.northMin)[-2:], str(self.northMin+1)[-2:],
                       str(self.northMin+2)[-2:], str(self.northMax)[-2:]]
            
            ims = []
            for i in range(2):
                img, cmap = imgs[i], cmaps[i]
                im = ax[i].imshow(img, origin='lower', cmap=cmap,
                                  vmin=cmapRanges[i][0], vmax=cmapRanges[i][1])
                ims.append(im)
                ax[i].set_xticks(ticks=ticks)
                ax[i].set_xticklabels(labels=xlabels)
                ax[i].set_yticks(ticks=ticks)
                if i == 0:
                    ax[i].set_yticklabels(labels=ylabels)
                    ax[i].set_ylabel(f'Northing (+{str(self.northMin)[:-2]}e2)')
                else:
                    ax[i].set_yticklabels(labels=[])
                if i == 0:
                    ax[i].set_xlabel(f'Easting (+{str(self.eastMin)[:-2]}e2)')
                ax[i].set_aspect("equal")
           
            plt.subplots_adjust(left=leftMargin, right=rightMargin,
                                    top=topMargin, bottom=bottomMargin,
                                    wspace=wspace, hspace=hspace)

            for i in range(2):
                p = ax[i].get_position().get_points().flatten()
                ax_cbar = fig.add_axes([p[0], 0.85, p[2]-p[0], 0.05])
                ax_cbar.set_title(titles[i], loc='left')
                cb = plt.colorbar(ims[i], cax=ax_cbar, orientation='horizontal')
                if i == 1:
                    cb.set_ticks([0, 1])
                    cb.set_ticklabels("Visible", "Shaded")

            plt.close()

            return fig
        
    @param.depends('modelComplete', 'date', 'chooseTimeSeries')
    def timeSeries_Plot(self):
        '''
        plots a time series, given set of times and a tuple of y's.
        '''
        if self.modelComplete == 'Incomplete':
            plt.close()
            fig, ax = self.fig, self.ax
            title = 'YYYY:MM:DD (sunrise - sunset); R, S, V, Bins= []'
            ax.set_title(title, loc='left')
            ax.text(x=-0.04, y=800, s="Current configuration not yet run.", 
                    fontsize=16)
            ax.text(x=-0.04, y=600, s="Run model to generate curves.", 
                    fontsize=30)
            plt.close()
            return fig
        else:
            plt.close()
            fig, ax = self.fig, self.ax
            
            t_dict = self.param.time.names
            sunrise_sunset = f'({list(t_dict)[0]}-{list(t_dict)[-1]})'
            line1 = f'{self.date_string} {sunrise_sunset};'
            line2 = f' R, S, V, Bins={[self.resolution,self.sigma,self.vertEx,self.bins]}'
            title = line1+line2
            ax.set_title(title, loc='left', fontsize=12)

            par1, par2 = self.par1, self.par2

            df = self.dataframe
            times = df['UTC_datetime'] - timedelta(hours=self.UTC_offset)
            time_labels = [t.strftime("%H:%M:%S") for t in times] #MY FIRST LIST COMPREHENSION :)
            time_labels[0] = ''
            ax.set_xticks(times[::4])
            ax.set_xticklabels(time_labels[::4])
            
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
            
            plt.close()

            return fig
        