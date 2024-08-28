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
from . import bfu_export_single_alembic_animation
from . import bfu_export_single_fbx_action
from . import bfu_export_single_camera
from . import bfu_export_single_spline
from . import bfu_export_single_fbx_nla_anim
from . import bfu_export_single_skeletal_mesh
from . import bfu_export_single_static_mesh
from . import bfu_export_single_static_mesh_collection
from . import bfu_export_single_groom_simulation
from .. import bfu_cached_asset_list
from .. import bps
from .. import bbpl
from .. import bfu_assets_manager
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_camera
from .. import bfu_spline
from .. import bfu_static_mesh
from .. import bfu_skeletal_mesh
from .. import bfu_alembic_animation
from .. import bfu_groom




def IsValidActionForExport(scene, obj, animType):
    if animType == "Action":
        if scene.anin_export:
            if obj.bfu_skeleton_export_procedure == 'auto-rig-pro':
                if bfu_basics.CheckPluginIsActivated('auto_rig_pro-master'):
                    return True
            else:
                return True
        else:
            return False
    elif animType == "Pose":
        if scene.anin_export:
            if obj.bfu_skeleton_export_procedure == 'auto-rig-pro':
                if bfu_basics.CheckPluginIsActivated('auto_rig_pro-master'):
                    return True
            else:
                return True
        else:
            return False
    elif animType == "NLA":
        if scene.anin_export:
            if obj.bfu_skeleton_export_procedure == 'auto-rig-pro':
                return False
            else:
                return True
        else:
            False
    else:
        print("Error in IsValidActionForExport() animType not found: ", animType)
    return False


def IsValidObjectForExport(scene, obj):
    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_asset_class(obj)
    return asset_class.can_export_obj_asset(obj)

def PrepareSceneForExport():
    for obj in bpy.data.objects:
        if obj.hide_select:
            obj.hide_select = False
        if obj.hide_viewport:
            obj.hide_viewport = False
        if obj.hide_get():
            obj.hide_set(False)

    for col in bpy.data.collections:
        if col.hide_select:
            col.hide_select = False
        if col.hide_viewport:
            col.hide_viewport = False

    for vlayer in bpy.context.scene.view_layers:
        layer_collections = bbpl.utils.get_layer_collections_recursive(vlayer.layer_collection)
        for layer_collection in layer_collections:
            if layer_collection.exclude:
                layer_collection.exclude = False
            if layer_collection.hide_viewport:
                layer_collection.hide_viewport = False

def process_export(op):
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    export_filter = scene.bfu_export_selection_filter

    local_view_areas = bbpl.scene_utils.move_to_global_view()

    MyCurrentDataSave = bbpl.utils.UserSceneSave()
    MyCurrentDataSave.save_current_scene()
    
    if export_filter == "default":
        PrepareSceneForExport()
        final_asset_cache = bfu_cached_asset_list.GetfinalAssetCache()
        final_asset_list_to_export = final_asset_cache.GetFinalAssetList()

    elif export_filter == "only_object" or export_filter == "only_object_action":
        final_asset_cache = bfu_cached_asset_list.GetfinalAssetCache()
        final_asset_list_to_export = final_asset_cache.GetFinalAssetList() #Get finial assets visible only
        PrepareSceneForExport()


    bbpl.utils.safe_mode_set('OBJECT', MyCurrentDataSave.user_select_class.user_active)

    if addon_prefs.revertExportPath:
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_static_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_skeletal_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_alembic_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_groom_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_camera_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_spline_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_other_file_path))

    obj_list = []  # Do a simple list of Objects to export
    action_list = []  # Do a simple list of Action to export
    col_list = []  # Do a simple list of Collection to export

    export_all_from_asset_list(op, final_asset_list_to_export)

    for Asset in final_asset_list_to_export:
        if Asset.asset_type == "Action" or Asset.asset_type == "Pose":
            if Asset.obj not in action_list:
                action_list.append(Asset.action.name)
            if Asset.obj not in obj_list:
                obj_list.append(Asset.obj)

        elif Asset.asset_type == "Collection StaticMesh":
            if Asset.obj not in col_list:
                col_list.append(Asset.obj)

        else:
            if Asset.obj not in obj_list:
                obj_list.append(Asset.obj)

    MyCurrentDataSave.reset_select_by_name()
    MyCurrentDataSave.reset_scene_at_save(print_removed_items = True)

    # Clean actions
    for action in bpy.data.actions:
        if action.name not in MyCurrentDataSave.action_names:
            bpy.data.actions.remove(action)

    bbpl.scene_utils.move_to_local_view(local_view_areas)


def export_all_from_asset_list(op, asset_list: bfu_cached_asset_list.AssetToExport):
    export_collection_from_asset_list(op, asset_list)
    export_camera_from_asset_list(op, asset_list)
    export_spline_from_asset_list(op, asset_list)
    export_static_mesh_from_asset_list(op, asset_list)
    export_skeletal_mesh_from_asset_list(op, asset_list)
    export_alembic_from_asset_list(op, asset_list)
    export_groom_from_asset_list(op, asset_list)
    export_animation_from_asset_list(op, asset_list)
    export_nonlinear_animation_from_asset_list(op, asset_list)

