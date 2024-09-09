import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSVファイルのパスを定義
file_paths = [
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_660_seconds-1.jpg.csv',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_660_seconds.jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_660_seconds (1).jpg.csv',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_300_seconds-1 (1).jpg.csv',
    '../csv/csv_240905_MG_CP_1M_NaCl.mp4_frame_at_100_seconds.jpg.csv'
]

# CSVファイルに対応するグラフタイトルを辞書で指定
titles = {
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_660_seconds-1.jpg.csv': 'Distribution of Particle Volume (µm³) - 1M NaOH at after current',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv': 'Distribution of Particle Volume (µm³) - 1M NaOH at current on',
    '../csv/csv_240906_MG_CP_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv': 'Distribution of Particle Volume (µm³) - 1M NaOH at no current',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_660_seconds.jpg.csv': 'Distribution of Particle Volume (µm³) - 1M NaCl and 1M NaOH at after current',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_300_seconds.jpg.csv': 'Distribution of Particle Volume (µm³) - 1M NaCl and 1M NaOH at current on',
    '../csv/csv_240905_MG_CP_1M_NaCl_1M_NaOH.mp4_frame_at_100_seconds.jpg.csv': 'Distribution of Particle Volume (µm³) - 1M NaCl and 1M NaOH at no current',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_660_seconds (1).jpg.csv': 'Distribution of Particle Volume (µm³) - 1M NaCl at after current',
    '../csv/csv_beta_240905_MG_CP_1M_NaCl.mp4_frame_at_300_seconds-1 (1).jpg.csv': 'Distribution of Particle Volume (µm³) - 1M NaCl at current on',
    '../csv/csv_240905_MG_CP_1M_NaCl.mp4_frame_at_100_seconds.jpg.csv': 'Distribution of Particle Volume (µm³) - 1M NaCl at no current'
}

# データフレームを読み込む
dataframes = {path: pd.read_csv(path) for path in file_paths}

# すべてのデータから体積の最小値と最大値を取得
all_volumes = pd.concat([df[df['Index'] != 'Total Volume']['Volume (µm^3)'] for df in dataframes.values()])
all_volumes = pd.to_numeric(all_volumes, errors='coerce')  # 数値に変換
min_volume = all_volumes.min()
max_volume = all_volumes.max()

# 体積を使ったプロット関数を定義
def plot_volume_distribution_with_log_scale(dataframes, min_volume, max_volume):
    bins = np.logspace(np.log10(min_volume), np.log10(max_volume), 30)  # 対数スケールのビンを設定
    for file, df in dataframes.items():
        # 「Total Volume」行を削除
        df_cleaned = df[df['Index'] != 'Total Volume']

        # ヒストグラムを作成（体積を使う）
        plt.figure(figsize=(10, 6))
        plt.hist(df_cleaned['Volume (µm^3)'], bins=bins, edgecolor='black', alpha=0.7)
        plt.xscale('log')  # X軸を対数スケールに設定
        plt.title(titles[file], fontsize=14)
        plt.xlabel('Volume (µm³) [Log Scale]', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.ylim(0, 92)  # Y軸の範囲を0から28に設定
        plt.xlim(min_volume, max_volume)

        # X軸の目盛りを設定
        xticks = np.logspace(np.log10(min_volume), np.log10(max_volume), num=10)  # min_volumeからmax_volumeまでの目盛りを設定
        plt.xticks(xticks, labels=[f"{x:.1e}" for x in xticks])

        plt.grid(True, which='both')  # 主目盛りと副目盛りの両方にグリッドを設定

        # グラフを保存
        output_image_path = f"../log_scale_img/output_with_log_scale_volume_{file.split('/')[-1]}.png"
        plt.savefig(output_image_path)
        plt.close()

# 体積を使ったプロットを生成
plot_volume_distribution_with_log_scale(dataframes, min_volume, max_volume)
