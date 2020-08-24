# Simple .MTL reader.
# Run after .OBJ import.
# Creates a basic Redshift material with a texture map.

# EXAMPLE: Expected format.
#newmtl _4_2_                       <- Material name.
#Ns 96.078431                       <- Specular intensity
#Ka 0.000000 0.000000 0.000000      <- Ambient color.
#Kd 0.640000 0.640000 0.640000      <- Diffuse color.
#Ks 0.500000 0.500000 0.500000      <- Specular color.
#Ni 1.000000                        <- Index of refraction.
#d 1.000000                         <- Opacity.
#illum 2                            <- Illumination model, expect 2..probably will not support.
#map_Kd 21_budova/_4_2_.jpg         <- Map name.
#map_Kn 21_budova/_4_2_n.jpg        <- Map name.
 
import hou,os, re, platform

def returnValidHoudiniNodeName(passedItem):
    # Thanks to Graham on OdForce for this function!
    # Replace any illegal characters for node names here.
    return re.sub("[^0-9a-zA-Z\.]+", "_", passedItem)

def installNormalMap(passedSHOP, passedImageFilePath, passedName):
    rs_vop = hou.node("%s/%s" % (passedSHOP, passedName))
    if rs_vop != None:
        rs_bump = hou.node("%s/%s/rs_Bump_%s" % (passedSHOP, passedName, passedName))  # Detect existing rsBumpMap node.
        if rs_bump != None:
            rs_nor = rs_vop.createNode("redshift::TextureSampler",returnValidHoudiniNodeName("rs_Nor_%s" % passedName))
            if rs_nor != None:
                if passedImageFilePath.find("NOT_DETECTED")==-1:
                    # Only plug in normal map if the normal map was specified.
                    rs_bump.setInput(0,rs_nor)
                    rs_bump.parm("scale").set(1.0)
                    rs_bump.parm("inputType").set("1")              # tangent space type for normal maps.
                    rs_nor.parm("tex0").set(passedImageFilePath)    # set the filename to the normal map texture.
                    rs_nor.parm("tex0_gammaoverride").set(1)
        
