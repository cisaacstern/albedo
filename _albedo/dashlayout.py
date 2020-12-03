import _albedo.dashtutorial as dashtutorial
import param
import panel as pn
import matplotlib.pyplot as plt

class DashLayout(dashtutorial.DashTutorial):
    
    @param.depends('date', 'resolution', 'sigma',
                   'vertEx', 'bins')
    def return_config_pane(self):
        
        def grab_config():
            config_obj = {
                'SnowSeason': '18-19',
                'Date': self.date,
                'Raster': {'Resolution': self.resolution,
                           'Sigma': self.sigma,
                           'Vert Exag': self.vertEx},
                'Azimuth Bins': self.bins,
            }
            return config_obj
        
        current_config = grab_config()
        
        self.dictionary = current_config
        
        return pn.pane.JSON(current_config, name='JSON',
                            width=300, theme='dark', depth=-1)
    
    @param.depends('dictionary')
    def reset_run_state(self):
        self.run = False
        self.progress.value = 0
        self.modelComplete = 'Incomplete'
        return
    
    @param.depends('modelComplete')
    def return_run_alert(self):
        if self.modelComplete == 'Incomplete':
            txt = '####Ready to run.'
            at = 'warning'
        else:
            txt = '####Model complete.'
            at = 'info'
        return pn.pane.Alert(txt, alert_type=at, width=130)
    
    @param.depends('modelComplete')
    def return_run_button(self):
        args = dict({'width': 80, 'name':'', 'parameters':['run']})
        enabled = pn.Param(
            self.param, **args, 
            widgets={'run':
                     {'widget_type': pn.widgets.Toggle, 'disabled':False},})
        disabled = pn.Param(
            self.param, **args, 
            widgets={'run':
                     {'widget_type': pn.widgets.Toggle, 'disabled':True},})
        if self.modelComplete == 'Incomplete':
            return enabled
        elif self.modelComplete == 'Complete':
            return disabled
    
    def set_layout(self):
        self.function_row = pn.Row(
            self.set_filename, self.set_dataframe, self.set_raster,
            self.set_axes, #self.calc_meanM_list, self.calc_meanAlpha_list,
            self.set_m, self.set_masks, self.run_model, self.reset_run_state,
            sizing_mode='scale_both'
        )
        self.json_pane = pn.pane.JSON(self.json_obj, name='JSON', width=300, 
                                      theme='dark', hover_preview=True)
        
        self.init_comment = pn.pane.Markdown(
            '''
            Immutable model init settings are presented below for reference. 
            To begin, choose a date from the selector at right.
            Explore the pointcloud with the view controls. 
            In the next tab, specify pointcloud rasterization and azimuth bins.
            '''
        )
        self.run_comment = pn.pane.Markdown(
            '''
            Current configuration presented below for reference.
            Press Run to run this config.
            To adjust config, return to Configure tab. 
            In the next tab, review results of completed model.
            '''
        )
        self.cap_state = pn.WidgetBox(
            pn.pane.Markdown(
            '''
            The displayed datetime is XXXXX. \n
            Click here to download a .json object which captures all 
            current state variables.
            To upload a saved .json object, click here.
            '''
            ), 
            width=350, name='Capture State'
        )
        self.config_accordion = pn.Tabs(
            pn.Row(self.tryptic,
                   name='Raster Settings',
                   width=900
                  ),
            pn.Column(pn.Row(self.polarAxes, self.plotMRaster, self.plotMask),
                      name='Terrain Correction Preview',
                      width=900
                     )
        )
        self.model_tabs = pn.Row(
            pn.Tabs(pn.Row(
                        pn.Column(self.init_comment, self.json_pane),
                        pn.Column(
                            pn.Row(self.file_selector, self.pointcloud_control),
                            self.axes3d
                        ),
                        name='Initialize'
                    ),
                    pn.Column(
                        pn.Row(self.raster_control, self.azi_bins,
                               self.horizon_preview),
                        self.config_accordion,
                        name='Configure'
                    ),
                    pn.Column(pn.Row(
                        pn.Column(self.run_comment, self.return_config_pane),
                        pn.Column(
                            pn.Row(self.return_run_button, 
                                   pn.Column(
                                       pn.Spacer(height=20),
                                       self.progress
                                   )
                                  ),
                            self.return_run_alert,
                            self.run_tab_logs
                            )
                        ),
                        name='Run'
                    ),
                    pn.Column(pn.Row(self.analyze_timepoint, 
                                     self.timeseries_control
                                    ),
                              pn.Tabs(pn.Column(
                                          self.timeSeries_Plot,
                                          name='Time Series Plot',
                                          width=900
                                          ),
                                      pn.Column(
                                          name='Terrain Correction @ Timepoint',
                                          width=900
                                      ),
                                      pn.Column(
                                          name='Dataframe',
                                          width=900
                                      ),
                              ), 
                              name='Analyze'
                    ),
                    pn.Column(self.cap_state,
                              name='Export'
                             ),
                    active=0
                   ),
        )
        
        plt.close()
        return
        
    def dashboard(self):
        self.set_json()
        self.set_controls()
        self.set_layout()
        return pn.Column(self.function_row,
                         self.model_tabs)