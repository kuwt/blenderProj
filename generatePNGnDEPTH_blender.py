import bpy
from bpy import context
scene = context.scene
##meter in unit
#################parameter################################
objectPath = "F:\\ronaldwork\\testData\\cadModel\\VShapePartsTemplate.STL"
scalingFactor = 0.001

namePrefix = "v"
basePath = "F:\\ronaldwork\\testData\\images"

#################CLEAR################################
for obj in bpy.data.objects:
    obj.select = True
bpy.ops.object.delete()
#################CAMERA################################
for obj in bpy.data.objects:
    obj.select = False
    
bpy.ops.object.camera_add()
bpy.data.objects['Camera'].select = True
scene.camera = context.object
bpy.context.active_object.rotation_mode = 'XYZ'
bpy.context.active_object.rotation_euler = (0,0 , 0)
bpy.context.active_object.location[0] = 0
bpy.context.active_object.location[1] = 0
bpy.context.active_object.location[2] = 1
#################LIGHT################################
for obj in bpy.data.objects:
    obj.select = False
    
bpy.ops.object.lamp_add(type='SUN')
bpy.data.objects['Sun'].select = True
bpy.context.active_object.rotation_mode = 'XYZ'
bpy.context.active_object.rotation_euler = (0,0 , 0)
bpy.context.active_object.location[0] = 0
bpy.context.active_object.location[1] = 0
bpy.context.active_object.location[2] = 1

#################TEMPLATE################################
bpy.ops.import_mesh.stl(filepath=objectPath)
for obj in bpy.data.objects:
    obj.select = False
bpy.data.objects['VShapePartsTemplate'].select = True
bpy.context.active_object.location[0] = 0
bpy.context.active_object.location[1] = 0
bpy.context.active_object.location[2] = 0
bpy.context.active_object.scale[0] = scalingFactor
bpy.context.active_object.scale[1] = scalingFactor
bpy.context.active_object.scale[2] = scalingFactor

###################create rotation steps#######################################
angleStep = 10
numofAlphaStep = int(360/angleStep)
numofBetaStep = 1  #int(180/angleStep)
numofGammaStep = 1# int(360/angleStep)

angles = []
for alphaIdx in range(0,numofAlphaStep):
    for betaIdx in range(0,numofBetaStep):
        for gammaIdx in range(0,numofGammaStep):
            alpha = alphaIdx * angleStep
            beta = betaIdx * angleStep
            gamma = gammaIdx * angleStep
            angles.append([alpha,beta,gamma])


 ###################SAVE RGB################################################
# Set up rendering of depth map:
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

# clear default nodes
for n in tree.nodes:
    tree.nodes.remove(n)

# create input render layer node
rl = tree.nodes.new('CompositorNodeRLayers')

fileOutput = tree.nodes.new(type="CompositorNodeOutputFile")
fileOutput.base_path = basePath
fileOutput.format.file_format = "PNG"
links.new(rl.outputs[0], fileOutput.inputs[0])
    
###################SAVE DEPTH###################################################
# Set up rendering of depth map:
fileOutputDepth = tree.nodes.new(type="CompositorNodeOutputFile")
fileOutputDepth.base_path = basePath
fileOutputDepth.format.file_format = "OPEN_EXR"
links.new(rl.outputs[2], fileOutputDepth.inputs[0])

    
###################main loop#######################################
idx = 0
for angle in angles:
    pi = 3.1415926
    alpha = angle[0]
    beta = angle[1]
    gamma = angle[2]
    alphaRAD = alpha * pi / 180
    betaRAD = beta * pi / 180
    gammaRAD = gamma * pi / 180
    
    bpy.context.active_object.rotation_mode = 'XYZ'
    bpy.context.active_object.rotation_euler = (alphaRAD,betaRAD , gammaRAD)
    
    rgbPath = "{0}_rgb_{1:06d}_".format(namePrefix,idx)
    depthPath = "{0}_depth_{1:06d}_".format(namePrefix,idx)
    fileOutput.file_slots[0].path = rgbPath
    fileOutputDepth.file_slots[0].path = depthPath
    bpy.ops.render.render()
    idx = idx+1