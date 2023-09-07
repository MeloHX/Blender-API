
bl_info = {
    "name": "Vert Runner",
    "author": "xuan",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Object > Animation > Vert Runner",
    "description": "Run over vertices of the active object",
    "category": "Learning",
}

"""我们将按照通常的步骤进行:1写运算符2。编写菜单项3。注册类和接口"""

import bpy
from math import asin, pi


class VertRunner(bpy.types.Operator):
    """Run over the vertices of the active object"""
    bl_idname = "object.vert_runner"
    bl_label = "Vertex Runner"
    bl_description = "Animate along vertices of active object"
    bl_options = {'REGISTER', 'UNDO'}

    # 我们用一个Integer Property设置每个关键帧之间的距离:
    step: bpy.props.IntProperty(default=12)
    loop: bpy.props.BoolProperty(default=True)

    @classmethod
    # 为了使选定的对象在活动对象的几何形状上动画化，我们需要以下内容:•活动对象•网格数据(Mesh)•选定对象
    # 没有返回任何false（条件都成立），就会开始执行execute
    def poll(cls, context):
        obj = context.object

        if not obj:
            return False

        if not obj.type == 'MESH':
            return False
        
        if not len(context.selected_objects) > 1:
            return False

        return True

    def aim_to_point(self, ob, target_co):
        # 目标位置-当前位置 ，获得旋转方向
        direction = target_co - ob.location
        direction.normalize()

        arc = asin(direction.y)
        if direction.x < 0:
            arc = pi - arc
        
        arc += pi / 2
        arcs = (arc, arc + 2*pi, arc - 2*pi)

        diffs = [abs(ob.rotation_euler.z - a) for a in arcs]
        shortest = min(diffs)

        res = next(a for i, a in enumerate(arcs) if diffs[i] == shortest)
        ob.rotation_euler.z = res


    """Breaking the operator’s goal into steps, we should do the following:
        1. Get a list of patrol points; in this case, the vertices of the active object.
            2. Scroll through the selected objects.
                3. Move them through the patrol points and set the keyframes."""
    def execute(self, context):
        verts = list(context.object.data.vertices)
        
        # 在vert的末尾添加它的第一个元素的副本，使对象回到动画结束时的初始位置:实现循环播放的效果
        if self.loop:
            verts.append(verts[0])

        # When we iterate through the selected objects, we should make sure to skip the active one, which is likely selected:
        for ob in context.selectable_objects:
            if ob == context.active_object:
                continue      

            # move to last position to orient towards first vertex
            ob.location = context.object.data.vertices[-1].co

            frame = context.scene.frame_current
            for vert in verts:                
                # orient towards destination before moving the object
                self.aim_to_point(ob, vert.co)
                ob.keyframe_insert('rotation_euler', frame=frame, index=2)

                ob.location = vert.co
                ob.keyframe_insert('location', frame=frame)

                frame += self.step
 
        return {'FINISHED'}


def anim_menu_func(self, context):
    # Since menu elements are displayed in reverse order, we must add a separator first:
    self.layout.separator()
    self.layout.operator(VertRunner.bl_idname,
                         text=VertRunner.bl_label)

def register():
    bpy.utils.register_class(VertRunner)
    bpy.types.VIEW3D_MT_object_animation.append(anim_menu_func)  #TODO: header button

def unregister():
    bpy.types.VIEW3D_MT_object_animation.remove(anim_menu_func)
    bpy.utils.unregister_class(VertRunner)