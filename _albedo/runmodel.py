import _albedo.plotmethods as plotmethods
import param
import numpy as np
import matplotlib.pyplot as plt

class RunModel(plotmethods.PlotMethods):
    
    @param.depends('run')
    def run_model(self): #formerly, calc_maskedmeanM_list
        if self.run == False:
            pass
        elif self.run == True:
            #TODO: get return_run_alert to display 'running...'
            self.return_run_alert()
            #TODO: bin azimuths - generate a slope to horz reference set here
            col_count = self.dataframe.shape[0]
            self.progress.max = col_count-1
            maskedmeanM_list = []
            #TODO: msk_elevRast_List, msk_slopeRast_List, msk_aspectRast_List = [], [], []
            #TODO: viz_percent_list = []
            #TODO: self.model_dataframe = self.dataframe ----> statically "snapshot" all this. for downstream speed.
            for index in range(0, col_count):
                plt.close('all')
                self.timePoint = index
                img = self.M_calculation(df=self.dataframe, 
                                         row=index,
                                         choice='masked'
                                        )
                maskedmeanM = np.mean(img)
                maskedmeanM_list.append(maskedmeanM)
                self.progress.value = self.timePoint
            self.maskedmeanM_list = maskedmeanM_list
            #TODO:model_dataframe.insert(maskedmeanM_list, msk_elevRast_List, msk_slopeRast_List, msk_aspectRast_List,
            #                            viz_percent_list)
            #TODO: for list in all these lists: del list
            self.timePoint = 0
            #TODO: make a new timePoint parameter: modelTimePoint
            #      also make a new horizon mask 'overlay/remove' selector: modelOverlay
            #      also make new Crossselector: modelCrossselector
            #      also make a whole new set of plotter functions, for tryptic, sunpos, M, horizon, and timeseries
            #      ---> use these new plotters, in class ModelPlots(), to plot directly from the assembled dataframe
            #      ---> it may be a good idea to drop the dataframe in storage, and then call it generatively based on
            #           the index of modelTimePoint.
            #           ----> this may be the first viable opportunity i have to use a generator, 
            #                 given that the indexing will now be only
            #TODO: by having NO DUPLICATE panes between config and run tabs,
            #       --> we may get a real speedup
            #TODO: add 'DATAFRAME' accordion to run_accordions
            #       ---> but size of dataframe may mean this is only a partial, or generative view
            #       ----> serves as a reference for upcoming download feature
            #TODO: OVERAL PICTURE: ISOLATE TABS, no duplicates, take a static snapshot in run, and plot from there.
            #               --> among other things, this means that we don't need to burden the 'Config' tab
            #                    with re-rendering views, if we are moving modelTimePoint to index model data,
            #                     and not the "global" self.timePoint
            self.modelComplete = 'Complete'
            #TODO:add 'refresh/clear figure' method / garbage collector
            return 
        
    @param.depends('fill_True')
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