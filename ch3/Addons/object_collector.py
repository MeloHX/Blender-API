
import bpy

bl_info = {
 "name": "Collector",
 "author": "John Doe",
 "version": (1, 0),
 "blender": (3, 00, 0),
 "description": "Create collections for object types",
 "category": "Object",
}


def register():
 # this function is called when the add-on is enabled
  bpy.utils.register_class(OBJECT_OT_collector_types)
  menu = bpy.types.VIEW3D_MT_object_context_menu
  menu.append(draw_collector_item)

def unregister():
 # this function is called when the add-on is disabled
  bpy.utils.unregister_class(OBJECT_OT_collector_types)
  menu = bpy.types.VIEW3D_MT_object_context_menu
  menu.remove(draw_collector_item)

"""A class deriving bpy.types.Operators must implement these members:
• A static string named bl_idname that contains a unique name by which the operator 
goes internally
• A static string named bl_label that contains the displayed name of the operator
• A poll() class method that verifies that the conditions for executing the operator are met 
and return either True or False
• An execute() method that runs when the operator is executed, returning a set of possible 
running states
• Optionally, a docstring that Blender will display as additional information"""

class OBJECT_OT_collector_types(bpy.types.Operator):
 """Create collections based on objects types"""
 # F3后输入create type 会出现bl_idname的名字，使得blender完成这个插件指定的操作
 bl_idname = "object.pckt_type_collector"
 bl_label = "Create Type Collections"

 @classmethod
 def poll(cls, context):
   return len(context.scene.objects) > 0
 
#  #  to create the Mesh, Light, and Camera collections and bring each object under each one of them.
#  def execute(self, context):
#     mesh_cl = bpy.data.collections.new("Mesh")
#     light_cl = bpy.data.collections.new("Light")
#     cam_cl = bpy.data.collections.new("Camera")
#     context.scene.collection.children.link(mesh_cl)
#     context.scene.collection.children.link(light_cl)
#     context.scene.collection.children.link(cam_cl)
#     for ob in context.scene.objects:
#       if ob.type == 'MESH':
#         mesh_cl.objects.link(ob)
#       elif ob.type == 'LIGHT':
#         light_cl.objects.link(ob)
#       elif ob.type == 'CAMERA':
#         cam_cl.objects.link(ob)
#     return {'FINISHED'}
 
@staticmethod
def get_collection(name):
 '''Returns the collection named after the given
 argument. If it doesn't exist, a new collection
 is created and linked to the scene'''
 try:
  return bpy.data.collections[name]
 except KeyError:
  cl = bpy.data.collections.new(name)
  bpy.context.scene.collection.children.link(cl)
  return cl
 
def execute(self, context):
  for ob in context.scene.objects:
    cl = self.get_collection(ob.type.title())
    try:
      cl.objects.link(ob)
    except RuntimeError:
      continue
  return {'FINISHED'}

def draw_collector_item(self, context):
 row = self.layout.row()
 row.operator(OBJECT_OT_collector_types.bl_idname)
 