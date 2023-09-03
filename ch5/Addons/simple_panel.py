
bl_info = {
    "name": "A Very Simple Panel",
    "author": "Xuan",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "description": "Just show up a panel in the UI",
    "category": "Learning",
}

import bpy
from bpy.utils import previews
import os
import random

# global variable for icon storage
"""我们的图标必须在脚本中的任何地方都可以访问。可以使用全局变量、静态成员或单例对象进行存储。在本例中，我们使用全局变量，因为它是更简单的选项。"""
custom_icons = None

# 我们自己添加一个笑脸图标
def load_custom_icons():
    """Load icon from the add-on folder"""
    Addon_path = os.path.dirname(r"H:\Python project\Git\Blender-API\ch5\Addons\icon_smile_64.png")
    img_file = os.path.join(Addon_path,"icon_smile_64.png")
    global custom_icons

    custom_icons = previews.new()
    custom_icons.load("smile_face",img_file, 'IMAGE')


# 当插件禁用时，移除图标
def remove_custom_icons():
    """Clear Icons loaded from file"""
    global custom_icons
    bpy.utils.previews.remove(custom_icons)

# 该函数接受 Blender 对象的列表、偏移量和坐标轴参数，并根据这些参数随机地修改这些对象的位置
def add_random_location(objects, amount=1,do_axis=(True, True, True)):
    """Add units to the locations of given objects"""
    for ob in objects:
        for i in range(3):
            if do_axis[i]:
                loc = ob.location
                # 产生一个（-1，1之间的随即偏移）
                loc[i] += random.randint(-amount, amount)


class TRANSFORM_OT_random_location(bpy.types.Operator):
    """Add units to the locations of selected objects"""
    bl_idname = "transform.add_random_location"
    bl_label = "Add random Location"

    amount: bpy.props.IntProperty(name="Amount",default=1)
    axis: bpy.props.BoolVectorProperty(name="Displace Axis",default=(True, True, True))

    @classmethod
    def poll(cls, context):
        return context.selected_objects
    
    # invoke 方法的目的是在用户执行操作时显示一个属性对话框，以便用户可以设置操作的参数或提供必要的信息。这种方法通常用于与用户进行交互，以确保操作执行时具有正确的参数
    # invoke_props_dialog 方法来显示与操作关联的属性对话框。self 在这里表示当前操作的实例。属性对话框通常用于让用户输入和配置操作的参数。
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    
    def execute(self, context):
        add_random_location(context.selected_objects,self.amount,self.axis)
        return {'FINISHED'}


class OBJECT_PT_very_simple(bpy.types.Panel):
    """Creates a Panel in the object context of the properties editor"""
    # still a draft: actual code will be added later
    """To add our panel to the Object Properties area, we must set its bl_space_type to 'PROPERTIES' and bl_context to 'object"""

    bl_label = "A Very Simple Panel"
    bl_idname = "VERYSIMPLE_PT_layout"
    bl_space_type = 'PROPERTIES'
    l_region_type = 'WINDOW'
    bl_context = 'object'
    max_objects = 3
    

    """Draw接受self和context参数。根据Python惯例,self是类的运行实例,而context包含有关Blender场景当前状态的信息"""
    def draw(self, context):
     # add layout elements
        layout = self.layout
        layout.label(text="A Very Simple Label",icon="INFO")
        layout.label(text="Isn't it great?",icon='QUESTION')
        layout.label(text="Smile", icon_value=custom_icons["smile_face"].icon_id)

        # 设置一个box面板框 ,有基本信息，他遍历的是bl_info中的内容，即该面板展示了里面的信息
        col = layout.column()
        box = col.box()
        split = box.split(factor=0.3)
        left_col = split.column()
        right_col = split.column()
        for k, v in bl_info.items():
            if not v:
            # ignore empty entries
                continue
            left_col.label(text=k)
            right_col.label(text=str(v))

        # 继续在下面添加显示object的信息：
        col.label(text="Scene Objects:")
        # 两列，省略号意味着逐行填充网格，因此要将row_major设置为True
        grid = col.grid_flow(columns=2, row_major=True)
        for i, ob in enumerate(context.scene.objects):
            if i > self.max_objects:
                objects_left = len(context.scene.objects)
                objects_left -= self.max_objects
                txt = f"... (more {objects_left} objects"
                grid.label(text=txt)
                break
            # 搜索到每个object对应的 OUTLINER_OB_{object_type},例如OUTLINER_OB_Cube,然后对应出图标
            grid.label(text=ob.name,icon=f'OUTLINER_OB_{ob.type}')

        # 添加一个删除按钮
        num_selected = len(context.selected_objects)
        if num_selected > 0:
            op_txt = f"Delete {num_selected} object"
            if num_selected > 1:
                op_txt += "s" # add plural 's'
            props = col.operator(bpy.ops.object.delete.idname(),text=op_txt)
            props.confirm = False
        # 添加禁止隐藏UI界面的规则
        else:
            to_disable = col.column()
            to_disable.enabled = False
            to_disable.operator(bpy.ops.object.delete.idname(),text="Delete Selected")
        


    def register():
        load_custom_icons()
        bpy.utils.register_class()
        bpy.utils.register_class(OBJECT_PT_very_simple)

    def unregister():
        bpy.utils.unregister_class(OBJECT_PT_very_simple)
        remove_custom_icons()