import sys
import cv2
import numpy as np
import csv

# 引数から画像パスを取得
image_path = sys.argv[1]

# 画像を読み込む
image = cv2.imread(image_path)

# 画像の横幅を取得して出力
image_width = image.shape[1]  # 画像の横幅 (ピクセル)
print(f"Image width (in pixels): {image_width}")

# グレースケールに変換（処理しやすくするため）
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 赤色を検出するための範囲を設定し、マスクを作成
lower_red = np.array([0, 0, 100])
upper_red = np.array([50, 50, 255])
mask = cv2.inRange(image, lower_red, upper_red)

# 赤色領域の輪郭を検出
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.0  # フォントサイズを大きくする
thickness = 2     # 太さを増やす

# 各輪郭を円で近似し、半球の体積を計算
output_image = image.copy()
csv_data = []  # CSVに保存するためのデータを格納するリスト
count = 0

for contour in contours:
    if len(contour) >= 5:  # 輪郭が十分な点を持っていることを確認
        count += 1
        (x, y), radius = cv2.minEnclosingCircle(contour)
        radius = int(radius)  # 半径を整数に変換
        center = (int(x), int(y))

        # 半球の体積を計算 V = (4/3) * π * r^3
        volume = (4/3) * np.pi * (radius**3)
        
        # 半径と体積を出力
        print(f"radius: {radius}")
        print(f"volume: {volume}")

        # 近似された円を描画
        cv2.circle(output_image, center, radius, (0, 255, 0), 2)

        # 円の近くに半径と円番号を表示
        text = f"#{count} R={radius}px"
        cv2.putText(output_image, text, (center[0], center[1] - 10),
                    font, font_scale, (255, 0, 0), thickness)

        # CSV用のデータを保存
        csv_data.append([count, radius/image_width, center[0]/image_width, center[1]/image_width])

# 処理後の画像を保存
processed_image_path = f"processed_files/processed_{image_path.split('/')[-1]}"
cv2.imwrite(processed_image_path, output_image)

# CSVファイルに半径と中心座標を保存
csv_file_path = f"circle_info/circles_{image_path.split('/')[-1].replace('.png', '.csv').replace('.jpg', '.csv')}"
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Circle #", "Radius (px)", "Center X", "Center Y"])
    writer.writerows(csv_data)

print(f"CSV file saved at {csv_file_path}")
