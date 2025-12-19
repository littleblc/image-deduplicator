# Release Notes - Image Deduplicator v0.1.0

## 🎉 首次发布

这是 Image Deduplicator 的第一个正式版本！

## ✨ 主要功能

### 文件支持
- ✅ **图片格式**: .jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff
- ✅ **视频格式**: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .mpg, .mpeg

### 核心功能
- ✅ 递归扫描文件夹及所有子文件夹
- ✅ 基于 SHA-256 哈希值准确识别重复文件
- ✅ 多种删除策略（保留第一个/最后一个/手动选择）
- ✅ 安全的多重确认机制
- ✅ 预览模式（dry-run）

### 用户界面
- ✅ 彩色终端输出（使用 colorama）
- ✅ 美观的进度条（使用 tqdm）
- ✅ 友好的交互式界面
- ✅ 详细的帮助文档

### 配置和日志
- ✅ 配置文件支持（~/.image-deduplicator/config.json）
- ✅ 详细的日志记录
- ✅ 可自定义的设置

## 📦 下载

### Windows 用户

下载独立的 EXE 文件（无需安装 Python）：

**[下载 image-deduplicator.exe](https://github.com/littleblc/image-deduplicator/releases/download/v0.1.0/image-deduplicator.exe)**

- 文件大小：约 9 MB
- 系统要求：Windows 7 或更高版本
- 无需安装，直接运行

### Python 用户

通过 pip 安装：

```bash
pip install git+https://github.com/littleblc/image-deduplicator.git
```

或从源码安装：

```bash
git clone https://github.com/littleblc/image-deduplicator.git
cd image-deduplicator
pip install -e ".[optional]"
```

## 🚀 快速开始

### Windows EXE 版本

```cmd
# 交互模式
image-deduplicator.exe

# 指定文件夹
image-deduplicator.exe --folder "C:\Users\YourName\Pictures"

# 预览模式
image-deduplicator.exe --folder "C:\Users\YourName\Pictures" --dry-run

# 自动删除
image-deduplicator.exe --folder "C:\Users\YourName\Pictures" --auto keep-first
```

### Python 版本

```bash
# 交互模式
image-deduplicator

# 指定文件夹
image-deduplicator --folder /path/to/images

# 预览模式
image-deduplicator --folder /path/to/images --dry-run

# 自动删除
image-deduplicator --folder /path/to/images --auto keep-first
```

## 📖 文档

- [完整使用指南](USAGE.md)
- [Windows EXE 使用说明](EXE_README.md)
- [GitHub 仓库](https://github.com/littleblc/image-deduplicator)

## 🔧 技术细节

### 依赖项
- Python 3.8+
- colorama >= 0.4.6（可选，用于彩色输出）
- tqdm >= 4.64.0（可选，用于进度条）
- Pillow >= 9.0（可选，用于测试）

### 测试
- 56 个单元测试，全部通过
- 测试覆盖率：90%+
- 使用 pytest 和 hypothesis 进行测试

### 性能
- 扫描速度：约 100 个文件/10秒
- 哈希计算：约 10MB/秒
- 内存使用：处理 1000 个文件时约 100MB

## 🐛 已知问题

目前没有已知的重大问题。

如果你发现任何问题，请在 [GitHub Issues](https://github.com/littleblc/image-deduplicator/issues) 上报告。

## 🙏 致谢

感谢所有测试和反馈的用户！

## 📄 许可证

MIT License - 可自由使用、修改和分发

---

**完整更新日志**

### v0.1.0 (2024-12-19)

#### 新增功能
- ✨ 初始版本发布
- ✨ 支持图片和视频文件去重
- ✨ 彩色终端输出
- ✨ 进度条显示
- ✨ 配置文件支持
- ✨ Windows EXE 版本
- ✨ 详细的文档

#### 改进
- 🎨 友好的用户界面
- ⚡ 高效的文件扫描和哈希计算
- 🔒 安全的删除机制
- 📝 完整的测试覆盖

---

**下载链接**

- [Windows EXE (9 MB)](https://github.com/littleblc/image-deduplicator/releases/download/v0.1.0/image-deduplicator.exe)
- [源代码 (zip)](https://github.com/littleblc/image-deduplicator/archive/refs/tags/v0.1.0.zip)
- [源代码 (tar.gz)](https://github.com/littleblc/image-deduplicator/archive/refs/tags/v0.1.0.tar.gz)
