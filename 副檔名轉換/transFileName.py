import os
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 設定檔案名稱路徑
settings_path = 'user_settings.pkl'

def load_settings():
    try:
        with open(settings_path, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {"old_ext": ".jpg", "new_ext": ".jpg", "directory": ""}

def save_settings(settings):
    with open(settings_path, 'wb') as f:
        pickle.dump(settings, f)

def rename_files(directory, old_extension, new_extension):
    for filename in os.listdir(directory):
        if filename.endswith(old_extension):
            file_base = os.path.splitext(filename)[0]
            new_filename = file_base + new_extension
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            os.rename(old_file, new_file)
    messagebox.showinfo("完成", "檔案重新命名完成！")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder_selected)

def update_entry_visibility(*args):
    old_choice = old_ext_var.get()
    new_choice = new_ext_var.get()
    entry_old_ext.place_forget()
    entry_new_ext.place_forget()
    if old_choice == "其他":
        entry_old_ext.place(x=150, y=70)
    if new_choice == "其他":
        entry_new_ext.place(x=150, y=150)

def start_renaming():
    folder_path = entry_folder.get()
    old_ext = old_ext_var.get() if old_ext_var.get() != "其他" else entry_old_ext.get()
    new_ext = new_ext_var.get() if new_ext_var.get() != "其他" else entry_new_ext.get()
    if folder_path and old_ext and new_ext:
        rename_files(folder_path, old_ext, new_ext)
        settings = {"old_ext": old_ext, "new_ext": new_ext, "directory": folder_path}
        save_settings(settings)
    else:
        messagebox.showwarning("警告", "請確保所有欄位都已正確填寫！")

app = tk.Tk()
app.title("批量修改檔案附檔名工具")
app.geometry("600x300")

# 設定樣式
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), foreground="blue")
style.configure("TButton", font=("Helvetica", 12, "bold"), background="#E05B5B", foreground="black")
style.configure("TEntry", font=("Helvetica", 12))

frame = ttk.Frame(app)
frame.place(x=20, y=20, width=600, height=260)

lbl_folder = ttk.Label(frame, text="選擇目錄:")
lbl_folder.place(x=0, y=0, height=30)

entry_folder = ttk.Entry(frame, width=30)
entry_folder.place(x=150, y=0, height=30)

btn_browse = ttk.Button(frame, text="瀏覽", command=browse_folder)
btn_browse.place(x=350, y=0, height=30)

extensions = [".jpg", ".png", ".jfif", "其他"]
settings = load_settings()

old_ext_var = tk.StringVar(value=settings['old_ext'])
new_ext_var = tk.StringVar(value=settings['new_ext'])

lbl_old_ext = ttk.Label(frame, text="選擇舊附檔名:")
lbl_old_ext.place(x=0, y=30)

old_extension_menu = ttk.Combobox(frame, textvariable=old_ext_var, values=extensions, width=17)
old_extension_menu.place(x=150, y=30)
old_extension_menu.bind('<<ComboboxSelected>>', update_entry_visibility)

entry_old_ext = ttk.Entry(frame, width=20)

lbl_new_ext = ttk.Label(frame, text="選擇新附檔名:")
lbl_new_ext.place(x=0, y=110)

new_extension_menu = ttk.Combobox(frame, textvariable=new_ext_var, values=extensions, width=17)
new_extension_menu.place(x=150, y=110)
new_extension_menu.bind('<<ComboboxSelected>>', update_entry_visibility)

entry_new_ext = ttk.Entry(frame, width=20)

btn_start = ttk.Button(frame, text="開始轉換", command=start_renaming)
btn_start.place(x=300-50 , y=200)

entry_folder.insert(0, settings['directory'])
update_entry_visibility()  # 初始隱藏輸入框
app.mainloop()