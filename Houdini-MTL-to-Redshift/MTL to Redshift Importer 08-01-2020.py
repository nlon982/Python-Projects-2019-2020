# newmtl (material name). string. called mat_name
# Ns (specular intensity). float. called reflection_weight
# Ka (ambient color). NOT USED
# Kd (diffuse color). 3 big list. called same
# Ks (specular color). 3 big list. called same
# Ni (index of refraction). float. called ior
# d (opacity). float. called same.
# illum (illumination model, we're assuming 2). NOT USED
# map_Kd (filepath to diffuse map)
# map_Kn (filepath to normal map)

import re, os

class Material:
    def __init__(self, material_name, mtl_file_path): # The main idea here is to reflect what the MTL is showing (material_name is a prime example). However, I am planning on doing defaults here.. alternative is to make a huge if/elif function which handles this default thing
        self.material_name = material_name # each thing here corresponds to the allowed_token_names, so in theory:  change that, and adjust this, and update create_in_houdini() and you can add things
        self.texture_path = mtl_file_path[:mtl_file_path.rfind("\\") + 1]
        self.ns = None
        self.ka = None # NOT USED 
        self.kd = None 
        self.ks = None
        self.ni = None
        self.d = None
        self.illum = None # NOT USED (this is hard coded for 2)
        self.map_kd = None
        self.map_kn = None

    def defaults(self):
        if self.ns == None:
            self.ns = 0
        if self.ka == None:
            self.ka = 0
        if self.kd == None:
            self.kd = 0
        if self.ks == None:
            self.ks = 0
        if self.ni == None:
            self.ni = 0
        if self.d == None:
            self.d = 0
        if self.illum == None:
            self.illum = 0

    def create_in_houdini(self):
        valid_material_name = get_valid_houdini_node_name(self.material_name)
        a_material_node = hou.node("/shop").createNode("redshift_vopnet", valid_material_name) # called rs_vop
        a_material_node.allowEditingOfContents()
        redshift_material_node = hou.node(a_material_node.path() + "/" + "redshift_material1") # called rs_output. ALSO: don't know if a_material_node.path() will work like I expect
        shader_node = a_material_node.createNode("redshift::Material", "Shader") # called rs_mat
        redshift_material_node.setInput(0, shader_node, 0) # not sure what this does, or why. * EDIT: he does the exact thing as well later on

        # re: below. Houdini doesn't seem to mind floats/ints being passed as strings, it interprets/converts them accordingly.
        shader_node.parm("refl_weight").set(self.ns[0]) ####################### TODO: I need to add defaults in material init. Perhaps no defaults are good? i.e. depends on the norm of mtl files - which idk.
        # ambient color i.e. Ka is not used #
        shader_node.parm("diffuse_colorr").set(self.kd[0])
        shader_node.parm("diffuse_colorg").set(self.kd[1])
        shader_node.parm("diffuse_colorb").set(self.kd[2])
        shader_node.parm("refl_colorr").set(self.ks[0])
        shader_node.parm("refl_colorg").set(self.ks[1])
        shader_node.parm("refl_colorb").set(self.ks[2])
        #shader_node.parm("refl_ior").set(self.ni[0])
        shader_node.parm("opacity_colorr").set(self.d[0]) # i.e. mtl gives opacity for rgb as one value
        shader_node.parm("opacity_colorg").set(self.d[0])
        shader_node.parm("opacity_colorb").set(self.d[0])
        # the following isn't in MTL, and is hard coded to "soft blur reflection"
        shader_node.parm("refl_roughness").set(0.23)
        
        
        texture_sampler_diffuse_node = a_material_node.createNode("redshift::TextureSampler", "diffuse") # haven't cared to give a name
        if self.map_kd[0] != None:
            map_kd_path = self.texture_path + self.map_kd[0]
            print(map_kd_path)
            texture_sampler_diffuse_node.parm("tex0").set(map_kd_path)
            
            shader_node.setInput(0, texture_sampler_diffuse_node)
            
            extension = os.path.splitext(self.map_kd[0])[1]
            files_with_alphas = [".png",".PNG",".tga",".TGA",".tif",".TIF",".tiff",".TIFF",".exr",".EXR"]
            if extension in files_with_alphas:
                sprite_node = a_material_node.createNode("redshift::Sprite") # haven't cared to give a name
                sprite_node.parm("tex0").set(map_kd_path)
                sprite_node.parm("mode").set("1")
                sprite_node.setInput(0, shader_node)
                redshift_material_node.setInput(0, sprite_node)
                #shader_node.setInput(46, texture_sampler_diffuse_node) # input #46 is opacity color (i.e. alpha)

        # remove luminosity from texture using a color corrector
        color_correction_node = a_material_node.createNode("redshift::RSColorCorrection")
        color_correction_node.setInput(0, texture_sampler_diffuse_node)

        color_correction_node.parm("saturation").set(0)
        # add a slight bump using greyscale value of diffuse texture
        
        bump_map_node = a_material_node.createNode("redshift::BumpMap")
        bump_map_node.setInput(0, color_correction_node)
        bump_map_node.parm("scale").set(0.25) # Hard coded
        redshift_material_node.setInput(2, bump_map_node)

        if self.map_kn[0] != None:
            map_kn_path = self.texture_path + self.map_kn[0]
            # assuming map_kd exists (that's what he does), he does error protection too
            texture_sampler_normal_node = a_material_node.createNode("redshift::TextureSampler")
            bump_map_node.setInput(0, texture_sampler_normal_node)
            bump_map_node.parm("scale").set(1.0)
            bump_map_node.parm("inputType").set("1")
            texture_sampler_normal_node.parm("tex0").set(map_kn_path)
            texture_sampler_normal_node.parm("tex0_gammaoverride").set(1)

        # Layout
        a_material_node.moveToGoodPosition()
        texture_sampler_diffuse_node.moveToGoodPosition()
        color_correction_node.moveToGoodPosition()
        bump_map_node.moveToGoodPosition()
        shader_node.moveToGoodPosition()
        redshift_material_node.moveToGoodPosition()
        