def export_collection_from_asset_list(op, asset_list: bfu_cached_asset_list.AssetToExport):
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    print("Start Export collection(s)")

    if scene.static_collection_export:
        collection_asset_cache = bfu_cached_asset_list.GetCollectionAssetCache()
        collection_export_asset_list = collection_asset_cache.GetCollectionAssetList()
        for col in collection_export_asset_list:
            # Save current start/end frame
            UserStartFrame = scene.frame_start
            UserEndFrame = scene.frame_end
            bfu_export_single_static_mesh_collection.ProcessCollectionExport(op, col)

            # Resets previous start/end frame
            scene.frame_start = UserStartFrame
            scene.frame_end = UserEndFrame



def export_camera_from_asset_list(op, asset_list: bfu_cached_asset_list.AssetToExport):
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    print("Start Export camera(s)")

    camera_list = []

    use_camera_evaluate = (scene.text_AdditionalData and addon_prefs.useGeneratedScripts)
    if use_camera_evaluate:
        multi_camera_tracks = bfu_camera.bfu_camera_data.BFU_MultiCameraTracks()
        multi_camera_tracks.set_start_end_frames(scene.frame_start, scene.frame_end+1)
    
    # Preparre asset to export
    for asset in asset_list:
        asset: bfu_cached_asset_list.AssetToExport
        if asset.asset_type == bfu_camera.bfu_camera_config.asset_type_name:
            obj = asset.obj
            if obj.bfu_export_type == "export_recursive":
                if bfu_camera.bfu_camera_utils.is_camera(obj) and IsValidObjectForExport(scene, obj):                    
                    camera_list.append(obj)
                    multi_camera_tracks.add_camera_to_evaluate(obj)

    if use_camera_evaluate:
        multi_camera_tracks.evaluate_all_cameras()

    #Start export
    for obj in camera_list:
        # Save current start/end frame
        UserStartFrame = scene.frame_start
        UserEndFrame = scene.frame_end

        if use_camera_evaluate:
            camera_tracks = multi_camera_tracks.get_evaluate_camera_data(obj)
        else:
            camera_tracks = None
        bfu_export_single_camera.ProcessCameraExport(op, obj, camera_tracks)

        # Resets previous start/end frame
        scene.frame_start = UserStartFrame
        scene.frame_end = UserEndFrame
        #UpdateExportProgress()

def export_spline_from_asset_list(op, asset_list: bfu_cached_asset_list.AssetToExport):
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    print("Start Export spline(s)")

    spline_list = []

    use_spline_evaluate = (scene.text_AdditionalData and addon_prefs.useGeneratedScripts)
    if use_spline_evaluate:
        multi_spline_tracks = bfu_spline.bfu_spline_data.BFU_MultiSplineTracks()
    
    # Preparre asset to export
    for asset in asset_list:
        asset: bfu_cached_asset_list.AssetToExport
        if asset.asset_type == bfu_spline.bfu_spline_config.asset_type_name:
            obj = asset.obj
            if obj.bfu_export_type == "export_recursive":
                if bfu_spline.bfu_spline_utils.is_spline(obj) and IsValidObjectForExport(scene, obj):                    
                    spline_list.append(obj)
                    multi_spline_tracks.add_spline_to_evaluate(obj)

    if use_spline_evaluate:
        multi_spline_tracks.evaluate_all_splines()

    #Start export
    for obj in spline_list:

        if use_spline_evaluate:
            spline_tracks = multi_spline_tracks.get_evaluate_spline_data(obj)
        else:
            spline_tracks = None
        bfu_export_single_spline.ProcessSplineExport(op, obj, spline_tracks)


def export_static_mesh_from_asset_list(op, asset_list: [bfu_cached_asset_list.AssetToExport]):
    scene = bpy.context.scene

    print("Start Export StaticMesh(s)")
    for asset in asset_list:
        asset: bfu_cached_asset_list.AssetToExport
        if asset.asset_type == bfu_static_mesh.bfu_static_mesh_config.asset_type_name:
            obj = asset.obj
            if obj.bfu_export_type == "export_recursive":
                if bfu_static_mesh.bfu_static_mesh_utils.is_static_mesh(obj) and IsValidObjectForExport(scene, obj):

                    # Save current start/end frame
                    UserStartFrame = scene.frame_start
                    UserEndFrame = scene.frame_end
                    bfu_export_single_static_mesh.ProcessStaticMeshExport(op, obj)

                    # Resets previous start/end frame
                    scene.frame_start = UserStartFrame
                    scene.frame_end = UserEndFrame
                    #UpdateExportProgress()

