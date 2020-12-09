import _albedo.plotmethods as plotmethods
import param
import numpy as np
import matplotlib.pyplot as plt
import time

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
            start_t = time.time()
            
            #run log updates:
            k, v = list(self.dictionary.keys()), list(self.dictionary.values())
            rk, rv = list(v[1].keys()), list(v[1].values())
            ak, av = list(v[2].keys()), list(v[2].values())
            self.log +=  f"""\nModel queued with config:
            {k[0]}: {v[0]}
            {k[1]}: {rk[0]}: {rv[0]}
                    {rk[1]}: {rv[1]}
                    {rk[2]}: {rv[2]}
                    {rk[3]}: {rv[3]}
            {k[2]}:{ak[0]}: {av[0]}
            """
            if self.bins != 'Max':
                bins = av[1]
                vals = [str(np.around(val,1)) for val in bins]
                vals = [' '+val if len(val)==4 else val for val in vals]
                vals = ['  '+val if len(val)==3 else val for val in vals]
                newline = "\n"
                self.log += f"""{ak[1]}: {newline}"""
                cycles = int((len(bins))/8)*8
                lines = ["            "+', '.join(vals[:8]) if c==0
                         else ', '.join(vals[c:c+8]) for c in range(0, cycles, 8)]
                tabbed_newline = newline+"            "
                self.log +=f"""{tabbed_newline.join(lines)}"""
            else:
                self.log +=f"""{ak[1]}: {av[1]}"""
                    
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
            
            #bin azimuths - generate a slope to horz reference set here
            '''
            gauss = dayList[3][:,:,1]
            referenceGrids, maskWaypoints = [], []
            '''
            #bins          = np.linspace(0,360,self.bins,endpoint=True)
            #aziVals       = df['solarAzimuth'].to_numpy(copy=True)
            #binAssignment = np.digitize(aziVals, bins)
            '''
            uniqueBins    = np.unique(binAssignment)

            aziStarter = bins[1]/2
            binSize    = bins[1]
            lastAzi    = 360 - aziStarter
            binAzimuth = np.linspace(binStarter, lastAzi, self.bins-1, endpoint=True)
            
            for i in range(0,len(uniqueBins)):
                aziBin = uniqueBins[i]
                azi = binAzimuth[aziBin-1]
                rotatedGrid = rotate2azimuth(azi, gauss)
                hPointGrid = fwdHorz2D(rotatedGrid)
                slope2horzGrid = slope2horz(rotatedGrid, hPointGrid)
                referenceStack = np.dstack((rotatedGrid, hPointGrid, slope2horzGrid))
                referenceGrids.append(referenceStack)
            
            slope2horz_refs = []
            for index in range(ncols):
                plt.close('all')
                #trigger new raster set
                #  NOTE: I believe this cannot be easily converted
                #        to list comprehensions, given that it req-
                #        uires triggering this 'cascade' of state 
                #        rasters by indexing self.time parameter.
                self.time = index
            '''

            maskedmeanM_list, viz_percent_list = [], []
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
                #calc masked M
                m = self.M_calculation(df, row=index, choice='masked')
                maskedmeanM = np.mean(m)
                maskedmeanM_list.append(maskedmeanM)
                #update progress bar
                self.progress.value = self.time
                
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
            self.log+=f"""<pre style="color:lime">\nModel completed in {run_t}s.
            {cell_t}s/timepoint for array of {ar_cs} cells @ {ncols} timepoints.
            </pre>
            """
            self.modelComplete = 'Complete'
            return 
        
    @param.depends('set_curve_filler')
    def fill_between(self):
        '''
        fills between selected curves
        '''
        #fill between measured direct rad and rad_reconstruction
        if 'Rad_Meas: Direct Downw' in self.chooseTimeSeries and 'IDR_Recon: Planar' in self.chooseTimeSeries:
            if self.fill_True:
                ax.fill_between(times, downDirect, radRecon_planarM, 
                                where=(downDirect>radRecon_planarM),
                                interpolate=True, color='orange', alpha=0.2)
                ax.fill_between(times, downDirect, radRecon_planarM, 
                                where=(downDirect<radRecon_planarM),
                                interpolate=True, color='red', alpha=0.4)
        pass
    #TODO: define UI for this feature.
    #perhaps, tabs for the "Select Curve" cross selector
    #one cross selector to select base curve.
    #then for "fill-to curve", another tab., where we are reminded of 
    #the base curve via widget.link method i.e. "the base curve is {link.Crossselector.value}"
    
    def snapshots(self):
        '''
        for use in comparing different model setting to one-another.
        by pressing 'take snapshot', the user saves the currently plotted 
        masked_timeseries dataframe to the list of objects in a "my_snapshots"
        ObjectSelector param. these snapshots can then be compared to eachother
        by selecting from a multiple selector widget.
        '''
        pass
    
    def multiDay_snapshot(self):
        '''
        this extents snapshots to allow visualization of many days in series
        perhaps will require a different window.
        '''
        pass