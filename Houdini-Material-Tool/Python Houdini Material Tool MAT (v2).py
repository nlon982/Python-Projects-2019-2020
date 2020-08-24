import os

print("----------------------------------------------------")
# inside pack location is materials
# inside pack location and materials is maps


#cTextureSampler i0 eShader ndiffuse_color

#[cTextureSampler i0 *cNull i0 ] [eNullDIFF i0 cShaderswitch i1] [eTextureSamplerDIFF i0 cTriPlanar i0] [eTriPlanarDIFF i0 eShaderswitchDIFF i2] [eShaderswitchDIFF i0 * eShader ndiffuse_color] NEW:[eParm i0 eShaderswitchDIFF i0] 

#parm is called "parameter"
#null is called "null"


#triplanar is called "redshift::TriPlanar"
#shaderswitch is called "redshift::RSShaderSwitch"

"cNull i0 eNullDIFF i0 credshift::RSShaderSwitch i1 eTextureSamplerDIFF i0 credshift::TriPlanar i0 eTriPlanarDIFF i0 eRSShaderSwitchDIFF i2 eRSShaderSwitchDIFF i0"

#credshift::RSShaderSwitch!tex0:penis i1 eTextureSamplerDIFF i0


def parameter_processor(params, node, a_material_node):
    while "!" in params:
        #print(params)
        param_name = params[1:params.find(":")] # we know the first digit is going to be !
        end = params[1:].find("!") + 1
        if end == 0:
            end = len(params)
        param_content = params[params.find(":") + 1: end]
        set_parms(node, param_name, param_content, a_material_node)
        params = params[end:]

def parameter_temp_processor(entry):
    if "!" in entry:
        entry_without_param = entry[:entry.find("!")]
        params = entry[entry.find("!"):]
        return entry_without_param, params
    return entry, None

def set_parms(node, param_name, param_content, a_material_node):
    print(param_name, param_content)
    if "^" in param_name and "^" in param_content:
        parmsinfolder_from_node = node.parmTuplesInFolder((param_name[1:],))
        parmsinfolder_from_material = a_material_node.parmTuplesInFolder((param_content[1:],))
        if len(parmsinfolder_from_node) == len(parmsinfolder_from_material):
            for i in range(len(parmsinfolder_from_node)):
                print("{} set {}".format(parmsinfolder_from_node[i], parmsinfolder_from_material[i]))
                parmsinfolder_from_node[i].set(parmsinfolder_from_material[i])
        return
    if "*" in param_name and "*" in param_content:
        parmsinfolder_from_node = node.parmTuples()
        parmsinfolder_from_material = a_material_node.parmTuplesInFolder((param_content[1:],))
        if len(parmsinfolder_from_node) == len(parmsinfolder_from_material):
            for i in range(len(parmsinfolder_from_node)):
                print("{} set {}".format(parmsinfolder_from_node[i], parmsinfolder_from_material[i]))
                parmsinfolder_from_node[i].set(parmsinfolder_from_material[i])
        return    
    if param_content[0:3] == "int":
        print(param_content)
        param_content = int(param_content[3:])
        print(param_content)
    elif param_content[0:3] == "str":
        print(param_content)
        param_content = param_content[3:] #already string
        print(param_content)
    print(param_name, param_content)
    node.setParms({param_name: param_content})
    #print("do the following on this node: {} . param_name : {} . param_content : {}".format(node.path(), param_name, param_content))

def get_name(entry, map_name):
    if ":" in entry:
        entry = entry[entry.rfind(":") + 1:] + map_name
    else:
        entry = entry + map_name
    return entry

def update_21_aug(map_and_type_node_setup_dict):
    for key in map_and_type_node_setup_dict.keys():
        name = key.split()[0]
        contents = map_and_type_node_setup_dict[key]
        contents_list = contents.split()
        branchnode = contents_list[:-2][-2][1:]
        if "*" in branchnode:
            branchnode = branchnode[:branchnode.find("*")]
        contents_list[:-2][-2] = contents_list[:-2][-2].replace("*", "") # the reason this doesn't work is because it's editing a new list, not the og, I can't remember if it has some other functionality though
        ## lazy:
        for index in range(len(contents_list)):
            if "*" in contents_list[index]:
                contents_list[index] = contents_list[index].replace("*", "")
        ### lazy end
        middle_new =  " cnull i0 enull{} i0 credshift::RSShaderSwitch!*blah:*ShaderSwitch_settings i1 e{}{} i0 credshift::TriPlanar!^Coordinates:^Triplanar_settings!^Texture:^Triplanar_settings2 i0 eTriPlanar{} i0 eRSShaderSwitch{} i2 eRSShaderSwitch{} i0 ".format(name, branchnode, name, name, name, name)
        end_new = ""
        #end_new = " eParm i0 eRSShaderSwitch{} i0".format(name)
        contents_new = " ".join(contents_list[:-2]) + middle_new + " ".join(contents_list[-2:len(contents_list)]) + end_new
        map_and_type_node_setup_dict[key] = contents_new
    return map_and_type_node_setup_dict
        
        



