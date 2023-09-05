from bpy.utils import previews
import os

# 根据Python的命名约定，变量名是大写的，因为它是全局的。此外，它以下划线开头，因为它不打算在任何其他模块中使用
# global list for storing icon collection
_CUSTOM_ICONS = None

def register_icons():
    """Load icon from the add-on folder"""
    global _CUSTOM_ICONS
    if _CUSTOM_ICONS:
        # the collection list is already  loaded
        return

    collection = previews.new()
    img_extensions = ('.png', '.jpg')
    
    module_path = os.path.dirname("H:\\Python project\\Git\\Blender-API\\ch6\\Addons\\structured_addon\\pictures")
    picture_path = os.path.join(module_path, 'pictures')
    for img_file in os.listdir(picture_path):
        # ext是拓展名即：png,jpg
        img_name, ext = os.path.splitext(img_file)
        
        if ext.lower() not in img_extensions:
            continue
        disk_path = os.path.join(picture_path, img_file)
        # img_name 就是后面用于查找的icon_id
        collection.load(img_name, disk_path, 'IMAGE')

    _CUSTOM_ICONS = collection

def unregister_icons():
    """Removes all loaded icons"""
    global _CUSTOM_ICONS
    if _CUSTOM_ICONS:
        previews.remove(_CUSTOM_ICONS)
    
    _CUSTOM_ICONS = None


def get_icons_collection():
    # load icons from disk
    register_icons()

    # at this point, we should have icons. A None _CUSTOM_ICONS would cause an error
    assert _CUSTOM_ICONS
    return _CUSTOM_ICONS