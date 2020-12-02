import _albedo.runmodel as runmodel
import panel as pn

class DashControls(runmodel.RunModel):

    def set_controls(self):
        self.time_control = pn.WidgetBox(
            pn.Param(self.param, parameters=['snowSeas', 'dateIndex', 'timePoint'], 
                     widgets={'snowSeas':{'widget_type': pn.widgets.IntSlider, 'width': 80},
                              'dateIndex':{'widget_type': pn.widgets.IntSlider, 'width': 80},
                              'timePoint':{'widget_type': pn.widgets.IntSlider, 'width': 80}},
                     width=100, name='Time'
                    )
        )
        self.run_tab_time = pn.WidgetBox(
            pn.Param(self.param, parameters=[], 
                     height=70, width=210, name='Model Time'
                    )
        )
        self.pointcloud_control = pn.WidgetBox(
            pn.Param(self.param, parameters=['elev', 'azim', 'choose3d'], 
                     widgets={'elev':{'widget_type': pn.widgets.IntSlider, 'width': 80},
                              'azim':{'widget_type': pn.widgets.IntSlider, 'width': 80},
                              'choose3d':{'widget_type': pn.widgets.CheckBoxGroup, 
                                          'inline': False}
                             },
                     width=100, name='Pointcloud'
                    )
        )
        self.raster_control = pn.WidgetBox(
            pn.Param(self.param, parameters=['resolution', 'sigma', 'vertEx'],
                     width=100, name='Raster')
        )
        self.horizon_control = pn.WidgetBox(
            pn.Row(
                pn.Param(self.param, parameters=['activateMask'],
                         widgets={'activateMask':{'widget_type': pn.widgets.RadioBoxGroup, 
                                                  'inline': False}},
                         height=70, width=105, name='Horizon Mask'
                        ),
                pn.Param(self.param, parameters=['bins'],
                         width=107, name='Azimuth'
                        ),
            )
        )
        self.run_tab_horizon = pn.WidgetBox(
            pn.Param(self.param, parameters=[],
                     height=70, width=110, name='Model Horz Mask'
                    )
        )
        self.timeseries_control = pn.WidgetBox(
            pn.Param(self.param, parameters=['chooseTimeSeries'], 
                     widgets={'chooseTimeSeries':{'widget_type':pn.widgets.CrossSelector,
                                                  'width': 500, 'height': 30},
                             },
                     width=530, height=262, name='Select Curves'
                    )
        )
        
        self.run_tab_timeseries_control = pn.WidgetBox(
            pn.Param(self.param, parameters=[], 
                     width=530, height=262, name='Model Select Curves'
                    )
        )

        return