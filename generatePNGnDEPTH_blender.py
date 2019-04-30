import bpy

#################SELECT################################
bpy.data.objects['VShapePartsTemplate'].select = True


#################SELECT################################
namePrefix = "v"
basePath = "F:\\ronaldwork\\testData\\images"
###################create rotation steps#######################################
angleStep = 15
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