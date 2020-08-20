import bpy
import bpy_extras
import math

scene = bpy.context.scene

# The output path/file for the 2d pixel coordinates
outputFile2d = "../2d_marker-coordinates.csv"
# The output path/file for the 3d pixel coordinates
outputFile3d = "../3d_relative_marker-coordinates.csv"

#The list of object names for which to get coordinates of. Usually set up as empty objects with a copy location constraint to follow a bone
OBJs = ["snout", "snout_tip", "fore_paw_l", "elbow_r", "fore_paw_r", "digit_1_r", "digit_2_r", "digit_3_r", "digit_4_r", "digit_5_r"] 
# The reference object to use calculate 3d coordinates relative to 
reference_obj = "snout"
# The camera to get the 2d pixel coordinates with. The camera/render output settings must match the real videos to get the correct coordinates (ie. image width/height)
cam = "Camera_Side"

# The starting frame of the animation to export
frame_start = 1
# The ending frame of the animation to export
frame_end = 1000
# The number of frames to skip (ie export every frame(1) every second frame (2) etc.)
frame_step = 1




########### Not for editing #######
CSV_output = ""
CSV_output_mCBF = ""


# Main method to initialize csv output text and update scene/frame count before calling the coordinate calculator methods. Returns the two csv texts filled with coords
def getMarkers():
    frames = int((frame_end - frame_start)/frame_step)
    text2d = initCSVData()
    text3d = initCSVData_mCBF()
    for f in range(frames+1):
        print("Frame: ", (f* frame_step)+frame_start, end ="\r")
        text2d += "\nFrame" + str((f* frame_step)+frame_start)
        text3d += "\nFrame" + str((f* frame_step)+frame_start)
        bpy.context.scene.frame_set((f* frame_step)+frame_start)
        scene = bpy.context.scene
        bpy.context.view_layer.update()
        text2d = getPixelCoordinates(text2d)
        text3d = getRelativeCoordinates_mCBF(text3d)
    return text2d, text3d

# Initialize the first 3 rows of the csv file for the pixel coordinates (following deeplabcut frame labeling format)
def initCSVData():
    out = "scorer"
    for i in range(len(OBJs)):
        out += ",Blender,Blender"
    out += "\nbodyparts"
    for obj in OBJs:
        out += ","+obj+","+obj
    out += "\ncoords"
    for obj in OBJs:
        out += ",x,y"
    return out

# Initialize the first 3 rows of the csv file for the 3d relative coordinates (similar to deeplabcut with an dded column for z coords).
def initCSVData_mCBF():
    out = "scorer"
    for i in range(len(OBJs)):
        out += ",Blender,Blender,Blender"
    out += "\nbodyparts"
    for obj in OBJs:
        out += ","+obj+","+obj+","+obj
    out += "\ncoords"
    for obj in OBJs:
        out += ",x,y,z"
    return out

# Method to gather marker coordinates relative to the camera frame and transforming it to pixel coordinates taking into consideration the output render image frame size
def getPixelCoordinates(text):
    temp = text
    camera = bpy.data.objects[cam]    
    for obj in OBJs:
        obj_pos = bpy.data.objects[obj].matrix_world.to_translation()
        
        coords2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, obj_pos)

        
        render_scale = scene.render.resolution_percentage / 100
        render_size = (
            int(scene.render.resolution_x * render_scale),
            int(scene.render.resolution_y * render_scale),
        )
        
        u = round(coords2d.x * render_size[0])
        v = round(coords2d.y * render_size[1])
        j = render_size[1] - v
        i = u

        temp += "," + str(i) + "," + str(j)
    return temp

# Method to gather marker coordinates relative to the reference marker's world coordinate position
def getRelativeCoordinates_mCBF(text):
    temp = text
    camera = bpy.data.objects[cam]  
    root_pos =  bpy.data.objects[reference_obj].matrix_world.to_translation()
    for obj in OBJs:
        obj_pos = bpy.data.objects[obj].matrix_world.to_translation()
        
        i = obj_pos.x - root_pos.x
        j = obj_pos.y - root_pos.y
        k = obj_pos.z - root_pos.z

        temp += "," + str(i) + "," + str(j)  + "," + str(k)
    return temp

       


CSV_output, CSV_output_mCBF = getMarkers()


# Saving of files!
print("Saving 2D Pixel Coords...")
f = open(outputFile2d, 'w' )
f.writelines( CSV_output )
f.close()
print("Done!")

print("Saving 3D mCBF Coords...")
f = open(outputFile3d, 'w' )
f.writelines( CSV_output_mCBF )
f.close()
print("Done!")

