import sys
from importlib import reload
import bpy

from . import *
# import operators
# import img_loader
# import panel
# import preferences

def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return
    reload(sys.modules[__name__])
    reload(img_loader)
    reload(panel)
    reload(preferences)
    reload(operators)