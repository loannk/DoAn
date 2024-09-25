import tkinter as tk
from tkinter import messagebox
from model import MTT, baodong, LoigiaiToiUu
import logging

# Đường dẫn tới file Excel đã được chọn sẵn
file_path = 'Rules.xlsx'  # Đặt đường dẫn tới file Excel của bạn ở đây

def MangTinhToan():
    try:
        # Lấy dữ liệu đầu vào từ người dùng
        A = set(entry_A.get().upper().split(','))
        B = set(entry_B.get().upper().split(','))
        chuoi = entry_chuoi.get().upper().split(',')

        # Gọi hàm xử lý dữ liệu từ model.py
        main_reactions, chain_reactions = MTT(file_path, A, B, chuoi)

        # Hiển thị kết quả
        result_text1.delete(1.0, tk.END)  # Clear previous results
        if main_reactions:
            result_text1.insert(tk.END, "\nCác phản ứng có thể xảy ra:\n")
            for reaction in main_reactions:
                result_text1.insert(tk.END, f" {reaction[0]}: {' + '.join(reaction[1])} -> {' + '.join(reaction[2])}\n")
        else:
            if chain_reactions:
                result_text1.insert(tk.END, "\nCác phản ứng có thể xảy ra trong chuỗi:\n")
                for reaction in chain_reactions:
                    result_text1.insert(tk.END, f" {reaction[0]}: {' + '.join(reaction[1])} -> {' + '.join(reaction[2])}\n")
            else:
                result_text1.insert(tk.END, "Kết quả: Không tìm thấy phản ứng phù hợp.\n")
    except Exception as e:
        logging.error(f"Error in MangTinhToan: {e}")
        messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")

def ToiUu():
    try:
        # Lấy dữ liệu đầu vào từ người dùng
        D = set(entry_D.get().upper().split(','))
        E = set(entry_E.get().upper().split(','))

        # Gọi hàm xử lý dữ liệu từ model.py
        found, solution = LoigiaiToiUu(file_path, D, E)

        # Hiển thị kết quả
        result_text3.delete(1.0, tk.END)  # Clear previous results
        if found:
            result_text3.insert(tk.END, "\nCác phản ứng có thể xảy ra:\n")
            for reaction in solution:
                result_text3.insert(tk.END, f" {reaction[0]}: {' + '.join(reaction[1])} -> {' + '.join(reaction[2])}\n")
        else:
            result_text3.insert(tk.END, "Kết quả: Không tìm thấy phản ứng phù hợp.\n")
    except Exception as e:
        logging.error(f"Error in ToiUu: {e}")
        messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")

def Closure():
    try:
        # Lấy dữ liệu đầu vào từ người dùng
        C = set(entry_C.get().upper().split(','))

        # Gọi hàm xử lý dữ liệu từ model.py
        closure, closure_reactions = baodong(file_path, C)

        # Hiển thị kết quả
        result_text2.delete(1.0, tk.END)  # Clear previous results
        if closure and closure_reactions:
            result_text2.insert(tk.END, "\nBao đóng của chất trên là:\n")
            result_text2.insert(tk.END, f"{closure}\n")

            result_text2.insert(tk.END, "\nPhương trình của các bao đóng trên là:\n")
            for reaction in closure_reactions:
                result_text2.insert(tk.END, f" {reaction[0]}: {' + '.join(reaction[1])} -> {' + '.join(reaction[2])}\n")
        else:
            result_text2.insert(tk.END, "Kết quả: Không tìm thấy kết quả.\n")
    except Exception as e:
        logging.error(f"Error in Closure: {e}")
        messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")

def hide_all_frames():
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()

# Hàm đổi màu nền của các nút khi một mục được chọn
def update_button_bg(selected_button):
    for button in buttons:
        button.config(bg="SystemButtonFace")
    selected_button.config(bg="lightblue")

# Hàm xử lý khi chọn mục 1
def show_frame1():
    hide_all_frames()
    frame1.pack(padx=10, pady=10)
    update_button_bg(button1)

# Hàm xử lý khi chọn mục 2
def show_frame2():
    hide_all_frames()
    frame2.pack(padx=10, pady=10)
    update_button_bg(button2)

# Hàm xử lý khi chọn mục 3
def show_frame3():
    hide_all_frames()
    frame3.pack(padx=10, pady=10)
    update_button_bg(button3)

def clear_frame1():
    entry_A.delete(0, tk.END)
    entry_B.delete(0, tk.END)
    entry_chuoi.delete(0, tk.END)
    result_text1.delete(1.0, tk.END)

