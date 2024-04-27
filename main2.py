import os
import subprocess

# 获取当前文件夹路径
current_directory = os.getcwd()

# 读取时间段列表
time_segments = []
with open(os.path.join(current_directory, "1.txt"), "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        if " --> " in line:
            start, end = line.strip().split(" --> ")
            start = start.replace(",", ".")
            end = end.replace(",", ".")
            time_segments.append({"start": start, "end": end})

# 提取视频片段并保存为临时文件
output_files = []
for i, segment in enumerate(time_segments, start=1):
    output_file = f"part{i}.mp4"
    start = segment["start"]
    end = segment["end"]
    cmd = [
        "ffmpeg",
        "-i", os.path.join(current_directory, "1.mp4"),
        "-ss", start,
        "-to", end,
        "-vf", "format=yuv420p",
        "-af", "aresample=async=1:first_pts=0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-vsync", "2",
        "-async", "1",
        output_file
    ]
    subprocess.run(cmd, capture_output=True)
    output_files.append(output_file)

# 创建concat文件
with open(os.path.join(current_directory, "list.txt"), "w", encoding="utf-8") as f:
    for output_file in output_files:
        f.write(f"file '{output_file}'\n")

# 合并视频片段
cmd = [
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", os.path.join(current_directory, "list.txt"),
    "-vf", "format=yuv420p",
    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
    "-c:a", "aac", "-b:a", "192k",
    "-vsync", "2",
    "-async", "1",
    os.path.join(current_directory, "output.mp4")
]
subprocess.run(cmd, capture_output=True)

# 删除临时文件
for output_file in output_files:
    if os.path.exists(output_file):
        os.remove(output_file)

# 删除concat文件
if os.path.exists(os.path.join(current_directory, "list.txt")):
    os.remove(os.path.join(current_directory, "list.txt"))
