import _albedo.dataset as dataset
import param
import panel as pn

class Parameters(dataset.DataSet):
    
    timePoint= param.Integer(default=0, bounds=(0, 100))
    
    elev     = param.Integer(default=30, bounds=(0, 90), step=5)
    azim     = param.Integer(default=285, bounds=(0, 360), step=15)

    choose3d = param.ListSelector(default=['Pointcloud', 'Planar Fit'],
                                  objects=['Pointcloud', 'Planar Fit'])
    
    resolution = param.Integer(default=30, bounds=(10, 300), step=10)
    sigma      = param.Number(0.5, bounds=(0, 3))
    vertEx     = param.Number(86.3, bounds=(0, 150))
    
    chooseTimeSeries = param.ListSelector(default=['Rad_Meas: Global Up', 'Rad_Meas: Direct Down', 'Rad_Meas: Diffuse Down',
                                                   'M: Planar', #'M: Raster Mean', #'M: Horizon Mean',
                                                   'Alpha: Planar', #'Alpha: Raster Mean', #'Alpha: Horizon Mean',
                                                   'IDR_Recon: Planar', #'IDR_Recon: Raster Mean'#, #'IDR_Recon: Horizon Mean',
                                                  ],
                                          objects=['Rad_Meas: Global Up', 'Rad_Meas: Direct Down', 'Rad_Meas: Diffuse Down',
                                                   'M: Planar', #'M: Raster Mean', 'M: Horizon Mean',
                                                   'Alpha: Planar', #'Alpha: Raster Mean', 'Alpha: Horizon Mean',
                                                   'IDR_Recon: Planar', #'IDR_Recon: Raster Mean', 'IDR_Recon: Horizon Mean',
                                                  ]
                                         )
    
    activateMask = param.Selector(objects=['Overlay', 'Remove'])
    bins = param.Integer(default=16, bounds=(8, 64), step=8)

    
    run = param.Boolean(False)
    
    progress = pn.widgets.Progress(name='Progress', width=80, value=0, bar_color='info')
    
    modelComplete = param.ObjectSelector(default="Incomplete", 
                                         objects=["Incomplete", "Running", "Complete"])
    
    dictionary = param.Dict(default={"default": "dictionary"})

    fill_True = param.Boolean(True, doc="A Boolean parameter")