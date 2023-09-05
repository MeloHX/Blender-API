import bpy
import random


def add_random_location(objects, amount=1,
                        do_axis=(True, True, True)):
    """Add units to the locations of given objects"""
    for ob in objects:
        for i in range(3):
            if do_axis[i]:
                loc = ob.location
                loc[i] += random.randint(-amount, amount)


class TRANSFORM_OT_random_location(bpy.types.Operator):
    """Add units to the locations of selected objects"""
    bl_idname = "transform.add_random_location"
    bl_label = "Add random Location"

    #这些属性通常用于自定义Blender插件的行为和外观
    amount: bpy.props.IntProperty(name="Amount",
                                  default=1)
    axis: bpy.props.BoolVectorProperty(
                               name="Displace Axis",
                               default=(True, True, True)
                               )
    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        add_random_location(context.selected_objects,
                            self.amount,
                            self.axis)
        return {'FINISHED'}


def register_classes():
    bpy.utils.register_class(TRANSFORM_OT_random_location)
def unregister_classes():
    bpy.utils.unregister_class(TRANSFORM_OT_random_location)