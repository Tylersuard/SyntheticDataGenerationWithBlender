import bpy

import os

import time

curr_dir = os.getcwd()

bpy.data.objects["Boeing_E3"].select_set(True)

#REMEMBER.  Every time you create something, that something gets selected.

bpy.ops.object.light_add(type='SUN')

bpy.ops.object.camera_add()

#bpy.ops.view3d.object_as_camera()

#select the plane again

bpy.data.objects["Boeing_E3"].select_set(True)
#bpy.ops.object.select_all(action='SELECT')


bpy.data.scenes["Scene"].camera = bpy.data.objects["Camera"]
bpy.ops.view3d.camera_to_view_selected()

#add code that says use nodes?
bpy.data.materials["body"].use_nodes = True
bpy.data.materials["wings"].use_nodes = True

#create 2 nodes in the "wings" material and link them
wings_TexImageNode = bpy.data.materials["wings"].node_tree.nodes.new(type = 'ShaderNodeTexImage')
wings_BrightContrastNode = bpy.data.materials["wings"].node_tree.nodes.new(type = 'ShaderNodeBrightContrast')

bpy.data.materials["wings"].node_tree.nodes["Bright/Contrast"].inputs[1].default_value = -0.2

links = bpy.data.materials["wings"].node_tree.links
links.new(bpy.data.materials["wings"].node_tree.nodes["Image Texture"].outputs[0],bpy.data.materials["wings"].node_tree.nodes["Bright/Contrast"].inputs[0])
links.new(bpy.data.materials["wings"].node_tree.nodes["Bright/Contrast"].outputs[0], bpy.data.materials["wings"].node_tree.nodes["Principled BSDF.001"].inputs[0])

i = 0

for filename in os.listdir(curr_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_filepath = os.path.join(curr_dir,filename)
        
        bpy.data.objects["Boeing_E3"].select_set(True)

        bpy.data.materials["body"].node_tree.nodes['Image Texture'].image = bpy.data.images.load(image_filepath)
        
        bpy.data.materials["wings"].node_tree.nodes['Image Texture'].image = bpy.data.images.load(image_filepath)

        print("Changed colors!")        

        bpy.context.scene.render.filepath = image_filepath[:-4] + "_render.jpg"

        bpy.ops.render.render(write_still = True)
        
        i+=1
                
        time.sleep(1)
