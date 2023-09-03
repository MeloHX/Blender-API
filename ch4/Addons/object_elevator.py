
bl_info = {
    "name": "Elevator",
    "author": "John Doe",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Move objects up to a minimum height",
    "category": "Object",
}


import bpy
# 用于引入浮点数
from bpy.props import FloatProperty
# 因为我们想要显示一个使用约束的复选框，所以用到Bool Property
from bpy.props import BoolProperty

from copy import copy

# 用来找到最上层的父类，因为我们希望对父类先做出变换，再处理子类，否则可能会导致子类出错
def ancestors_count(ob):
    """Return number of objects up in the hierarchy"""
    ancestors = 0
    while ob.parent:
        ancestors += 1
        ob = ob.parent

    return ancestors


def get_constraint(ob, constr_type, reuse=True):
    """Return first constraint of given type.
    If not found, a new one is created"""
    if reuse:
        for constr in ob.constraints:
            if constr.type == constr_type:
                return constr
    
    return ob.constraints.new(constr_type)


class OBJECT_OT_elevator(bpy.types.Operator):
    """Move Objects up to a certain height"""
    """• bl_label: The display name of the panel
        • bl_idname: The unique name of the panel for internal usage"""
    bl_idname = "object.pckt_floor_transform"
    bl_label = "Elevate Objects"
    bl_options = {'REGISTER', 'UNDO'}

    floor: FloatProperty(name="Floor", default=0)
    constr: BoolProperty(name="Constraints", default=False)
    # 这样做的目的是避免重复约束，即：在循环中，检查可以使用的现有约束。如果没有找到，脚本就创建它
    reuse: BoolProperty(name="Reuse", default=True)

    @classmethod
    # 因为作用于对象，所以要检查有无对象
    def poll(cls, context):
        return len(bpy.context.selected_objects) > 0

    def execute(self, context):
        if self.constr:
            for ob in context.selected_objects:
                limit = get_constraint(ob, 'LIMIT_LOCATION', self.reuse)

                limit.use_min_z = True
                limit.min_z = self.floor
            
            return {'FINISHED'}

        # affect coordinates directly
        # sort parent objects first
        # context. selected_objects being read-only,  we cannot reorder it directly ，we need to copy its content to a list：
        # Now we can order this list in a way that won’t cause the same object to be moved twice(#copy())
        selected_objects = copy(context.selected_objects)
        selected_objects.sort(key=ancestors_count)

        for ob in selected_objects:
            matrix_world = ob.matrix_world
            # 在矩阵中判断z的高度是否到达最小高度
            if matrix_world[2][3] > self.floor:
                continue    

            matrix_world[2][3] = self.floor
            # make sure next object matrix will be updated： Since matrix values are not automatically updated during script execution,
            
            context.view_layer.update()

        return {'FINISHED'}


def draw_elevator_item(self, context):
    # 将操作符添加到对象右键菜单中;
    # Menu functions must accept self and context as argument
    # context is left unused in this case
    row = self.layout.row()
    row.operator(OBJECT_OT_elevator.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_elevator)
    # 插件被启用或者禁用的时候会用到这俩函数，所以这里作用对象时 draw_elevator_item
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_elevator_item)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_elevator)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_elevator_item)
    