def createRedshiftImageMapMaterial(passedSHOP, passedImageFilePath, passedName, passedDiffuse=[0,0,0], passedSpecular=[0,0,0], passedWeight=0.1, passedIOR=1.0, passedOpacity=1.0):
    #print "->%s [%s] [%s]" % (passedSHOP, passedImageFilePath, passedName)
    rs_vop = hou.node(passedSHOP).createNode("redshift_vopnet",passedName)
    if rs_vop != None:
        rs_output = hou.node("%s/%s/redshift_material1" % (passedSHOP, passedName))  # Detect the default closure node that should be created by the redshift_vopnet.
        if rs_output != None:
            # Create.
            rs_mat = rs_vop.createNode("redshift::Material","rs_Mat")
            if rs_mat != None:
                # Set passed values.
                rs_mat.parm("diffuse_colorr").set(passedDiffuse[0])
                rs_mat.parm("diffuse_colorg").set(passedDiffuse[1])
                rs_mat.parm("diffuse_colorb").set(passedDiffuse[2])
                rs_mat.parm("refl_colorr").set(passedSpecular[0])
                rs_mat.parm("refl_colorg").set(passedSpecular[1])
                rs_mat.parm("refl_colorb").set(passedSpecular[2])
                rs_mat.parm("refl_weight").set(passedWeight)
                rs_mat.parm("refl_roughness").set(0.23)         # Hard coded to soft blur reflection.
                rs_mat.parm("refl_ior").set(passedIOR)
                rs_mat.parm("opacity_colorr").set(passedOpacity)
                rs_mat.parm("opacity_colorg").set(passedOpacity)
                rs_mat.parm("opacity_colorb").set(passedOpacity)
                
                rs_tex = rs_vop.createNode("redshift::TextureSampler",returnValidHoudiniNodeName("rs_Tex_%s" % passedName))
                if rs_tex != None:
                    # Wire
                    try:
                        rs_output.setInput(0,rs_mat)
                        can_continue = True
                    except:
                        can_continue = False
                    if can_continue:
                        if passedImageFilePath.find("NOT_DETECTED")==-1:
                            # Only plug in texture if the texture map was specified.
                            rs_mat.setInput(0,rs_tex)                       # input #0 is diffuse color.
                        extension = os.path.splitext(passedImageFilePath)[1]
                        files_with_alphas = [".png",".PNG",".tga",".TGA",".tif",".TIF",".tiff",".TIFF",".exr",".EXR"]
                        if extension in files_with_alphas:
                            # Place a sprite after the rsMaterial to implment opacity support.
                            rs_sprite = rs_vop.createNode("redshift::Sprite",returnValidHoudiniNodeName("rs_Sprite_%s" % passedName))
                            if rs_sprite != None:
                                rs_sprite.parm("tex0").set(passedImageFilePath)    # set the filename to the texture.
                                rs_sprite.parm("mode").set("1")
                                rs_sprite.setInput(0,rs_mat)
                                rs_output.setInput(0,rs_sprite)
                                #rs_mat.setInput(46,rs_tex)                  # input #46 is opacity color (i.e. alpha).

                        rs_tex.parm("tex0").set(passedImageFilePath)    # set the filename to the texture.
                        
                        # Remove luminosity from texture using a color corrector.
                        rs_cc = rs_vop.createNode("redshift::RSColorCorrection",returnValidHoudiniNodeName("rs_CC_%s" % passedName))
                        if rs_cc != None:
                            rs_cc.setInput(0,rs_tex)
                            
                            rs_cc.parm("saturation").set(0)
                            # Add a slight bump using the greyscale value of the diffuse texture.
                            rs_bump = rs_vop.createNode("redshift::BumpMap",returnValidHoudiniNodeName("rs_Bump_%s" % passedName))
                            if rs_bump != None:
                                rs_bump.setInput(0,rs_cc)
                                rs_bump.parm("scale").set(0.25)          # Hard coded, feel free to adjust.
                                rs_output.setInput(2,rs_bump)
                                                
                        # Layout.
                        rs_vop.moveToGoodPosition() 
                        rs_tex.moveToGoodPosition()
                        rs_cc.moveToGoodPosition() 
                        rs_bump.moveToGoodPosition()
                        rs_mat.moveToGoodPosition()
                        rs_output.moveToGoodPosition()
                else:
                    print "problem creating redshift::TextureSampler node."
            else:
                print "problem creating redshift::Material node."
        else:
            print "problem detecting redshift_material1 automatic closure."
    else:
        print "problem creating redshift vop net?"
 
cur_mat = None

# Select MTL file to process...
n = 5
if n==0:
    texture_path = '/media/banedesh/Storage/Documents/Models/Blendswap/cc0_Destruction_Assets/Building_Budova~/01'
    file_name = '/media/banedesh/Storage/Documents/Models/Blendswap/cc0_Destruction_Assets/Building_Budova~/01/21_budova.mtl'
if n==1:
    texture_path = '/media/banedesh/Storage/Documents/Models/Blendswap/cc0_Destruction_Assets/Colosseums/Colosseum4'
    file_name = '/media/banedesh/Storage/Documents/Models/Blendswap/cc0_Destruction_Assets/Colosseums/Colosseum4/Colosseum.mtl'
if n==2:
    texture_path = '/media/banedesh/Storage/Documents/Models/Blendswap/cc0_Destruction_Assets/Fancy_Architecture/002_Sanpietro'
    file_name = '/media/banedesh/Storage/Documents/Models/Blendswap/cc0_Destruction_Assets/Fancy_Architecture/002_Sanpietro/sanpietro.mtl'
