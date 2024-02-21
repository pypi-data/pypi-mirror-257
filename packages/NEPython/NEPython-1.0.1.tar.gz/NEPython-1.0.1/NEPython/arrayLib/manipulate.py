def merge_dictionary(dic1, dic2):
    new_arr = {
        k: dic1.get(k,0) + dic2.get(k,0) \
        for k in set(dic1 | dic2)
    }
    return(new_arr)

def merge_arrays(arr1, arr2):
    arr1 + arr2
    return sorted(set(arr1))