def mtl_file_parser(mtl_file_path):
    mtl_file = open(mtl_file_path, 'r')
    a_str = mtl_file.read()
    lines = a_str.split("\n")

    for line in lines:
        clean_line = line.lstrip() # get rid of spaces at front
        line_list = clean_line.split(" ") # get line in terms of items seperated by space
        allowed_token_names = ["Ns", "Ka", "Kd", "Ks", "Ni", "d", "illum", "map_Kd", "map_Kn"]
        
        if line_list[0] == "newmtl":          
            material_object = Material(line_list[1], mtl_file_path)
        elif line_list[0] == "" or line_list[0] == "#": # i.e. as soon as there is an empty line, this marks end of material entry in mtl: so create that material in houdini
            try:
                material_object
            except NameError: # i.e. material object does not exist
                pass
            else: # material object does exist
                #print("hi")
                material_object.create_in_houdini()
        elif line_list[0] in allowed_token_names:
            token_parser(line_list, material_object)
        else:
            print("{} is not in allowed token names list: {}".format(line_list[0], allowed_token_names))

def token_parser(line_list, material_object):
    token_name = line_list[0]
    token_info = line_list[1:]
    # hard coded things that he did
    if token_name == "Ns": 
        token_info[0] = str(float(token_info[0]) / 100) # i.e. 100 turns to 1
    # end
    exec_me = "material_object." + token_name.lower() + " = " + str(token_info)
    exec(exec_me)

def get_valid_houdini_node_name(name):
    return re.sub("[^0-9a-zA-Z\.]+", "_", name)


#### CHANGE ME
mtl_file_parser(r"C:\Users\Nathan Longhurst\Documents\Houdini Projects\Kyle Importer Project\Material Downaloads\another 3dsky\Plum Julia Grup 23579.mtl")
# I have coded this hap-hazardly (currently), so that the textures need to be in same folder as your mtl.
