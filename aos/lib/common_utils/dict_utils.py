def merge_dicts(dict1,dict2):
    dict3 = dict(dict1)
    for key, value in dict2.items():
        if dict3.has_key(key):
            dict3[key] = dict3[key] + value
        else:
            dict3[key] = value
    return dict3