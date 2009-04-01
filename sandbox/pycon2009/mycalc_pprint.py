
def pp(st):
    data, children = st
    if isinstance(data, str):
        return data.join([pp(child) for child in children ])
    else: return str(data)
    
        
    
