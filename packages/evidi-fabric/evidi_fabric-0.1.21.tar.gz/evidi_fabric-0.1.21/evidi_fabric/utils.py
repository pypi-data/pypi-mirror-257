from evidi_fabric.sql import add_default_where_clause

def extend_list_in_dict(dct, key, value:list) -> dict:
    """
    Extending list element of a dictionary. 
    If key does not exists, then it is created.
    """
    if key in dct.keys():
        dct[key].extend(value)
    else:
        dct[key]=value
    return dct


def merge_configs(base:dict, custom:dict) -> dict:
    """
    Find matching keys from two dictionaries and append the lists together if value is list.
    """
    result = base.copy()
    for key, value in custom.items():
        if isinstance(value, dict) and key in base:
            result[key] = merge_configs(base[key], value)
        elif isinstance(value, list):
            # Append additional columns to the existing 'columns' list
            result[key] = base.get(key, []) + value
        else:
            result[key] = value
    return result


def get_config(config_base, config_custom) -> dict:
    """
    Retrieves and merge the config_base and config_custom config files to a single config dictionary. 
    """
    config_raw = merge_configs(config_base, config_custom)
    try:
        config = add_default_where_clause(config_raw)
    except:
        #Could not add default where clause
        config = config_raw
        pass

    return config