# Univariate
def median(data: list):
    assert len(data) > 0, "List is empty"
    if len(data) == 1:
        return data[0]
    
    data = sorted(data)
    mid_index = len(data) // 2
    if len(data) % 2 == 1:
        return data[mid_index]
    else:
        return 0.5 * (data[mid_index - 1] + data[mid_index]) 
    