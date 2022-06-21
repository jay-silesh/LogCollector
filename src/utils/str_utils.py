def strip_dict(d):
    def strip_list(l):
        return [strip_dict(x)
        if isinstance(x, dict)
        else strip_list(x)
        if isinstance(x, list)
        else clean(value)
        for x in l]

    def clean(string):
        return ''.join(string.split())

    return { key.strip() : strip_dict(value)
             if isinstance(value, dict)
             else strip_list(value)
             if isinstance(value, list)
             else value
             if isinstance(value, bool)
             else clean(value)
             for key, value in d.items() }