if n==3:
    texture_path = 'C:\Users\Mitzumi\Documents\Models\Blendswap\cc0_14_building_set\obj'
    file_name = 'C:\Users\Mitzumi\Documents\Models\Blendswap\cc0_14_building_set\obj\Building_A13.mtl'
if n==4:
    texture_path = 'C:\Users\Mitzumi\Documents\Models\Blendswap\cc0_Robinson_R22_Helicopter_with_Cycles_Materials'
    file_name = 'C:\Users\Mitzumi\Documents\Models\Blendswap\cc0_Robinson_R22_Helicopter_with_Cycles_Materials\cc0_R22_Helicopter_Cycles_Materials.mtl'
if n==5:
    texture_path = '/media/banedesh/Storage/Documents/Models/Skyrim/architecture/skyhaventemple'
    file_name = '/media/banedesh/Storage/Documents/Models/Skyrim/architecture/skyhaventemple/skyhaventempletemplayout01.mtl'

with open(file_name, 'r') as f:
    lines = f.read().splitlines()   # Remove slash n character at the end of each line.
f.close()

# Defaults
material_pending = False
opacity = 1.0
ior = 1.0
reflection_weight = 0.1
reflection_roughness = 0.23
diffuse_color = [0,0,0]
specular_color = [0,0,0]

for line in lines:
    s = line.lstrip()       # Remove leading TAB or spacing if present.
    ary = s.split(' ')      # Split by spaces.
    if ary[0] == 'newmtl':
        if material_pending:
            # This material has no map associated with it, only color. Still needs to be created before we move on.
            shader_name = returnValidHoudiniNodeName("%s" % mat_name)
            createRedshiftImageMapMaterial("/shop", "%s/%s" % (texture_path,"NOT_DETECTED"), shader_name, diffuse_color,specular_color,reflection_weight,ior, opacity)
            # Reset defaults.
            material_pending = False
            opacity = 1.0
            ior = 1.0
            reflection_weight = 0.1
            reflection_roughness = 0.23
            diffuse_color = [0,0,0]
            specular_color = [0,0,0]
            
        mat_name = ary[1]   # Kind of assuming that only one space will be between the token and the value.
        material_pending = True

    if ary[0] == 'Ks':
        specular_color = [ary[1],ary[2],ary[3]]
    if ary[0] == 'Kd':
        diffuse_color = [ary[1],ary[2],ary[3]]
    if ary[0] == 'Ns':
        reflection_weight = float(ary[1])/100
    if ary[0] == 'Ni':
        ior = ary[1]
    if ary[0] == 'd':
        opacity = ary[1]
    if ary[0] == 'map_Kd':
        # Found a diffuse map.
        # Grab the name of this new material and create a Redshift shader network that we can populate.
        shader_name = returnValidHoudiniNodeName("%s" % mat_name)
        if platform.system() == 'Windows':
            createRedshiftImageMapMaterial("/shop", "%s\%s" % (texture_path,ary[1].lower()), shader_name, diffuse_color,specular_color,reflection_weight,ior, opacity)
        else:
            createRedshiftImageMapMaterial("/shop", "%s/%s" % (texture_path,ary[1].lower()), shader_name, diffuse_color,specular_color,reflection_weight,ior, opacity)
        # Reset defaults.
        material_pending = False
        opacity = 1.0
        ior = 1.0
        reflection_weight = 0.1
        reflection_roughness = 0.23
        diffuse_color = [0,0,0]
        specular_color = [0,0,0]
    if ary[0] == 'map_Kn':
        # Found a normal map.
        # Assume there is already a diffuse map present and simply reprogram the bump map node.
        shader_name = returnValidHoudiniNodeName("%s" % mat_name)
        if platform.system() == 'Windows':
            installNormalMap("/shop", "%s\%s" % (texture_path, ary[1].lower()), shader_name)
        else:
            installNormalMap("/shop", "%s/%s" % (texture_path, ary[1].lower()), shader_name)

