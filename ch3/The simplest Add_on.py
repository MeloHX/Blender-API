
# Add_on文件以空白行开始，空白行结尾，否则不被认为是Add_on
bl_info = {
    "name": "The Simplest Add-on",
    "author": "John Doe",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "A very simple add-on",
    "warning": "This is just for Learning",
    "category": "Learning",
}


def register():
    # this function is called when the add-on is enabled
    pass

def unregister():
    # this function is called when the add-on is disabled
    pass