def clear_frame2():
    entry_C.delete(0, tk.END)
    result_text2.delete(1.0, tk.END)

def clear_frame3():
    entry_D.delete(0, tk.END)
    entry_E.delete(0, tk.END)
    result_text3.delete(1.0, tk.END)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Form Mạng tính toán")

# Tạo thanh công cụ nằm ngang
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

# Tạo các nút trong thanh công cụ
button1 = tk.Button(toolbar, text="A->B", command=show_frame1)
button1.pack(side=tk.LEFT, padx=2, pady=2)
button2 = tk.Button(toolbar, text="Bao đóng", command=show_frame2)
button2.pack(side=tk.LEFT, padx=2, pady=2)
button3 = tk.Button(toolbar, text="Tối ưu", command=show_frame3)
button3.pack(side=tk.LEFT, padx=2, pady=2)

# Lưu các nút vào một danh sách để tiện cập nhật màu nền
buttons = [button1, button2, button3]

# Tạo frame chính
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Tạo frame cho mục 1
frame1 = tk.Frame(main_frame)
label1 = tk.Label(frame1, text="Nhập chất phản ứng (ngăn cách bằng dấu phẩy):")
label1.grid(row=0, column=0, sticky='w')
entry_A = tk.Entry(frame1, width=40)
entry_A.grid(row=0, column=1, pady=5)

label2 = tk.Label(frame1, text="Nhập chất sản phẩm (ngăn cách bằng dấu phẩy):")
label2.grid(row=1, column=0, sticky='w')
entry_B = tk.Entry(frame1, width=40)
entry_B.grid(row=1, column=1, pady=5)

label3 = tk.Label(frame1, text="Nhập chuỗi phản ứng (ngăn cách bằng dấu phẩy):")
label3.grid(row=2, column=0, sticky='w')
entry_chuoi = tk.Entry(frame1, width=40)
entry_chuoi.grid(row=2, column=1, pady=5)

process_button = tk.Button(frame1, text="Xử lý", command=MangTinhToan)
process_button.grid(row=3, column=0,columnspan=2, pady=10)
clear_button1 = tk.Button(frame1, text="Xóa", command=clear_frame1)
clear_button1.grid(row=3, column=1, pady=10)

result_label1 = tk.Label(frame1, text="Kết quả")
result_label1.grid(row=4, column=0, sticky='w')
result_text1 = tk.Text(frame1, height=10, width=60)
result_text1.grid(row=4, column=1, pady=5)

# Tạo frame cho mục 2
frame2 = tk.Frame(main_frame)
label4 = tk.Label(frame2, text="Nhập tập hợp chất cần tìm bao đóng (ngăn cách bằng dấu phẩy):")
label4.grid(row=0, column=0, sticky='w')
entry_C = tk.Entry(frame2, width=40)
entry_C.grid(row=0, column=1, pady=5)

process_button2 = tk.Button(frame2, text="Xử lý", command=Closure)
process_button2.grid(row=1, column=0,columnspan=2, pady=10)
clear_button2 = tk.Button(frame2, text="Xóa", command=clear_frame2)
clear_button2.grid(row=1, column=1, pady=10)

result_label2 = tk.Label(frame2, text="Kết quả")
result_label2.grid(row=2, column=0, sticky='w')
result_text2 = tk.Text(frame2, height=10, width=60)
result_text2.grid(row=2, column=1, pady=5)

# Tạo frame cho mục 3
frame3 = tk.Frame(main_frame)
label5 = tk.Label(frame3, text="Nhập chất phản ứng (ngăn cách bằng dấu phẩy):")
label5.grid(row=0, column=0, sticky='w')
entry_D = tk.Entry(frame3, width=40)
entry_D.grid(row=0, column=1, pady=5)

label6 = tk.Label(frame3, text="Nhập chất sản phẩm (ngăn cách bằng dấu phẩy):")
label6.grid(row=1, column=0, sticky='w')
entry_E = tk.Entry(frame3, width=40)
entry_E.grid(row=1, column=1, pady=5)

process_button3 = tk.Button(frame3, text="Xử lý", command=ToiUu)
process_button3.grid(row=2, column=0,columnspan=2, pady=10)
clear_button3 = tk.Button(frame3, text="Xóa", command=clear_frame3)
clear_button3.grid(row=2, column=1, pady=10)

result_label3 = tk.Label(frame3, text="Kết quả")
result_label3.grid(row=3, column=0, sticky='w')
result_text3 = tk.Text(frame3, height=10, width=60)
result_text3.grid(row=3, column=1, pady=5)

# Bắt đầu với hiển thị frame 1
show_frame1()

root.mainloop()
