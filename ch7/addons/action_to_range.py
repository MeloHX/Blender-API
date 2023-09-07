
bl_info = {
    "name": "Action to Range",
    "author": "Xuan",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Timeline > View > Action to Scene Range",
    "description": "Transfer Action Duration to Scene Range",
    "category": "Learning",
}

"""The next steps are as follows:
1. Writing the operator.
2. Writing its menu entry.
3. Registering the classes and user interface."""


import bpy


class ActionToSceneRange(bpy.types.Operator):
    """Set Playback range to current action Start/End"""
    bl_idname = "anim.action_to_range"
    bl_label = "Action to Scene Range"
    bl_description = "Transfer action range to scene range"
    bl_options = {'REGISTER', 'UNDO'}

    # 场景中的两个帧范围设置: 主要 （main）的影响场景渲染，而预览(preview)范围只影响Viewport回放。
    use_preview: bpy.props.BoolProperty(default=False)

    # Adding a poll and an execute method will allow the operator to run.否则是静态变量
    @classmethod
    def poll(cls, context):
        # 要获得活动动画的范围，我们必须验证以下条件:•应该有一个活动对象•活动对象必须是动画的
        # When any of the not conditions are met, the operator is grayed out in the interface. 
        # Otherwise, the operator can be launched, and that will run its execute method.
        obj = context.object
        if not obj:
            return False
        if not obj.animation_data:
            return False
        if not obj.animation_data.action:
            return False

        return True

    def execute(self, context):
        first, last = context.object.animation_data.action.frame_range

        scn = context.scene

        scn.use_preview_range = self.use_preview
        if self.use_preview:
            scn.frame_preview_start = int(first)
            scn.frame_preview_end = int(last)
        else:
            scn.frame_start = int(first)
            scn.frame_end = int(last)

        # 自动缩放和滚动动作编辑器的视图，以便你可以看到整个动画或动作的时间范围，而无需手动调整视图
        #有可能导致错误的代码放在try缩进块下，而在发生特定错误时执行的代码放在except ErrorType缩进块下
        try:
            bpy.ops.action.view_all()
        except RuntimeError:
            # we are not in the timeline context
            for window in context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type != 'DOPESHEET_EDITOR':
                        continue
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            with context.temp_override(window=window,
                                                        area=area,
                                                        region=region):
                                bpy.ops.action.view_all()
                            break
                    break
    
        return {'FINISHED'}


def menu_func(self, context):
    # 创建了一个带有文本标签的操作按钮，该按钮执行了一个名为 ActionToSceneRange 的操作，并且使用了预览模式
    props = self.layout.operator(ActionToSceneRange.bl_idname,
                                 text=ActionToSceneRange.bl_label + " (preview)")
    props.use_preview = True
    # 对应main模式，上面是预览模式
    props = self.layout.operator(ActionToSceneRange.bl_idname,
                                 text=ActionToSceneRange.bl_label)
    props.use_preview = False


def register():
    bpy.utils.register_class(ActionToSceneRange)
    bpy.types.TIME_MT_view.append(menu_func)

def unregister():
    bpy.types.TIME_MT_view.remove(menu_func)
    bpy.utils.unregister_class(ActionToSceneRange)