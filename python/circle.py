import sys
import cv2
import numpy as np
import csv

# 引数から画像パスとCSVパスを取得
if len(sys.argv) < 3:
    print("Usage: python script.py <image_path> <csv_path>")
    sys.exit(1)

image_path = sys.argv[1]
csv_path = sys.argv[2]

# 画像を読み込む
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Could not open image {image_path}")
    sys.exit(1)

# 画像の横幅を取得して出力
image_width = image.shape[1]  # 画像の横幅 (ピクセル)
print(f"Image width (in pixels): {image_width}")

# CSVファイルから円の情報を読み込む
csv_data = []
try:
    with open(csv_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            csv_data.append({
                "circle_id": int(float(row[0]) * image_width),
                "radius": int(float(row[1]) * image_width),
                "center_x": int(float(row[2]) * image_width),
                "center_y": int(float(row[3]) * image_width)
            })
except FileNotFoundError:
    print(f"Error: Could not open CSV file {csv_path}")
    sys.exit(1)

# 緑色で円を描画
output_image = image.copy()
for data in csv_data:
    center = (data["center_x"], data["center_y"])
    radius = data["radius"]
    # 円を描画
    cv2.circle(output_image, center, radius, (0, 255, 0), 2)

    # # 円のIDと半径を画像に描画
    # text = f"#{data['circle_id']} R={radius}px"
    # cv2.putText(output_image, text, (center[0], center[1] - 10),
    #             cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

# 処理後の画像を保存
output_image_path = f"with_circle_img/output_with_circles_{image_path.split('/')[-1]}"
cv2.imwrite(output_image_path, output_image)

print(f"Output image saved as {output_image_path}")
