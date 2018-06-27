import bpy
import mathutils
import random
import os
import sys

NAME_PROJECT = 'AccubuildFraming'

LEFT_CAM = 'Left'
RIGHT_CAM = 'Right'
CHECKERBOARD = 'checkerboard'

CHECKBRD_DIST           = 5
CHECKBRD_DIST_VAR       = 3
CHECKBRD_DIST_DELTA_VAR = 0
CHECKBRD_ANGLE          = 0
CHECKBRD_ANGLE_VAR      = 0.3
CHECKBRD_SCALE          = 0.5

IMAGES_NUM    = 30
IMAGES_OUTPUT = '/src/calibration/'

STD_VEC_EULER = mathutils.Vector([0,0,-1])

def get_fwd_rot(left_cam,right_cam):
    fwd_rot = []
    left_rot = left_cam.rotation_euler
    right_rot = right_cam.rotation_euler
    for i in range(3):
        fwd_rot.insert(i,(right_rot[i] - left_rot[i])/2 + left_rot[i])
    return mathutils.Euler(fwd_rot,'XYZ')

def get_rel_vec(left_cam, right_cam):
    rot = get_fwd_rot(left_cam,right_cam)
    rel_vec = STD_VEC_EULER.copy()
    rel_vec.rotate(rot)
    return rel_vec

def get_cam_midpoint(left_cam,right_cam):
    left_pos = left_cam.location
    right_pos = right_cam.location
    return (left_pos - right_pos)/2 + right_pos

def get_render(camera,output_path):
    current_scene = bpy.data.scenes['Scene']
    current_scene.render.filepath = output_path
    current_scene.camera = camera
    bpy.ops.render.render( write_still=True )

def main():
    fpath = os.path.dirname(os.path.realpath(__file__))
    proj_path = fpath[0:fpath.rfind(NAME_PROJECT)] + NAME_PROJECT
    output_path = proj_path + IMAGES_OUTPUT
    sample_path = proj_path + '/src/'
    
    left_cam = bpy.data.objects[LEFT_CAM]
    right_cam = bpy.data.objects[RIGHT_CAM]
    
    checkerboard = bpy.data.objects[CHECKERBOARD]
    checkerboard.scale = [CHECKBRD_SCALE,CHECKBRD_SCALE,CHECKBRD_SCALE]
    
    midpoint = get_cam_midpoint(left_cam,right_cam)
    cam_dir = get_fwd_rot(left_cam,right_cam)
    rel_vec = get_rel_vec(left_cam,right_cam)
    hiding_spot = midpoint - rel_vec
    
    excluded_obj_list = list(bpy.data.objects)
    
    excluded_obj_list.remove(left_cam)
    excluded_obj_list.remove(right_cam)
    excluded_obj_list.remove(checkerboard)
    
    for obj in excluded_obj_list:
        if obj.type != 'LAMP':
            obj.hide_render = True
    checkerboard.hide_render = False
    for i in range(IMAGES_NUM):
        checkerboard.location = midpoint + (CHECKBRD_DIST + random.uniform(-CHECKBRD_DIST_VAR, CHECKBRD_DIST_VAR)) * rel_vec
        checkerboard.delta_rotation_euler = mathutils.Euler([ random.uniform(-CHECKBRD_ANGLE_VAR,CHECKBRD_ANGLE_VAR), random.uniform(-CHECKBRD_ANGLE_VAR,CHECKBRD_ANGLE_VAR), random.uniform(-CHECKBRD_ANGLE_VAR,CHECKBRD_ANGLE_VAR)])
        get_render(left_cam,output_path + LEFT_CAM + "/" + LEFT_CAM + str(i))
        print(output_path + LEFT_CAM + "/" + LEFT_CAM + str(i))
        get_render(right_cam,output_path + RIGHT_CAM + "/" + RIGHT_CAM + str(i))
        print(output_path + RIGHT_CAM + "/" + RIGHT_CAM + str(i))
    
    for obj in excluded_obj_list:
        obj.hide_render = False
    
    checkerboard.hide_render = True
    
    get_render(left_cam,sample_path + 'left.png')
    get_render(right_cam,sample_path + 'right.png')

main()
