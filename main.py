import cv2
import numpy as np

# 全域變數
points = []  # 儲存標注區域的點
scale_points = []  # 儲存比例尺的點
scale_length = 0  # 比例尺的實際長度
snap_distance = 20  # 吸附距離閾值
print("\033[0;31;40m", "運行程式后，請在圖像上標注比例尺和範圍。標注完成後，按c鍵計算面積；按r重置比例尺和範圍標注；按q退出程式。", "\033[0m")
def mouse_callback(event, x, y, flags, param):
    """滑鼠事件回呼函式"""
    global points, scale_points, scale_length

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(scale_points) < 2:
            # 標注比例尺
            scale_points.append((x, y))
            if len(scale_points) == 2:
                # 取得比例尺長度
                scale_length_str = input("請輸入比例尺的實際長度數值，單位為米: ")
                scale_length = float(scale_length_str.split()[0])  # 提取數值部分
        else:
            # 標注區域邊界
            if len(points) > 2 and calculate_distance((x, y), points[0]) < snap_distance:
              #吸附到第一個點
              x,y = points[0]
              points.append((x,y))
            else:
              points.append((x, y))

def calculate_distance(p1, p2):
    """計算兩點之間的距離"""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# 1. 載入樓層平面圖像
image = cv2.imread("floor_plan.png")  # 將 "floor_plan.jpg" 替換為您的圖像路徑
clone = image.copy()

# 2. 手動標注邊界範圍
print("請先標注比例尺，后標注範圍。")
print("在圖像上單擊，綫段會自動標注在點之間。")
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_callback)


while True:
    temp_image = image.copy()

    # 繪製已標注的線條
    if len(points) > 1:
        cv2.polylines(temp_image, [np.array(points)], False, (0, 255, 0), 2)
    # 繪製比例尺

    if len(scale_points) == 2:

        cv2.line(temp_image, scale_points[0], scale_points[1], (255, 0, 0), 2)

    cv2.imshow("image", temp_image)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        # 重置標注
        image = clone.copy()
        points = []
        scale_points = []
        scale_length = 0
    elif key == ord("c"):
        # 計算面積
        if len(points) > 2 and len(scale_points) == 2 and scale_length > 0:
            # 計算比例尺的像素長度
            scale_pixel_length = np.sqrt((scale_points[0][0] - scale_points[1][0])**2 + (scale_points[0][1] - scale_points[1][1])**2)
            # 計算像素到實際長度的比例
            pixel_to_real_ratio = scale_length / scale_pixel_length

            # 計算標注區域的面積（像素單位）
            area_pixels = cv2.contourArea(np.array([points]))
            # 計算實際面積
            area_real = area_pixels * (pixel_to_real_ratio**2)

            print(f"標注區域的面積為：{area_real:.2f} 平方米")  # 假設比例尺單位為米
        else:
            print("請先標注區域邊界和比例尺。")
    elif key == ord("q"):
        # 退出
        break

cv2.destroyAllWindows()