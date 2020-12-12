import _albedo.plotmethods as plotmethods
import param
import time
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class RunModel(plotmethods.PlotMethods):
      
    def albedo(self, df, row, choice):
            '''
            '''
            for col in df.columns:
                if col.startswith('downward looking'):
                    D_up = df[col].iloc[row]
                if col.startswith('upward looking diffuse'):
                    D_down = df[col].iloc[row]
                if col.startswith('upward looking solar'):
                    B_down = df[col].iloc[row]
            B_down = B_down - D_down

            if choice == 'planar':
                c = df['M_planar'].iloc[row]
            elif choice == 'raster':
                c = df['raster_meanM'].iloc[row]
            elif choice == 'masked':
                c = df['maskedmeanM'].iloc[row]

            return D_up/((c*B_down)+D_down)
        
    @param.depends('run')
    def run_model(self): #formerly, calc_maskedmeanM_list
        if self.run == False:
            pass
        elif self.run == True:
            self.run_state = True
            start_t = time.time()
            
            #run log updates:
            k, v = list(self.dictionary.keys()), list(self.dictionary.values())
            const_key, const_values = k[0], v[0]
            config_key, config_values_dict = k[1], v[1]
            config_value_keys = list(config_values_dict.keys())
            config_value_vals = list(config_values_dict.values())

            date_key, date_val = config_value_keys[0], config_value_vals[0]
            raster_key, raster_vals = config_value_keys[1], config_value_vals[1]
            xgeo_key, xgeo_val = config_value_keys[2], config_value_vals[2]
            azi_key, azi_vals = config_value_keys[3], config_value_vals[3]
            self.log += f"""\nModel queued with config:
            {date_key}: {date_val}
            {raster_key}: {raster_vals}
            {xgeo_key}: {xgeo_val}
            {azi_key}: {list(azi_vals.keys())[0]}: {list(azi_vals.values())[0][0]}\n"""
            
            if self.bins != 'Max':
                bins = list(azi_vals.values())[0][1]
                vals = [str(np.around(val,1)) for val in bins]
                vals = [' '+val if len(val)==4 else val for val in vals]
                vals = ['  '+val if len(val)==3 else val for val in vals]
                newline = "\n"
                #print(f"""{ak[1]}: {newline}""")
                cycles = int((len(bins))/8)*8
                lines = ["            "+', '.join(vals[:8]) if c==0
                         else ', '.join(vals[c:c+8]) for c in range(0, cycles, 8)]
                tabbed_newline = newline+"            "
                self.log += f"""{tabbed_newline.join(lines)}"""
            else:
                pass
                    
            #runnnn!
            plt.close('all')                
            df = self.dataframe.copy(deep=True)
            ncols = self.dataframe.shape[0]
            self.progress.max = ncols-1
            self.log += '\nCopied dataframe'
            
            #PLANAR M
            self.p_slope, self.p_aspect = self.planar_slope_aspect()
            Mp_list = [self.M_calculation(df, row, choice='planar') 
                       for row in range(ncols)]
            df.insert(8, 'M_planar', Mp_list)

            #PLANAR ALBEDO
            Ap_list = [self.albedo(df, row, choice='planar')
                       for row in range(ncols)]
            df.insert(9, 'Albedo_planar', Ap_list)
            self.log += '\nAdded planar M and albedo to dataframe'

            #RASTER meanM
            meanM_list = [
                np.mean(
                    self.M_calculation(df=df, row=row, choice='raster')
                ) for row in range(ncols)
            ]
            df.insert(10, 'raster_meanM', meanM_list)

            #RASTER_mean_ALPHA
            meanAlpha_list = [
                self.albedo(df, row, choice = 'raster') 
                for row in range(ncols)
            ]
            df.insert(11, 'raster_meanALPHA', meanAlpha_list)
            self.log += """\nAdded raster M and albedo to dataframe
            Running horizon model...
            """            

            maskedmeanM_list, viz_percent_list = [], []
            
            self.img_arrays = []
            
            for index in range(ncols):
                plt.close('all')
                #trigger new raster set
                #  NOTE: I believe this cannot be easily converted
                #        to list comprehensions, given that it req-
                #        uires triggering this 'cascade' of state 
                #        rasters by indexing self.time parameter.
                self.time = index
                #calculate viz %
                unique, counts = np.unique(self.mask, return_counts=True)
                d = dict(zip(unique, counts))
                if 1.0 in d.keys():
                    vp = 1-(d[1.0]/(self.resolution**2)) #1.0 assigned to in-viz pts
                else:
                    vp = 1
                viz_percent_list.append(vp)
                
                ####MOVIE MADNESS#####
                
                t_arr, p_arr, d_arr = (self.triptych(), 
                                       self.polarAxes(),
                                       self.diptych())
                lower_set = np.hstack((t_arr, p_arr, d_arr))
                ts_array = self.timeSeries_Plot()
                img_array = np.vstack((ts_array, lower_set))
                
                self.img_arrays.append(img_array)
                
                if index == 0:
                    print('ts_array shape is ', ts_array.shape)
                    print('img_array shape is ', img_array.shape)
                    
                #calc masked M
                m = self.M_calculation(df, row=index, choice='masked')
                maskedmeanM = np.mean(m)
                maskedmeanM_list.append(maskedmeanM)
                #update progress bar
                self.progress.value = self.time
            
            self.log += 'Writing mp4...'
            
            ####MOVIE MADNESS#####
            # Set up formatting for the movie files
            fig2 = plt.figure(tight_layout=True, dpi=100)
            plt.axis('off')
            ims = [(plt.imshow(img),) for img in self.img_arrays]
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=5, metadata=dict(artist='Me'), bitrate=1800)
            im_ani = animation.ArtistAnimation(fig2, ims, interval=200, repeat_delay=3000, blit=False)
            im_ani.save('exports/animation.mp4', writer=writer)
            ####END MOVIE MADNESS#####
            
            df.insert(12, 'maskedmeanM', maskedmeanM_list)
            
            maskedAlbedo_list = [
                self.albedo(df, row, choice = 'masked')
                for row in range(ncols)
            ]
            df.insert(13, 'maskedAlbedo', maskedAlbedo_list)
            
            viz_percent_list = [item*3 for item in viz_percent_list] #norm-ing
            
            df.insert(14, 'viz_percent', viz_percent_list)
            
            del (Mp_list, Ap_list, meanM_list, meanAlpha_list, 
                 maskedmeanM_list, maskedAlbedo_list, viz_percent_list)

            self.log+='\nAdded horizon M, horizon albedo, and viz% to dataframe'
            self.time = 0
            self.model_dataframe = df
            end_t = time.time()
            run_t = np.around(end_t-start_t, 4)
            cell_t, ar_cs = np.around(run_t/ncols, 4), self.resolution**2
            unique_bins = (len(np.unique(df['bin_assignment'])) 
                           if self.bins!='Max' else ncols) 
                           
            
            self.log+=f"""<pre style="color:lime">\nModel completed in {run_t}s.
            {cell_t}s/timepoint for array of {ar_cs} cells @ {ncols} timepoints
            binned as {unique_bins} azimuths.
            </pre>
            """
            self.modelComplete = 'Complete'
            self.run_state = False

            return 
        