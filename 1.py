import os
import time
import hashlib
import shutil
import subprocess

# === 路径配置 ===
SOURCE_DIR = "/Users/owner/OneDrive - get net/NewFile/"
TARGET_DIR = "/Users/owner/cnebiblefellowship/public/NewFile/"
INDEX_HTML = "/Users/owner/cnebiblefellowship/public/index.html"

# 支持的扩展名
VALID_EXTENSIONS = {".doc", ".docx", ".m4a", ".mp3", ".pdf", ".mp4"}

# 哈希缓存
existing_hashes = set()

# === 工具函数 ===

def get_file_hash(filepath):
    """计算文件 SHA256 哈希，可能抛出 IOError/PermissionError"""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def format_file_size(bytes_size):
    return f"{bytes_size / (1024 * 1024):.1f} MB"

def get_file_type(ext):
    ext = ext.lower().lstrip(".")
    if ext in ["mp3", "m4a"]:
        return "audio"
    elif ext in ["doc", "docx"]:
        return "docx"
    elif ext == "pdf":
        return "pdf"
    elif ext == "mp4":
        return "video"
    else:
        return ext

def insert_into_index(filepath):
    if not os.path.exists(INDEX_HTML):
        print("❌ index.html 不存在")
        return

    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1]
    fsize = os.path.getsize(filepath)
    type_str = get_file_type(ext)
    size_str = format_file_size(fsize)

    new_line = f"    {{ name: '{filename}', size: '{size_str}', type: '{type_str}' }},\n"

    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "//2" in line:
            lines.insert(i + 1, new_line)
            break

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"📝 index.html 插入新条目：{filename}")

def trigger_download(filepath):
    """
    触发 OneDrive 客户端下载占位文件：
      - macOS 下用 `open`
      - Windows 下用 `os.startfile`
    """
    print(f"⏳ 尝试触发 OneDrive 下载：{os.path.basename(filepath)}")
    try:
        if os.name == 'posix':
            subprocess.run(["open", filepath], check=True)
        elif os.name == 'nt':
            os.startfile(filepath)
        else:
            print("⚠️ 不支持的操作系统，无法自动触发下载")
        # 等待一点时间让客户端启动下载
        time.sleep(1)
    except Exception as ex:
        print(f"❌ 触发下载失败：{ex}")

# === 主监控逻辑 ===

def monitor():
    print("🟢 正在持续监控文件夹...")

    while True:
        # 支持手动清除缓存
        if os.path.exists("reset.hash"):
            existing_hashes.clear()
            print("♻️ 已清除哈希缓存（重刷所有文件）")
            os.remove("reset.hash")

        for fname in os.listdir(SOURCE_DIR):
            src_path = os.path.join(SOURCE_DIR, fname)
            if not os.path.isfile(src_path):
                continue

            ext = os.path.splitext(fname)[1].lower()
            if ext not in VALID_EXTENSIONS:
                continue

            # 如果文件大小为 0，视为占位文件，触发下载
            try:
                if os.path.getsize(src_path) == 0:
                    print(f"⚠️ 占位文件检测到（大小为 0）：{fname}")
                    trigger_download(src_path)
                    continue
            except Exception as e:
                print(f"⚠️ 检测大小失败：{fname}，{e}")
                trigger_download(src_path)
                continue

            # 计算哈希，若抛错也当作占位文件处理
            try:
                file_hash = get_file_hash(src_path)
            except Exception as e:
                print(f"⚠️ 读取失败，可能为占位文件：{fname}，{e}")
                trigger_download(src_path)
                continue

            # 已处理过的文件跳过
            if file_hash in existing_hashes:
                continue

            # 新文件：复制并写入 index.html
            existing_hashes.add(file_hash)
            dst_path = os.path.join(TARGET_DIR, fname)

            try:
                shutil.copy2(src_path, dst_path)
                print(f"📂 已复制新文件：{fname}")
                insert_into_index(dst_path)
            except Exception as e:
                print(f"❌ 复制或插入失败：{e}")

        # 每 0.1 秒检查一次
        time.sleep(0.1)

# === 初始化已有文件哈希 ===

if __name__ == "__main__":
    os.makedirs(TARGET_DIR, exist_ok=True)
    for fname in os.listdir(TARGET_DIR):
        fpath = os.path.join(TARGET_DIR, fname)
        if os.path.isfile(fpath) and os.path.splitext(fname)[1].lower() in VALID_EXTENSIONS:
            try:
                existing_hashes.add(get_file_hash(fpath))
            except:
                pass
    monitor()
