import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, simpledialog, scrolledtext

# 全域變數
points = []
scale_points = []
scale_length = 0
snap_distance = 20



def mouse_callback(event, x, y, flags, param):
    global points, scale_points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(scale_points) < 2:
            scale_points.append((x, y))
        else:
            if len(points) > 2 and calculate_distance((x, y), points[0]) < snap_distance:
              x,y = points[0]
              points.append((x,y))
            else:
              points.append((x, y))

def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_scale_length():
    global scale_length
    length_str = simpledialog.askstring("輸入比例尺長度", "請輸入比例尺的實際長度（米）：")
    if length_str:
        try:
            scale_length = float(length_str)
        except ValueError:
            tk.messagebox.showerror("錯誤", "無效的長度輸入。")

def calculate_area():
    global points, scale_points, scale_length, output_text
    if len(points) > 2 and len(scale_points) == 2 and scale_length > 0:
        scale_pixel_length = np.sqrt((scale_points[0][0] - scale_points[1][0])**2 + (scale_points[0][1] - scale_points[1][1])**2)
        pixel_to_real_ratio = scale_length / scale_pixel_length
        area_pixels = cv2.contourArea(np.array([points]))
        area_real = area_pixels * (pixel_to_real_ratio**2)
        output_text.insert(tk.END, f"標注區域的面積為：{area_real:.2f} 平方米\n")
    else:
        output_text.insert(tk.END, "請先標注區域邊界和比例尺。\n")

def reset():
    global image, clone, points, scale_points, scale_length, output_text
    image = clone.copy()
    points = []
    scale_points = []
    scale_length = 0
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END,f"1. 在圖上選定兩點畫出比例尺，然後點擊‘輸入比例尺長度’並輸入長度。 2. 畫出計算面積範圍 3. 點擊‘計算面積’\n")
    output_text.insert(tk.END, f"\n")

# 載入圖像
image = cv2.imread("floor_plan.png")
clone = image.copy()

cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_callback)

# Tkinter GUI
root = tk.Tk()
root.title("圖像處理")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

scale_button = ttk.Button(frame, text="輸入比例尺長度", command=get_scale_length)
scale_button.pack(side=tk.LEFT, padx=5)

calculate_button = ttk.Button(frame, text="計算面積", command=calculate_area)
calculate_button.pack(side=tk.LEFT, padx=5)

reset_button = ttk.Button(frame, text="重置", command=reset)
reset_button.pack(side=tk.LEFT, padx=5)

# 輸出視窗
output_text = scrolledtext.ScrolledText(root, width=40, height=10)
output_text.pack(padx=10, pady=10)

output_text.insert(tk.END, f"1. 在圖上選定兩點畫出比例尺，然後點擊‘輸入比例尺長度’並輸入長度。 2. 畫出計算面積範圍 3. 點擊‘計算面積’\n")
output_text.insert(tk.END, f"\n")


def update_image():
    temp_image = image.copy()
    if len(points) > 1:
        cv2.polylines(temp_image, [np.array(points)], False, (0, 255, 0), 2)
    if len(scale_points) == 2:
        cv2.line(temp_image, scale_points[0], scale_points[1], (255, 0, 0), 2)
    cv2.imshow("image", temp_image)
    root.after(10, update_image)

update_image()
root.mainloop()

cv2.destroyAllWindows()