def get_pretty_material_name(material_name, cutoff_start, cutoff_end):
    pretty_material_name = material_name[0 + cutoff_start: len(material_name) - cutoff_end]
    return pretty_material_name

def get_material_scan(pack_location):
    dir_scan_list = list()
    scan_list = os.listdir(pack_location)
    for material_name in scan_list:
        a_path = pack_location + "\\" + material_name
        if os.path.isdir(a_path) == True:
            dir_scan_list.append(material_name)
    return dir_scan_list

def get_map_scan(pack_location, material_name):
    scan_list = os.listdir(pack_location + "\\" + material_name)
    return scan_list

def get_existing_maps(map_scan, map_name): # what items in the directory exist with that map_name
    existing_maps = list()
    for item in map_scan:
        if map_name in item:
                existing_maps.append(item)
    return existing_maps

def get_chosen_map_file(existing_maps, type_list):
    type_list.reverse()
    for file_type in type_list:
        for item in existing_maps:
            if file_type in item:
                chosen_map_file = item
                break
    return chosen_map_file

def node_setup_function(entry_1, entry_2, entry_3, entry_4, connection_pass_number, map_pass_number, pretty_material_name, chosen_map_file_path, housing_path, map_name):
    shader_node, a_material_node, a_material_path = material_initialization(pretty_material_name, housing_path, map_pass_number)
    entry_1, params_entry_1 = parameter_temp_processor(entry_1)
    entry_3, params_entry_3 = parameter_temp_processor(entry_3)
    #print("***********node_setup_function started")
    #print("command sent: {} {} {} {}".format(entry_1, entry_2, entry_3, entry_4))
    #print("current children:")
    #for child in a_material_node.children():
    #    print(child.name())
    #print()
    if entry_1[0] == "c":
        entry_1_name = get_name(entry_1[1:], map_name)
        #print("the entry_1_name is {}".format(entry_1_name))
        output_node = a_material_node.createNode(entry_1[1:], entry_1_name)
        #print("output node created called: {}".format(output_node.name()))
    elif entry_1[0] == "e":
        output_node = hou.node(a_material_path + "/" + entry_1[1:])
        #print("output node exists called: {}".format(output_node.name()))
    else:
        print("BAD INPUT e1")
    
    if entry_2[0] == "i":
        output_connector = entry_2[1:]
    elif entry_2[0] == "n":
        output_connector = entry_2[1:]
        output_connector = output_node.outputIndex(output_connector)
    else:
        print("BAD INPUT e2")            
    
    if entry_3[0] == "c":
        entry_3_name = get_name(entry_3[1:], map_name)
        #print("the entry_3_name is {}".format(entry_3_name))
        input_node = a_material_node.createNode(entry_3[1:], entry_3_name)
        #print("input node created called: {}".format(input_node.name()))
    elif entry_3[0] == "e":
        input_node = hou.node(a_material_path + "/" + entry_3[1:])
        #print("input node exists called: {}".format(input_node.name()))
    else:
        print("BAD INPUT e3")
    
    if entry_4[0] == "i":
        input_connector = entry_4[1:]
    elif entry_4[0] == "n":
        input_connector = entry_4[1:]
        input_connector = input_node.inputIndex(input_connector)
    else:
        print("BAD INPUT e4")

    if params_entry_1 is not None:
        parameter_processor(params_entry_1, output_node, a_material_node)
    if params_entry_3 is not None:
        parameter_processor(params_entry_3, input_node, a_material_node)

    #print("about to connect {} {} {} {}".format(output_node.type(), output_connector, input_node.type(), input_connector))
    input_node.setInput(int(input_connector), output_node, int(output_connector))
    if connection_pass_number == 1:
        output_node.setParms({"tex0": chosen_map_file_path})
    
    if "METAL" in chosen_map_file_path and connection_pass_number == 1: # cheating
        shader_node.setParms({"refl_fresnel_mode": "2"})
    
    a_material_node.layoutChildren()

