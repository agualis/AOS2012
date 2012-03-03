def is_in_list(element, list):
    try:
        list.index(element)
        return True
    except: 
        return False