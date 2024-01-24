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
from .. import bbpl
from ..bbpl.blender_layout.layout_expend_section.types import (
        BBPL_UI_ExpendSection,
        )

class BFU_UI_ExpendSection(BBPL_UI_ExpendSection):
    pass


classes = (
    BFU_UI_ExpendSection,
)



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_object_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Object Properties")
    bpy.types.Scene.bfu_object_lod_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Lod")
    bpy.types.Scene.bfu_object_collision_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Collision")
    bpy.types.Scene.bfu_object_material_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Material")
    bpy.types.Scene.bfu_object_vertex_color_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Vertex color")
    bpy.types.Scene.bfu_object_light_map_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Light map")
    bpy.types.Scene.bfu_object_uv_map_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="UV map")

    bpy.types.Scene.bfu_animation_action_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Actions Properties")
    bpy.types.Scene.bfu_animation_action_advanced_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Actions Advanced Properties")
    bpy.types.Scene.bfu_animation_nla_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="NLA Properties")
    bpy.types.Scene.bfu_animation_nla_advanced_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="NLA Advanced Properties")
    bpy.types.Scene.bfu_animation_advanced_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Animation Advanced Properties")

    bpy.types.Scene.bfu_skeleton_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Skeleton")
    bpy.types.Scene.bfu_engine_ref_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Engine Refs")
    bpy.types.Scene.bfu_modular_skeletal_mesh_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Modular Skeletal Mesh")

    bpy.types.Scene.bfu_collection_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Collection Properties")
    bpy.types.Scene.bfu_object_advanced_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Object advanced Properties")
    bpy.types.Scene.bfu_camera_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Camera")
    bpy.types.Scene.bfu_collision_socket_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Collision and Socket")
    bpy.types.Scene.bfu_lightmap_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Light Map")
    bpy.types.Scene.bfu_nomenclature_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Nomenclature")
    bpy.types.Scene.bfu_export_filter_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Export filters")
    bpy.types.Scene.bfu_export_process_properties_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Export process")
    bpy.types.Scene.bfu_script_tool_expanded = bpy.props.PointerProperty(type=BFU_UI_ExpendSection, name="Copy Import Script")

    bpy.types.Scene.bfu_active_tab = bpy.props.EnumProperty(
        items=(
            ('OBJECT', 'Object', 'Object tab.'),
            ('SCENE', 'Scene', 'Scene and world tab.')
            )
        )

    bpy.types.Scene.bfu_active_object_tab = bpy.props.EnumProperty(
        items=(
            ('GENERAL', 'General', 'General object tab.'),
            ('ANIM', 'Animations', 'Animations tab.'),
            ('MISC', 'Misc', 'Misc tab.'),
            ('ALL', 'All', 'All tabs.')
            )
        )

    bpy.types.Scene.bfu_active_scene_tab = bpy.props.EnumProperty(
        items=(
            ('GENERAL', 'Scene', 'General scene tab'),
            ('ALL', 'All', 'All tabs.')
            )
        )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bfu_object_properties_expanded
    del bpy.types.Scene.bfu_object_lod_properties_expanded
    del bpy.types.Scene.bfu_object_collision_properties_expanded
    del bpy.types.Scene.bfu_object_material_properties_expanded
    del bpy.types.Scene.bfu_object_vertex_color_properties_expanded
    del bpy.types.Scene.bfu_object_light_map_properties_expanded
    del bpy.types.Scene.bfu_object_uv_map_properties_expanded

    del bpy.types.Scene.bfu_animation_action_properties_expanded
    del bpy.types.Scene.bfu_animation_action_advanced_properties_expanded
    del bpy.types.Scene.bfu_animation_nla_properties_expanded
    del bpy.types.Scene.bfu_animation_nla_advanced_properties_expanded
    del bpy.types.Scene.bfu_animation_advanced_properties_expanded

    del bpy.types.Scene.bfu_skeleton_properties_expanded
    del bpy.types.Scene.bfu_engine_ref_properties_expanded
    del bpy.types.Scene.bfu_modular_skeletal_mesh_properties_expanded

    del bpy.types.Scene.bfu_collection_properties_expanded
    del bpy.types.Scene.bfu_object_advanced_properties_expanded
    del bpy.types.Scene.bfu_collision_socket_expanded
    del bpy.types.Scene.bfu_lightmap_expanded
    del bpy.types.Scene.bfu_nomenclature_properties_expanded
    del bpy.types.Scene.bfu_export_filter_properties_expanded
    del bpy.types.Scene.bfu_export_process_properties_expanded
    del bpy.types.Scene.bfu_script_tool_expanded

    del bpy.types.Scene.bfu_active_object_tab
