
def map_dict_keys(init_dict, map_dict):
    res_dict = {}
    for k, v in init_dict.items():
        if isinstance(v, dict):
            v = map_dict_keys(v, map_dict[k])
        elif k in map_dict.keys():
            k = str(map_dict[k])
        res_dict[k] = v
    return res_dict

def remove_dict_elements(dictioary,wanted_keys):
    temp_dict=dictioary
    unwanted_keys = set(dictioary) - set(wanted_keys)
    for unwanted_key in unwanted_keys: del temp_dict[unwanted_key]
    return temp_dict