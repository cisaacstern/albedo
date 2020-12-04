import _albedo.runmodel as runmodel
import panel as pn

class DashControls(runmodel.RunModel):

    def set_controls(self):
        self.file_selector = pn.WidgetBox(
            pn.Param(self.param, parameters=['date'], 
                     widgets={'date':{'widget_type': pn.widgets.DiscreteSlider, 
                                      'width': 105}},
                     width=120, name='File'
                    )
        )
        self.pointcloud_control = pn.WidgetBox(
            pn.Row(
                pn.Param(self.param, parameters=['choose3d'], 
                     widgets={'choose3d':
                              {'widget_type': pn.widgets.CheckBoxGroup, 
                               'inline': False}},
                     width=100, name='View'
                    ),
                pn.Param(self.param, parameters=['elev'], 
                     widgets={'elev':
                              {'widget_type': pn.widgets.IntSlider, 
                                      'width': 80}},
                     width=100, name=''
                    ),
                pn.Param(self.param, parameters=['azim'], 
                     widgets={'azim':{'widget_type': pn.widgets.IntSlider, 
                                      'width': 80}},
                     width=100, name=''
                    ),
            )
        )
        self.raster_control = pn.WidgetBox(
            pn.Row(
                pn.Param(self.param, parameters=['resolution'],
                     width=100, name='Raster'),
                pn.Param(self.param, parameters=['sigma'],
                     width=100, name=''),
                pn.Param(self.param, parameters=['vertEx'],
                     width=100, name=''),
            )
        )
        self.azi_bins = pn.WidgetBox(
            pn.Param(self.param, parameters=['bins'],
                     width=107, name='Azimuth')
        )
        self.horizon_preview = pn.WidgetBox(
            pn.Row(
                pn.Param(self.param, parameters=['activateMask'],
                         widgets={'activateMask':
                                  {'widget_type': pn.widgets.RadioBoxGroup, 
                                   'inline': False}},
                         width=105,
                         name='Preview'
                        )
            )
        )
        self.timeseries_control = pn.WidgetBox(
            pn.Param(self.param, parameters=['chooseTimeSeries'], 
                     widgets={'chooseTimeSeries':
                              {'widget_type':pn.widgets.CheckBoxGroup,
                               'width': 500, 'height': 30}},
                     width=530, height=100, name='Select Curves'
                    )
        )
        
        self.run_tab_logs = pn.WidgetBox(
            pn.Param(self.param, parameters=[], 
                     width=520, height=150, name='Build Log'
                    )
        )

        return