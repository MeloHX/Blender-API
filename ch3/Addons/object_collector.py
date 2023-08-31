
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
 pass
def unregister():
 # this function is called when the add-on is disabled
 pass


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
 bl_idname = "object.pckt_type_collector"
 bl_label = "Create Type Collections"

 @classmethod
 def poll(cls, context):
   return len(context.scene.objects) > 0
 
 #  to create the Mesh, Light, and Camera collections and bring each object under each one of them.
 def execute(self, context):
    mesh_cl = bpy.data.collections.new("Mesh")
    light_cl = bpy.data.collections.new("Light")
    cam_cl = bpy.data.collections.new("Camera")
    context.scene.collection.children.link(mesh_cl)
    context.scene.collection.children.link(light_cl)
    context.scene.collection.children.link(cam_cl)
    for ob in context.scene.objects:
      if ob.type == 'MESH':
        mesh_cl.objects.link(ob)
      elif ob.type == 'LIGHT':
        light_cl.objects.link(ob)
      elif ob.type == 'CAMERA':
        cam_cl.objects.link(ob)
    return {'FINISHED'}