import _albedo.dashcontrols as dashcontrols
import param
import panel as pn
import matplotlib.pyplot as plt

class DashLayout(dashcontrols.DashControls):
    
    @param.depends('date')
    def return_time_control(self):
        return pn.WidgetBox(
            pn.Param(
                self.param, parameters=['time'],
                widgets={'time':{'widget_type': pn.widgets.DiscreteSlider, 
                                 'width': 180}},
                         width=200, name='Time'))
    
    @param.depends('date', 'resolution', 'sigma', 'vertEx', 'bins')
    def return_config_pane(self):
        
        def grab_config():
            config_obj = {
                'Date': self.date_string,
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
    
    @param.depends('log')
    def return_log_pane(self):
        return pn.pane.HTML(
        f"""
        <div id=""style="overflow-y:scroll; height:400px;">
        <pre style="color:white; font-size:12px">Build Log</pre>
        <pre style="color:deepskyblue; font-size:12px">{self.log}</pre>
        </div>
        """,
        style={'background-color':'#000000', 'border':'2px solid black',
               'border-radius': '5px', 'padding': '10px','width':'560px'}
    )
    
    @param.depends('modelComplete')
    def return_model_df(self):
        if self.modelComplete == 'Incomplete':
            return pn.Row('Run model to generate dataframe.')
        else:
            return pn.pane.DataFrame(self.model_dataframe, 
                                     max_rows=4, max_cols=7, width=900)
    
    @param.depends('dictionary')
    def reset_run_state(self):
        self.run = False
        self.progress.value = 0
        if self.modelComplete == 'Complete':
            self.modelComplete = 'Incomplete'
            del self.model_dataframe
        return
    
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
            self.set_m, self.set_masks, self.run_model, self.reset_run_state
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
            pn.Row(self.tryptich,
                   name='Raster Settings',
                   width=900
                  ),
            pn.Column(pn.Row(self.polarAxes, self.diptych),
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
                               self.horizon_preview, self.return_time_control),
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
                            self.return_log_pane
                            )
                        ),
                        name='Run'
                    ),
                    pn.Column(pn.Row(#self.time_control.clone(), 
                                     self.timeseries_control
                                    ),
                              pn.Tabs(pn.Column(
                                          self.timeSeries_Plot,
                                          name='Time Series Plot',
                                          width=900
                                          ),
                                      pn.Column(
                                          self.return_model_df,
                                          name='Dataframe'
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