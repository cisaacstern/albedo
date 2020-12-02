import _albedo.dashtutorial as dashtutorial
import param
import panel as pn
import matplotlib.pyplot as plt

class DashLayout(dashtutorial.DashTutorial):
    
    @param.depends('dateIndex', 'resolution', 'sigma',
                   'vertEx', 'bins')
    def return_config_pane(self):
        
        def grab_config():
            config_obj = {
                'SnowSeason': '18-19',
                'DateIndex': self.dateIndex,
                'Raster': {'Resolution': self.resolution,
                           'Sigma': self.sigma,
                           'Vert Exag': self.vertEx},
                'Azimuth Bins': self.bins,
            }
            return config_obj
        
        current_config = grab_config()
        
        self.dictionary = current_config
        
        return pn.pane.JSON(current_config, name='JSON', height=182,
                            width=170, theme='dark', depth=-1)
    
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
        return pn.pane.Alert(txt, alert_type=at, width=154, height=95)
    
    @param.depends('modelComplete')
    def return_run_button(self):
        args = dict({'width':40, 'height':50, 'name':'',
            'parameters':['run']})
        enabled = pn.Param(
            self.param, **args, 
            widgets={'run':{'widget_type': pn.widgets.Checkbox, 'disabled':False},})
        disabled = pn.Param(
            self.param, **args, 
            widgets={'run':{'widget_type': pn.widgets.Checkbox, 'disabled':True},})
        if self.modelComplete == 'Incomplete':
            return enabled
        elif self.modelComplete == 'Complete':
            return disabled
    
    @param.depends('modelComplete')
    def return_run_accordion(self):
        if self.modelComplete == 'Incomplete':
            return pn.pane.Markdown('Plots will load when model is complete.')
        elif self.modelComplete == 'Complete':
            self.run_accordion = pn.Accordion(
                pn.Row('A model-specific tryptic will go here',
                       name='Rasters',
                       width=900
                      ),
                pn.Column('Model-specific sun pos, M, and horzion plots will go here',
                          name='Sun Position, Terrain Correction, Horizons',
                          width=900
                         ),
                pn.Column('A model-specific timeseries plot will go here',
                          name='Time Series Plot',
                          width=900
                         ),
            )
            return self.run_accordion
    
    def set_layout(self):
        self.function_row = pn.Row(
            self.set_filename, self.set_dataframe, self.set_raster,
            self.set_axes, self.calc_meanM_list, self.calc_meanAlpha_list,
            self.set_m, self.set_masks, self.run_model, self.reset_run_state
        )
        self.json_pane = pn.pane.JSON(self.json_obj, name='JSON', width=300, theme='dark')
        
        self.json_comment = pn.pane.Markdown(
            '''
            This pane presents init settings for reference. In the
            future, it can be used to re-init the app with different settings.
            '''
        )
        self.cap_state = pn.WidgetBox(
            pn.pane.Markdown(
            '''
            The displayed datetime is XXXXX. \n
            Click here to download a .json object which captures all current state variables.
            To upload a saved .json object, click here.
            '''
            ), 
            width=350, name='Capture State'
        )
        self.config_accordion = pn.Accordion(
            pn.Row(self.axes3d, self.tryptic,
                   name='Pointcloud & Raster Settings',
                   width=900
                  ),
            pn.Column(pn.Row(self.polarAxes, self.plotMRaster, self.plotMask),
                      name='Sun Position, Terrain Correction, Horizons',
                      width=900
                     ),
            pn.Column(self.timeSeries_Plot,
                      name='Time Series Plot',
                      width=900
                     ),
        )
        self.model_tabs = pn.Row(
            pn.Tabs(pn.Column(self.json_comment, self.json_pane,
                              name='Initialize'
                             ),
                    pn.Column(pn.Row(
                                pn.Column(
                                    pn.Row(self.time_control, self.pointcloud_control, self.raster_control),
                                    pn.Row(self.horizon_control)
                                ),
                                pn.Column(self.timeseries_control)),
                                self.config_accordion,
                                name='Configure'
                             ),
                    pn.Column(
                        pn.Row(pn.Column(pn.Row(self.return_config_pane, 
                                                pn.Column(
                                                    pn.Row(self.return_run_button, 
                                                           pn.Column(pn.Spacer(height=15), self.progress)),
                                                    self.return_run_alert)
                                               ),
                                         pn.Row(self.run_tab_horizon, self.run_tab_time)
                                        ),
                               self.run_tab_timeseries_control
                              ),
                        self.return_run_accordion,
                        name='Run',
                        dynamic=True
                    ),
                    pn.Row(pn.Spacer(width=10),
                           name='Analyze'
                          ),
                    pn.Column(self.cap_state,
                              name='Export'
                             ),
                    active=1
                   ),
        )
        self.tutorial_tabs = pn.Row(
            pn.Tabs(pn.Column(pn.Spacer(width=10),
                              name='Initialize'),
                    pn.Column(pn.Spacer(width=10),
                              name='Configure'),
                    pn.Column(pn.Spacer(width=10),
                              name='Run'),
                    pn.Column(pn.Spacer(width=10),
                              name='Analyze'),
                    pn.Column(pn.Spacer(width=10),
                              name='Export'),
                    active=1
                   )
        )
        
        plt.close()
        return
        
    def set_tabs(self):
        self.tabs = pn.Tabs(
            pn.Column(self.model_tabs, 
                      name = 'Model'),
            pn.Column(self.tutorial_tabs, 
                      name = 'Tutorial'),
            tabs_location='right'
        )
        return
        
    def dashboard(self):
        self.set_json()
        self.set_controls()
        self.set_layout()
        self.set_tabs()
        return pn.Column(self.function_row,
                         self.tabs)