def export_skeletal_mesh_from_asset_list(op, asset_list: bfu_cached_asset_list.AssetToExport):
    scene = bpy.context.scene

    print("Start Export SkeletalMesh(s)")
    for asset in asset_list:
        asset: bfu_cached_asset_list.AssetToExport
        if asset.asset_type == bfu_skeletal_mesh.bfu_skeletal_mesh_config.asset_type_name:
            armature = asset.obj
            mesh_parts = asset.obj_list
            desired_name = asset.name
            if armature.bfu_export_type == "export_recursive":
                if bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(armature) and IsValidObjectForExport(scene, armature):
                    # Save current start/end frame
                    UserStartFrame = scene.frame_start
                    UserEndFrame = scene.frame_end
                    bfu_export_single_skeletal_mesh.ProcessSkeletalMeshExport(op, armature, mesh_parts, desired_name)

                    # Resets previous start/end frame
                    scene.frame_start = UserStartFrame
                    scene.frame_end = UserEndFrame
                    #UpdateExportProgress()

def export_alembic_from_asset_list(op, asset_list: bfu_cached_asset_list.AssetToExport):
    scene = bpy.context.scene

    print("Start Export Alembic Animation(s)")
    
    for asset in asset_list:
        asset: bfu_cached_asset_list.AssetToExport
        if asset.asset_type == bfu_alembic_animation.bfu_alembic_animation_config.asset_type_name:
            obj = asset.obj
            if obj.bfu_export_type == "export_recursive":        
                if bfu_alembic_animation.bfu_alembic_animation_utils.is_alembic_animation(obj) and IsValidObjectForExport(scene, obj):
                    # Save current start/end frame
                    UserStartFrame = scene.frame_start
                    UserEndFrame = scene.frame_end
                    bfu_export_single_alembic_animation.ProcessAlembicAnimationExport(obj)

                    # Resets previous start/end frame
                    scene.frame_start = UserStartFrame
                    scene.frame_end = UserEndFrame
                    #UpdateExportProgress()

def export_groom_from_asset_list(op, asset_list: bfu_cached_asset_list.AssetToExport):
    scene = bpy.context.scene

    print("Start Export Groom Simulation(s)")
    for asset in asset_list:
        asset: bfu_cached_asset_list.AssetToExport
        if asset.asset_type == bfu_groom.bfu_groom_config.asset_type_name:
            obj = asset.obj
            if obj.bfu_export_type == "export_recursive":        
                if bfu_groom.bfu_groom_utils.is_groom(obj) and IsValidObjectForExport(scene, obj):
                    # Save current start/end frame
                    UserStartFrame = scene.frame_start
                    UserEndFrame = scene.frame_end
                    bfu_export_single_groom_simulation.ProcessGroomSimulationExport(obj)

                    # Resets previous start/end frame
                    scene.frame_start = UserStartFrame
                    scene.frame_end = UserEndFrame
                    #UpdateExportProgress()

def export_animation_from_asset_list(op, asset_list: bfu_cached_asset_list.AssetToExport):
    scene = bpy.context.scene

    for asset in asset_list:
        asset: bfu_cached_asset_list.AssetToExport
        if asset.asset_type == "Action" or asset.asset_type == "Pose":
            obj = asset.obj
            if obj.bfu_export_type == "export_recursive":    
                if bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj) and obj.visible_get():
                    # Action animation
                    print("Start Export Action(s)")
                    action_curve_scale = None
                    animation_asset_cache = bfu_cached_asset_list.GetAnimationAssetCache(obj)
                    animation_to_export = animation_asset_cache.GetAnimationAssetList()
                    for action in animation_to_export:
                        if action.name == asset.action.name:
                            animType = bfu_utils.GetActionType(action)

                            # Action and Pose
                            if IsValidActionForExport(scene, obj, animType):
                                if animType == "Action" or animType == "Pose":
                                    # Save current start/end frame
                                    UserStartFrame = scene.frame_start
                                    UserEndFrame = scene.frame_end
                                    action_curve_scale = bfu_export_single_fbx_action.ProcessActionExport(op, obj, action, action_curve_scale)

                                    # Resets previous start/end frame
                                    scene.frame_start = UserStartFrame
                                    scene.frame_end = UserEndFrame
                                    #UpdateExportProgress()
                    if action_curve_scale:
                        action_curve_scale.ResetScaleAfterExport()

def export_nonlinear_animation_from_asset_list(op, asset_list: bfu_cached_asset_list.AssetToExport):
    scene = bpy.context.scene

    for asset in asset_list:
        asset: bfu_cached_asset_list.AssetToExport
        if asset.asset_type == "NlAnim":
            obj = asset.obj
            if obj.bfu_export_type == "export_recursive":    
                if bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj) and obj.visible_get():
                    # NLA animation
                    print("Start Export NLA(s)")
                    if IsValidActionForExport(scene, obj, "NLA"):
                        if obj.bfu_anim_nla_use:
                            # Save current start/end frame
                            UserStartFrame = scene.frame_start
                            UserEndFrame = scene.frame_end
                            bfu_export_single_fbx_nla_anim.ProcessNLAAnimExport(op, obj)

                            # Resets previous start/end frame
                            scene.frame_start = UserStartFrame
                            scene.frame_end = UserEndFrame

