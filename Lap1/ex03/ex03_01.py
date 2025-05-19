def tinh_tong_so_chan(lst):
    tong = 0
    for num in lst:
        if num % 2 == 0:
            tong += num
    return tong

# Nhập danh sách từ người dùng
input_list = input("Nhập danh sách các số, cách nhau bằng dấu cách: ")
numbers = list(map(int, input_list.split()))

# Tính tổng các số chẵn
tong_chan = tinh_tong_so_chan(numbers)

# In kết quả
print("Tổng các số chẵn trong List là:", tong_chan)