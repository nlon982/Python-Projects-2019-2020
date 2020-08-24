import os

# inside pack location is materials
# inside pack location and materials is maps

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

def node_setup_function(entry_1, entry_2, entry_3, entry_4, connection_pass_number, map_pass_number, pretty_material_name, chosen_map_file_path, housing_path):
    shader_node, a_material_node, a_material_path = material_initialization(pretty_material_name, housing_path, map_pass_number)
    if entry_1[0] == "c":
        print("a")
        output_node = a_material_node.createNode(entry_1[1:])
        print("b")
    elif entry_1[0] == "e":
        output_node = hou.node(a_material_path + "/" + entry_1[1:])
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
        print("a")
        input_node = a_material_node.createNode(entry_3[1:])
        print("b")
    elif entry_3[0] == "e":
        input_node = hou.node(a_material_path + "/" + entry_3[1:])
    else:
        print("BAD INPUT e3")
    
    if entry_4[0] == "i":
        input_connector = entry_4[1:]
    elif entry_4[0] == "n":
        input_connector = entry_4[1:]
        input_connector = input_node.inputIndex(input_connector)
    else:
        print("BAD INPUT e4")
    
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
    return shader_node, a_material_node, a_material_path
    
def main():
    housing_path = "/mat"
    #pack_location = r"C:\Users\Nathan Longhurst\Desktop\GSG_EMC_Redshift"
    pack_location = r"D:\Blender\Textures Assets\Material Assets\PBR Textures\GSG_EMC_Redshift"
    cutoff_start = 2 
    cutoff_end = 0

    material_scan = get_material_scan(pack_location)
    map_and_type_node_setup_dict = {"DIFF .png .jpg" : "cTextureSampler i0 eShader ndiffuse_color", "ROUGH .jpg" : "cTextureSampler i0 eShader nrefl_roughness", "METAL .jpg" : "cTextureSampler i0 eShader nrefl_metalness", "HEIGHT .exr .jpg" : "cTextureSampler i0 cDisplacement i0 eDisplacement1 i0 eredshift_material1 i1", "NORM .jpg" : "cNormalMap i0 eShader nbump_input"}
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
                    node_setup_function(entry_1, entry_2, entry_3, entry_4, connection_pass_number, map_pass_number, pretty_material_name, chosen_map_file_path, housing_path)
        hou.node(housing_path).layoutChildren()

main()
