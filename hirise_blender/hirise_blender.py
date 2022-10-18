
import bpy
from .planetaryimage import PDS3Image
import numpy as np
import os


def make_mesh(gridded_data, lower_res_factor = 4, quads = True):
    data_width = gridded_data.shape[0]//lower_res_factor
    data_height = gridded_data.shape[1]//lower_res_factor

    vertices = np.zeros((data_width*data_height, 3))
    if quads:
        faces = np.zeros(((data_width-1)*(data_height-1), 4), dtype = 'int')
    else:
        faces = np.zeros(((data_width-1)*(data_height-1)*2, 3), dtype = 'int')
    
    for i in range(data_width):
        for j in range(data_height):
            vertices[i*data_height+j][0] = i*lower_res_factor
            vertices[i*data_height+j][1] = j*lower_res_factor
            if i == 0 or i == data_width-1 or j == 0 or j == data_height-1: 
                vertices[i*data_height+j][2] = 0 
            else:
                vertices[i*data_height+j][2] = gridded_data[i*lower_res_factor][j*lower_res_factor]

    for i in range(data_width-1):
        for j in range(data_height-1):
            if quads:
                faces[(i*(data_height-1)+j)][0] = i*data_height+j
                faces[(i*(data_height-1)+j)][1] = i*data_height+j+1
                faces[(i*(data_height-1)+j)][2] = (i+1)*data_height+j+1
                faces[(i*(data_height-1)+j)][3] = (i+1)*data_height+j
            else:
                faces[(i*(data_height-1)+j)*2][0] = i*data_height+j
                faces[(i*(data_height-1)+j)*2][1] = i*data_height+j+1
                faces[(i*(data_height-1)+j)*2][2] = (i+1)*data_height+j
                
                faces[(i*(data_height-1)+j)*2+1][0] = i*data_height+j+1
                faces[(i*(data_height-1)+j)*2+1][1] = (i+1)*data_height+j+1
                faces[(i*(data_height-1)+j)*2+1][2] = (i+1)*data_height+j
    
    mesh_data = bpy.data.meshes.new("cube_mesh_data")
    #mesh_data.from_pydata(vertices, [], faces)
    
    print("adding vertices...")
    mesh_data.vertices.add(vertices.shape[0])
    mesh_data.vertices.foreach_set("co", vertices.flatten())
    
    print("adding vertex indices...")
    mesh_data.loops.add(faces.size)
    mesh_data.loops.foreach_set("vertex_index", faces.flatten())
    
    print("adding faces...")
    mesh_data.polygons.add(faces.shape[0])
    if quads:
        mesh_data.polygons.foreach_set("loop_start", range(0, faces.size, 4))
        mesh_data.polygons.foreach_set("loop_total", [4]*faces.shape[0])
    else:
        mesh_data.polygons.foreach_set("loop_start", range(0, faces.size, 3))
        mesh_data.polygons.foreach_set("loop_total", [3]*faces.shape[0])

    print("update mesh...")
    mesh_data.update()
    
    print("validating mesh...")
    mesh_data.validate()
    
    return mesh_data

def read_img_data(context, filepath, ppgs, safety, quads):
    print(context)
    filename = os.path.basename(filepath)[:-4]
    # Open IMAGE
    image = PDS3Image.open(filepath)

    maxval =  image.data.max()
    minval = image.data.min()
    remove_mask = np.where(image.data < -10000, 0, image.data)
    minval = remove_mask.min()
    
    renormalized_masked = np.where(remove_mask != 0, remove_mask-minval, remove_mask)
    
    npdata = renormalized_masked[0]
    
    if not safety and ppgs < 4:
        ppgs = 4
    
        
    mesh_data = make_mesh(npdata, ppgs, quads)
       
    obj = bpy.data.objects.new(filename, mesh_data)

    new_collection = bpy.data.collections.new(filename)
    bpy.context.scene.collection.children.link(new_collection)
    # add object to scene collection
    new_collection.objects.link(obj)

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, IntProperty
from bpy.types import Operator


class ImportIMGData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.img_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import File"

    # ImportHelper mixin class uses this
    filename_ext = ".img"

    filter_glob: StringProperty(
        default="*.img",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    ppgs: IntProperty(
        name="Pixels Per Grid Square"
      , description="Choose How Many Pixels in the IMG file will correspond to a single grid square (quad or tri) in the mesh."
      , default=8
      , max = 32
      , min = 1
    )
    
    safety: BoolProperty(
        name="Safety"
      , description="Enable to go below 4 pixels per grid. DO THIS ONLY IF YOU HAVE TONS OF RAM"
      , default=False
    )
    
    quads: BoolProperty(
        name = "Use Quads"
      , description="Use a quad mesh or a triangle mesh."
      , default = True
      )

    def execute(self, context):
        return read_img_data(context, self.filepath, self.ppgs, self.safety, self.quads)


# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(ImportIMGData.bl_idname, text="HIRISE .IMG")


# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    bpy.utils.register_class(ImportIMGData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportIMGData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
    # test call
    #bpy.ops.import_test.some_data('INVOKE_DEFAULT')
