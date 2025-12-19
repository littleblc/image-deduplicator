# 下载 Image Deduplicator

## 🚀 快速下载

### Windows 用户（推荐）

直接下载独立的 EXE 文件，无需安装 Python：

**[点击下载 image-deduplicator.exe](https://github.com/littleblc/image-deduplicator/raw/main/dist/image-deduplicator.exe)**

- 📦 文件大小：约 9 MB
- 💻 系统要求：Windows 7 或更高版本
- ✅ 无需安装，直接运行
- 🎨 包含彩色输出和进度条

### 使用方法

下载后：

1. **双击运行** - 直接双击 `image-deduplicator.exe` 启动程序
2. **命令行运行** - 在 CMD 或 PowerShell 中运行：
   ```cmd
   image-deduplicator.exe --folder "C:\Users\YourName\Pictures"
   ```

详细使用说明请查看 [EXE_README.md](EXE_README.md)

---

## 🐍 Python 用户

如果你已经安装了 Python 3.8+，可以通过以下方式安装：

### 方法 1: 从 GitHub 安装

```bash
pip install git+https://github.com/littleblc/image-deduplicator.git
```

### 方法 2: 克隆仓库安装

```bash
git clone https://github.com/littleblc/image-deduplicator.git
cd image-deduplicator
pip install -e ".[optional]"
```

### 使用方法

安装后，在命令行中运行：

```bash
image-deduplicator --folder /path/to/images
```

---

## 📋 功能特性

- ✅ 支持图片：.jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff
- ✅ 支持视频：.mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .mpg, .mpeg
- ✅ 基于 SHA-256 哈希值准确识别重复
- ✅ 彩色终端输出
- ✅ 进度条显示
- ✅ 多种删除策略
- ✅ 安全确认机制
- ✅ 预览模式（dry-run）

---

## 📖 文档

- [完整使用指南](USAGE.md)
- [Windows EXE 使用说明](EXE_README.md)
- [发布说明](RELEASE_NOTES.md)

---

## 🔗 链接

- **GitHub 仓库**: https://github.com/littleblc/image-deduplicator
- **问题反馈**: https://github.com/littleblc/image-deduplicator/issues
- **直接下载 EXE**: https://github.com/littleblc/image-deduplicator/raw/main/dist/image-deduplicator.exe

---

## ⚠️ 安全提示

- 从官方 GitHub 仓库下载以确保安全
- 首次使用建议先用 `--dry-run` 预览
- 对重要文件夹操作前请先备份

---

**享受使用！如有问题请在 GitHub 上提交 Issue。**
