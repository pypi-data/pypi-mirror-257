def remove_array_duplicates(arr):
    return list(dict.fromkeys(arr).keys())

def switch_array_items(arr, a, b):
    index1 = arr.index(a)
    index2 = arr.index(b)
    arr[index1], arr[index2] = arr[index2], arr[index1]

def get_most_common_item(arr):
    return max(set(arr), key=arr.count)

def remove_first_occurrence_left(arr1, x):
    arr2 = []
    for i in arr1:
        arr2.append(i.removeprefix(x))
    return arr2

def remove_first_occurrence_right(arr1, x):
    arr2 = []
    for i in arr1:
        arr2.append(i[::-1].removesuffix(x[::-1])[::-1])
    return arr2

def rotate_list(arr, k):
    k = k % len(arr)
    return arr[-k:] + arr[:-k]

def find_consecutive_sublists_num(arr):
    result = []
    temp = []

    for i in arr:
        if not temp or (isinstance(i, (int, float)) and temp[-1] == i - 1):
            temp.append(i)
        elif temp:
            result.append(temp)
            temp = []

    if temp:
        result.append(temp)

    return result

def seperate_string_num(arr):
    result = []
    temp = [arr[0]]
    for i in range(1, len(arr)):
        try:
            if arr[i] == arr[i - 1] + 1:
                temp.append(arr[i])
            else:
                result.append(temp)
                temp = [arr[i]]
        except TypeError:
            result.append(temp)
            temp = [arr[i]]
    result.append(temp)
    return result