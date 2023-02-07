

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

    # If we have and odd amount of elements, include the median.
    if len(data) % 2 == 1:
        n+=1
    return median(data[:n])

def Q3(data: list):
    assert len(data) > 0, "List is empty"
    data = sorted(data)
    # Let the length of the data be 2n or 2n+1
    # Q3 = median of the n largest values.
    n = len(data) // 2

    # If we have and odd amount of elements, include the median.
    if len(data) % 2 == 1:
        n-=1
    return median(data[n:])
    
# Robust estimates of scale
def median_absolute_deviation(data: list):
    median_data = median(data)
    residuals_from_median = [abs(x_i - median_data) for x_i in data]
    return median(residuals_from_median)

def interquartile_range(data: list):
    return Q3(data) - Q1(data)

def S(data: list):
    """
    For each i we compute the median of |x_i - x_j|,
    where j = 1...n = len(data).
    This yields n numbers, of which we compute the median.
    """
    pairwise_medians = []
    for i in range(len(data)):
        abs_diff_from_i = []
        for j in range(len(data)):
            abs_diff_from_i.append(abs(data[i] - data[j]))
        pairwise_medians.append(median(abs_diff_from_i))
    return 1.1926 * median(pairwise_medians)

def Q(data: list):
    """
    First quartile of pairwise differences
    """
    abs_diff_from_i = []
    for i in range(len(data)):
        for j in range(i, len(data)):
            abs_diff_from_i.append(abs(data[i] - data[j]))
    return 2.2219 * Q1(abs_diff_from_i)


def is_outlier(data: list, data_point):
    """
    Using the MAD, check is data_point is an outlier
    """
    mad = median_absolute_deviation(data)
    med = median(data)
    threshold = 2.5
    criteria = abs(data_point - med) / mad
    return criteria > threshold