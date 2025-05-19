def tao_tuple_tu_list(lst):
    return tuple(lst)

# Nhập danh sách từ người dùng với các ký tự cách nhau bằng dấu phẩy
input_list = input("Nhập danh sách các số, các số cách nhau bằng dấu cách: ")
numbers = list(map(int, input_list.split(',')))

my_tuple = tao_tuple_tu_list(numbers)
print("List: ", numbers)
print("Tuple từ List: ", my_tuple)