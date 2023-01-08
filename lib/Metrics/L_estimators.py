
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

def Q1(data: list):
    assert len(data) > 0, "List is empty"
    data = sorted(data)
    # Let the length of the data be 2n or 2n+1
    # Q1 = median of the n smallest values.
    n = len(data) // 2
    return median(data[:n])

def Q3(data: list):
    assert len(data) > 0, "List is empty"
    data = sorted(data)
    # Let the length of the data be 2n or 2n+1
    # Q1 = median of the n largest values.
    n = len(data) // 2
    return median(data[n:])
    
def median_absolute_deviation(data: list):
    median_data = median(data)
    residuals_from_median = [abs(x_i - median_data) for x_i in data]
    return median(residuals_from_median)

def interquartile_range(data: list):
    return Q3(data) - Q1(data)