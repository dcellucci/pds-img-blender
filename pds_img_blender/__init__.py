import bpy

bl_info = {
    "name": "Import PDS IMG File",
    "blender": (3, 30, 0),
    "category": "Object",
}

if 'bpy' in locals():
    print('PDS IMG Reloading')
    from importlib import reload
    import sys
    for k, v in list(sys.modules.items()):
        if k.startswith('pds_img_blender.'):
            reload(v)

from .pds_img_blender import ImportIMGData, menu_func_import

# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    bpy.utils.register_class(ImportIMGData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportIMGData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)