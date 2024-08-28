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
from . import bfu_fbx_export
from . import bfu_export_utils
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_naming
from .. import bfu_vertex_color
from .. import bfu_check_potential_error
from .. import bfu_export_logs
from .. import bfu_assets_manager



def ProcessStaticMeshExport(op, obj, desired_name=""):
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()

    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_asset_class(obj)
    asset_type = asset_class.get_asset_type_name(obj)
    dirpath = asset_class.get_obj_export_directory_path(obj)
    absdirpath = asset_class.get_obj_export_abs_directory_path(obj)

    if desired_name:
        final_name = desired_name
    else:
        final_name = obj.name

    file_name = asset_class.get_obj_file_name(obj, final_name, "")
    file_name_at = asset_class.get_obj_file_name(obj, final_name+"_AdditionalTrack", "") 

    MyAsset: bfu_export_logs.BFU_OT_UnrealExportedAsset = scene.UnrealExportedAssetsList.add()
    MyAsset.object = obj
    MyAsset.asset_name = obj.name
    MyAsset.asset_global_scale = obj.bfu_export_global_scale
    MyAsset.folder_name = obj.bfu_export_folder_name
    MyAsset.asset_type = asset_type

    file: bfu_export_logs.BFU_OT_FileExport = MyAsset.files.add()
    file.file_name = file_name
    file.file_extension = "fbx"
    file.file_path = dirpath
    file.file_type = "FBX"

    MyAsset.StartAssetExport()
    ExportSingleStaticMesh(op, dirpath, file.GetFileWithExtension(), obj)

    if not obj.bfu_export_as_lod_mesh:
        if (scene.text_AdditionalData and addon_prefs.useGeneratedScripts):
            
            file: bfu_export_logs.BFU_OT_FileExport = MyAsset.files.add()
            file.file_name = file_name_at
            file.file_extension = "json"
            file.file_path = dirpath
            file.file_type = "AdditionalTrack"
            bfu_export_utils.ExportAdditionalParameter(absdirpath, file.GetFileWithExtension(), MyAsset)

    MyAsset.EndAssetExport(True)
    return MyAsset


def ExportSingleStaticMesh(
        op,
        dirpath,
        filename,
        obj
        ):

    '''
    #####################################################
            #STATIC MESH
    #####################################################
    '''
    # Export a single Mesh

    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()

    bbpl.utils.safe_mode_set('OBJECT')

    bfu_utils.SelectParentAndDesiredChilds(obj)
    asset_name = bfu_export_utils.PrepareExportName(obj, False)
    duplicate_data = bfu_export_utils.DuplicateSelectForExport()
    bfu_export_utils.SetDuplicateNameForExport(duplicate_data)
    
    bfu_export_utils.ConvertSelectedCurveToMesh()
    bfu_export_utils.MakeSelectVisualReal()

    bfu_utils.ApplyNeededModifierToSelect()
    for selected_obj in bpy.context.selected_objects:
        if obj.bfu_convert_geometry_node_attribute_to_uv:
            attrib_name = obj.bfu_convert_geometry_node_attribute_to_uv_name
            bfu_export_utils.ConvertGeometryNodeAttributeToUV(selected_obj, attrib_name)
        bfu_vertex_color.bfu_vertex_color_utils.SetVertexColorForUnrealExport(selected_obj)
        bfu_export_utils.CorrectExtremUVAtExport(selected_obj)
        bfu_export_utils.SetSocketsExportTransform(selected_obj)
        bfu_export_utils.SetSocketsExportName(selected_obj)

    active = bpy.context.view_layer.objects.active
    asset_name.target_object = active

    bfu_utils.ApplyExportTransform(active, "Object")

    asset_name.SetExportName()
    static_export_procedure = obj.bfu_static_export_procedure

    save_use_simplify = bbpl.utils.SaveUserRenderSimplify()
    scene.render.use_simplify = False

    if (static_export_procedure == "ue-standard"):
        bfu_fbx_export.export_scene_fbx_with_custom_fbx_io(
            operator=op,
            context=bpy.context,
            filepath=bfu_export_utils.GetExportFullpath(dirpath, filename),
            check_existing=False,
            use_selection=True,
            global_matrix=bfu_export_utils.get_static_axis_conversion(active),
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'EMPTY', 'CAMERA', 'LIGHT', 'MESH', 'OTHER'},
            colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(active),
            use_custom_props=obj.bfu_export_with_custom_props,
            mesh_smooth_type="FACE",
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=False,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=obj.bfu_export_with_meta_data,
            primary_bone_axis=bfu_export_utils.get_final_export_primary_bone_axis(active),
            secondary_bone_axis=bfu_export_utils.get_final_export_secondary_bone_axis(active),
            mirror_symmetry_right_side_bones=active.bfu_mirror_symmetry_right_side_bones,
            use_ue_mannequin_bone_alignment=active.bfu_use_ue_mannequin_bone_alignment,
            disable_free_scale_animation=active.bfu_disable_free_scale_animation,
            use_space_transform=bfu_export_utils.get_static_export_use_space_transform(active),
            axis_forward=bfu_export_utils.get_static_export_axis_forward(active),
            axis_up=bfu_export_utils.get_static_export_axis_up(active),
            bake_space_transform=False
            
            )
    elif (static_export_procedure == "blender-standard"):
        bfu_fbx_export.export_scene_fbx(
            filepath=bfu_export_utils.GetExportFullpath(dirpath, filename),
            check_existing=False,
            use_selection=True,
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'EMPTY', 'CAMERA', 'LIGHT', 'MESH', 'OTHER'},
            colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(active),
            use_custom_props=obj.bfu_export_with_custom_props,
            mesh_smooth_type="FACE",
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=False,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=obj.bfu_export_with_meta_data,
            use_space_transform=bfu_export_utils.get_static_export_use_space_transform(active),
            axis_forward=bfu_export_utils.get_static_export_axis_forward(active),
            axis_up=bfu_export_utils.get_static_export_axis_up(active),
            bake_space_transform=False
            )

    save_use_simplify.LoadUserRenderSimplify()
    asset_name.ResetNames()

    bfu_vertex_color.bfu_vertex_color_utils.ClearVertexColorForUnrealExport(active)
    bfu_export_utils.ResetSocketsExportName(active)
    bfu_export_utils.ResetSocketsTransform(active)
    bfu_utils.CleanDeleteObjects(bpy.context.selected_objects)
    for data in duplicate_data.data_to_remove:
        data.RemoveData()

    bfu_export_utils.ResetDuplicateNameAfterExport(duplicate_data)

    for obj in scene.objects:
        bfu_utils.ClearAllBFUTempVars(obj)