def material_initialization(pretty_material_name, housing_path, map_pass_number):
    a_material_path = housing_path + "/" + pretty_material_name
    a_material_node = hou.node(a_material_path)
    if a_material_node is None:
        a_material_node = hou.node(housing_path).createNode("redshift_vopnet", pretty_material_name)
        a_material_node.allowEditingOfContents()
    redshift_material_node = hou.node(housing_path + "/" + pretty_material_name + "/" + "redshift_material1")
    shader_node = hou.node(housing_path + "/" + pretty_material_name + "/" + "Shader")
    if shader_node is None:
        shader_node = a_material_node.createNode("redshift::Material", "Shader")
        redshift_material_node.setInput(0, shader_node, 0)
    #parm_node = hou.node(housing_path + "/" + pretty_material_name + "/" + "Parm")
    #if parm_node is None:
    #    parm_node = a_material_node.createNode("parameter", "Parm") #add parm name
    try:
        a_material_node.parmTuplesInFolder(("Triplanar_settings",))
    except:
        triplanar_node = a_material_node.createNode("redshift::TriPlanar", "dummy")
        folder_of_parms = triplanar_node.parmTuplesInFolder(("Coordinates",))
        template_group = a_material_node.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("foldername", "Triplanar_settings")
        parm_folder.setFolderType(hou.folderType.Simple)
        for item in folder_of_parms:
            instance_parm_template = item.parmTemplate()
            parm_folder.addParmTemplate(instance_parm_template)
        template_group.append(parm_folder)
        a_material_node.setParmTemplateGroup(template_group)
        triplanar_node.destroy()
    try:
        a_material_node.parmTuplesInFolder(("Triplanar_settings2",))
    except:
        triplanar_node = a_material_node.createNode("redshift::TriPlanar", "dummy")
        folder_of_parms = triplanar_node.parmTuplesInFolder(("Texture",))
        template_group = a_material_node.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("foldername", "Triplanar_settings2")
        parm_folder.setFolderType(hou.folderType.Simple)
        for item in folder_of_parms:
            instance_parm_template = item.parmTemplate()
            parm_folder.addParmTemplate(instance_parm_template)
        template_group.append(parm_folder)
        a_material_node.setParmTemplateGroup(template_group) 
        triplanar_node.destroy()
    try:
        a_material_node.parmTuplesInFolder(("ShaderSwitch_settings",))
    except:
        triplanar_node = a_material_node.createNode("redshift::RSShaderSwitch", "dummy")
        folder_of_parms = triplanar_node.parmTuples()
        template_group = a_material_node.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("foldername", "ShaderSwitch_settings")
        parm_folder.setFolderType(hou.folderType.Simple)
        for item in folder_of_parms:
            instance_parm_template = item.parmTemplate()
            parm_folder.addParmTemplate(instance_parm_template)
        template_group.append(parm_folder)
        a_material_node.setParmTemplateGroup(template_group)
        triplanar_node.destroy()
    return shader_node, a_material_node, a_material_path
    
def main():
    housing_path = "/mat"
    #pack_location = r"C:\Users\Nathan Longhurst\Desktop\GSG_EMC_Redshift"
    pack_location = r"D:\Blender\Textures Assets\Material Assets\PBR Textures\GSG_EMC_Redshift"
    cutoff_start = 2 
    cutoff_end = 0

    material_scan = get_material_scan(pack_location)
    map_and_type_node_setup_dict = {"DIFF .png .jpg" : "cTextureSampler i0 eShader ndiffuse_color", "ROUGH .jpg" : "cTextureSampler i0 eShader nrefl_roughness", "METAL .jpg" : "cTextureSampler i0 eShader nrefl_metalness", "HEIGHT .exr .jpg" : "cTextureSampler i0 cDisplacement i0 eDisplacement*HEIGHT i0 eredshift_material1 i1", "NORM .jpg" : "cNormalMap i0 eShader nbump_input"}
    map_and_type_node_setup_dict = update_21_aug(map_and_type_node_setup_dict)
    for material_name in material_scan:
        map_pass_number = 0
        for map_and_type, node_setup in map_and_type_node_setup_dict.items():
            map_pass_number += 1    
        
            node_setup = node_setup.split(" ")
                                    
            map_and_type_list = map_and_type.split(" ")
            map_name = map_and_type_list[0]
            type_list = map_and_type_list[1:]


            map_scan = get_map_scan(pack_location, material_name)
            existing_maps = get_existing_maps(map_scan, map_name)

            if len(existing_maps) < 1:
                continue
            
            chosen_map_file = get_chosen_map_file(existing_maps, type_list)
            chosen_map_file_path = pack_location + "\\" + material_name + "\\" + chosen_map_file
            

            if len(node_setup) % 4 == 0:
                connection_pass_number = 0
                while len(node_setup) > 0:
                    connection_pass_number += 1
                    entry_4 = node_setup.pop(3)
                    entry_3 = node_setup.pop(2)
                    entry_2 = node_setup.pop(1)
                    entry_1 = node_setup.pop(0)
                    pretty_material_name = get_pretty_material_name(material_name, cutoff_start, cutoff_end)
                    node_setup_function(entry_1, entry_2, entry_3, entry_4, connection_pass_number, map_pass_number, pretty_material_name, chosen_map_file_path, housing_path, map_name)
        hou.node(housing_path).layoutChildren()

main()
