# Linear search algorithm

# def linear_search(arr, target):
#     for i in range (0, len(arr)):
#         if arr[i] == target:
#             arr_two = arr_two.append(i)
            
#     return arr_two

# def test(index):
#     if index is not None:
#         print(f"target found at index : {index}")
#     else:
#         print("target not found in list")
# result = (linear_search([1, 2, 3,3, 4, 5], 3)) 
# # print(linear_search([1, 2, 45, 4, 5], 6)) # None 
# test(result)

#Binary searcg algorithm

def binary_search(arr, target):
    index = None
    counter = 0
    first = 0
    last = len(arr)-1 
    while first <= last:
        counter += 1
        mid = (first + last )//2
        if arr[mid]== target:
            index = mid
            break
        elif arr[mid] < target:
            first = mid +1

        elif arr[mid] > target:
            last = mid -1
        else:
            index = None
        
    return ({'index': index, 'counter': counter})


sorted_array = list(range(1, 100000100))

print(binary_search(sorted_array, 1))