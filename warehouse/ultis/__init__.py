def update_attr(obj, data):
    for key, value in data.items():
        setattr(obj, key, value)
