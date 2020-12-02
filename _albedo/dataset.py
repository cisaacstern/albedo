import param, os, datetime

class DataSet(param.Parameterized):
    
    #geographic constants
    eastMin, eastMax = 320977, 320980
    northMin, northMax = 4168144, 4168147        
    geotransform = [0, 1, 0, 0, 0, 1]
    projection = 'WGS84'
    UTC_offset = 8
    lat, long = 37.643, -119.029
    
    #timeseries constants
    timeResolution = 15
    
    #TODO: transform constants. i.e. richdem vert. exagg.
    
    #filepath constants
    pointcloud_directory = os.path.join(os.getcwd(), 'data', 'pointclouds')
    #pointcloud_directory = os.path.join(os.path.dirname(__file__), 'data', 'pointclouds')
    #pointcloud_directory = os.path.dirname('data/pointclouds/')
    #pointcloud_directory='data/pointclouds'
    
    pointclouds = []
    for file in os.listdir(pointcloud_directory): 
        pointclouds.append(file)
    pointclouds.sort()
    pc_count = len(pointclouds)
    
    rad_directory = os.path.join(os.getcwd(), 'data', 'radiometers')
    #rad_directory = os.path.join(os.path.dirname(__file__), 'data', 'radiometers')
    #rad_directory = os.path.dirname('data/radiometers/')
    #rad_directory = 'data/radiometers'
    radiometers = []
    with os.scandir(rad_directory) as it:
        for entry in it:
            if entry.name.startswith('20') and entry.is_file():
                radiometers.append(entry.name)
    radiometers.sort()
    rad_count = len(radiometers)
    
    assert (pc_count==rad_count), 'Fileset lengths unequal.'
    
    enabledDays = []
    for i in range(0, pc_count):
        enabledDays.append('placeholder')
    for i in range(0, pc_count):
        filename = pointclouds[i]
        year, month, day = int(filename[0:4]), int(filename[4:6]), int(filename[6:8])
        date = datetime.datetime(year, month, day, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
        enabledDays[i] = date
    
    #TODO: assert a check of enabled days against radiometer dates
    
    def set_json(self):
        self.json_obj = {
            'Easting Bounds': (self.eastMin, self.eastMax),
            'Northing Bounds': (self.northMin, self.northMax),
            'Geotransform': self.geotransform,
            'Projection': self.projection,
            'UTC Offset': self.UTC_offset,
            'LatLong': (self.lat, self.long),
            'Time Series Resolution (min)': self.timeResolution,
            'Filepaths': {'Pointclouds': self.pointcloud_directory,
                          'Radiometers': self.rad_directory
                         },
        }
        return
    
    #TODO: allow for snow season selection
    snowSeas = param.Integer(default=0, bounds=(0, 100))
    
    #for passing to Paramaters
    indexLength = pc_count-1
    dateIndex = param.Integer(default=0, bounds=(0, indexLength))
