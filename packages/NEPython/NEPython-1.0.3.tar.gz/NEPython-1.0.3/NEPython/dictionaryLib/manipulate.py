def merge_dictionary_values(dic1, dic2):
    new_arr = {
        k: dic1.get(k,0) + dic2.get(k,0) \
        for k in set(dic1 | dic2)
    }
    return(new_arr)