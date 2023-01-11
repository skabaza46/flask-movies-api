

def clean(name):
    """Clean the movie field names enable to create dynamic dictionary of statistics."""
    name = name.replace("&", "and")
    name =  name.lstrip().lower().replace(" ", "_")
    name =  name.lstrip().lower().replace("-", "_")
 
    return name