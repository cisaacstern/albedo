import _albedo.dashlayout
import panel as pn
from bokeh.io import curdoc
pn.extension()

dash = _albedo.dashlayout.DashLayout()
board = dash.dashboard()
model = board.get_root()
curdoc().add_root(model)
curdoc().title = 'Albedo'
