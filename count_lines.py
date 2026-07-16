import os


def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return len(lines)
    except Exception as e:
        print(f"读取文件失败: {file_path}, 错误: {e}")
        return 0


def main():
    folder_path = 'campus_data'

    if not os.path.exists(folder_path):
        print("文件夹不存在，请检查路径")
        return

    if not os.path.isdir(folder_path):
        print(f"{folder_path} 不是一个文件夹")
        return

    txt_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            txt_files.append(filename)

    if not txt_files:
        print("文件夹中没有找到 .txt 文件")
        return

    for filename in txt_files:
        file_path = os.path.join(folder_path, filename)
        line_count = count_lines_in_file(file_path)
        print(f"{filename}: {line_count} 行")


if __name__ == '__main__':
    main()
