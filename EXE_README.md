# Image Deduplicator - Windows EXE 版本

## 📦 下载和使用

### 下载 EXE 文件

EXE 文件位于 `dist` 文件夹中：
- **文件名**: `image-deduplicator.exe`
- **大小**: 约 9 MB
- **系统要求**: Windows 7 或更高版本

### 快速开始

#### 方法 1: 双击运行（交互模式）

1. 双击 `image-deduplicator.exe`
2. 按照提示输入要扫描的文件夹路径
3. 查看扫描结果
4. 选择删除策略
5. 确认删除操作

#### 方法 2: 命令行运行

打开命令提示符（CMD）或 PowerShell，然后：

```cmd
# 基本使用（交互模式）
image-deduplicator.exe

# 指定文件夹
image-deduplicator.exe --folder "C:\Users\YourName\Pictures"

# 预览模式（不实际删除）
image-deduplicator.exe --folder "C:\Users\YourName\Pictures" --dry-run

# 自动删除（保留第一个文件）
image-deduplicator.exe --folder "C:\Users\YourName\Pictures" --auto keep-first

# 禁用彩色输出
image-deduplicator.exe --no-color

# 禁用进度条
image-deduplicator.exe --no-progress
```

## 🎯 功能特性

- ✅ 扫描图片文件：.jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff
- ✅ 扫描视频文件：.mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .mpg, .mpeg
- ✅ 基于 SHA-256 哈希值准确识别重复文件
- ✅ 彩色终端输出
- ✅ 进度条显示
- ✅ 多种删除策略
- ✅ 安全确认机制
- ✅ 预览模式（dry-run）

## 📝 使用示例

### 示例 1: 扫描图片文件夹

```cmd
image-deduplicator.exe --folder "C:\Users\YourName\Pictures"
```

### 示例 2: 扫描视频文件夹（预览模式）

```cmd
image-deduplicator.exe --folder "D:\Videos" --dry-run
```

### 示例 3: 自动删除重复文件

```cmd
image-deduplicator.exe --folder "C:\Downloads" --auto keep-first
```

### 示例 4: 扫描多个文件夹（使用批处理）

创建一个 `scan_all.bat` 文件：

```batch
@echo off
echo Scanning Pictures...
image-deduplicator.exe --folder "C:\Users\YourName\Pictures" --auto keep-first

echo Scanning Downloads...
image-deduplicator.exe --folder "C:\Users\YourName\Downloads" --auto keep-first

echo Scanning Videos...
image-deduplicator.exe --folder "D:\Videos" --auto keep-first

echo All done!
pause
```

## ⚙️ 配置文件

首次运行后，配置文件会自动创建在：
```
C:\Users\YourName\.image-deduplicator\config.json
```

你可以编辑这个文件来自定义：
- 支持的文件格式
- 文件读取块大小
- 默认删除策略
- 日志级别

## 🔒 安全性

- ✅ 多重确认机制
- ✅ 每个重复组至少保留一个文件
- ✅ 支持预览模式（dry-run）
- ✅ 详细的日志记录
- ⚠️ 删除操作不可撤销，请谨慎使用

## 📊 性能

- 扫描速度：约 100 个文件/10秒
- 哈希计算：约 10MB/秒
- 内存使用：处理 1000 个文件时约 100MB

## 🐛 故障排除

### 问题 1: EXE 无法运行

**解决方案**:
- 确保你的 Windows 版本是 Windows 7 或更高
- 右键点击 EXE，选择"以管理员身份运行"
- 检查杀毒软件是否阻止了程序

### 问题 2: 找不到文件夹

**解决方案**:
- 使用完整路径，例如：`C:\Users\YourName\Pictures`
- 如果路径包含空格，使用引号：`"C:\My Pictures"`

### 问题 3: 权限错误

**解决方案**:
- 以管理员身份运行程序
- 确保对目标文件夹有读写权限

### 问题 4: 彩色输出显示异常

**解决方案**:
- 使用 `--no-color` 参数禁用彩色输出
- 或者使用 Windows Terminal 而不是 CMD

## 📦 分发 EXE

如果你想分享这个工具给其他人：

1. 只需要分发 `dist\image-deduplicator.exe` 文件
2. 不需要安装 Python 或任何依赖
3. 接收者可以直接运行 EXE 文件

## 🔄 更新

要获取最新版本：

1. 访问 GitHub 仓库：https://github.com/littleblc/image-deduplicator
2. 下载最新的 Release
3. 或者从源码重新构建（见下文）

## 🛠️ 从源码构建 EXE

如果你想自己构建 EXE：

```cmd
# 1. 克隆仓库
git clone https://github.com/littleblc/image-deduplicator.git
cd image-deduplicator

# 2. 安装依赖
pip install -e ".[optional]"
pip install pyinstaller

# 3. 构建 EXE
pyinstaller build_exe.spec --clean

# 4. EXE 文件位于 dist 文件夹
```

或者直接运行：
```cmd
build_exe.bat
```

## 📄 许可证

MIT License - 可自由使用、修改和分发

## 🔗 链接

- GitHub: https://github.com/littleblc/image-deduplicator
- 问题反馈: https://github.com/littleblc/image-deduplicator/issues
- 完整文档: 查看 USAGE.md

## ⭐ 提示

- 建议先使用 `--dry-run` 预览将要删除的文件
- 对重要文件夹进行操作前，请先备份
- 可以使用配置文件自定义行为
- 支持拖放：将文件夹拖到 EXE 上（某些情况下）

---

**享受使用！如果有任何问题，请在 GitHub 上提交 Issue。**
