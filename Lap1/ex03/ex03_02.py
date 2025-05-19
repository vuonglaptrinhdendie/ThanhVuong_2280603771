def dao_nguoc_list(lst):
    return lst[::-1]

# Nhập danh sách từ người dùng với các ký tự cách nhau bằng dấu phẩy
input_list = input("Nhập danh sách các số, các số cách nhau bằng dấu cách: ")
numbers = list(map(int, input_list.split(',')))

# Sử dụng hàm đảo ngược
list_dao_nguoc = dao_nguoc_list(numbers)
print("List sau khi đảo ngược: ", list_dao_nguoc)