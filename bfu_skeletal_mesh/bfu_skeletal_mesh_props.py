# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================


import bpy
from . import bfu_skeletal_mesh_utils
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl


def get_preset_values():
    preset_values = [
        'obj.bfu_export_skeletal_mesh_as_static_mesh',
        'obj.bfu_create_sub_folder_with_skeletal_mesh_name'
        ]
    return preset_values

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.bfu_export_skeletal_mesh_as_static_mesh = bpy.props.BoolProperty(
        name="Export as Static Mesh",
        description="If true this mesh will be exported as a Static Mesh",
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )
    
    bpy.types.Object.bfu_create_sub_folder_with_skeletal_mesh_name = bpy.props.BoolProperty(
        name="Create SK Sub Folder",
        description="Create a subfolder with the armature name to avoid asset conflicts during the export. (Recommended)",
        override={'LIBRARY_OVERRIDABLE'},
        default=True
        )

    bpy.types.Scene.bfu_skeleton_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Skeleton")
    bpy.types.Scene.bfu_modular_skeletal_mesh_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Modular Skeletal Mesh")



def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bfu_modular_skeletal_mesh_properties_expanded
    del bpy.types.Scene.bfu_skeleton_properties_expanded
    
    del bpy.types.Object.bfu_create_sub_folder_with_skeletal_mesh_name
    del bpy.types.Object.bfu_export_skeletal_mesh_as_static_mesh