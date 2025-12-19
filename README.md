# Image Deduplicator

图片去重工具 - 一个命令行应用程序，用于扫描指定文件夹中的所有图片文件，识别内容相同但可能名称不同的重复图片，并提供批量删除功能。

## 功能特性

- ✅ 递归扫描文件夹中的所有图片文件
- ✅ 支持多种图片格式：.jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff
- ✅ 通过 SHA-256 哈希值准确识别重复图片
- ✅ 提供多种删除策略（保留第一个、保留最后一个、手动选择）
- ✅ 安全的删除确认机制
- ✅ 友好的命令行界面
- ✨ **彩色终端输出**（使用 colorama）
- ✨ **进度条显示**（使用 tqdm）
- ✨ **配置文件支持**（~/.image-deduplicator/config.json）
- ✨ **详细的帮助文档**（见 USAGE.md）

## 安装

### 基本安装

在项目目录中运行：

```bash
pip install -e .
```

### 安装可选依赖（推荐）

为了获得最佳体验（彩色输出和进度条），建议安装可选依赖：

```bash
pip install -e ".[optional]"
```

这将安装：
- `tqdm` - 美观的进度条显示
- `colorama` - 彩色终端输出
- `Pillow` - 图片处理库（用于测试）

### 安装所有依赖（开发）

如果你想进行开发和测试：

```bash
pip install -e ".[all]"
```

这将安装所有可选依赖和测试依赖。

## 快速开始

### 交互式模式

```bash
image-deduplicator
```

程序会引导您完成所有步骤。

### 常用命令

```bash
# 指定文件夹
image-deduplicator --folder /path/to/images

# 预览模式（不实际删除）
image-deduplicator --folder /path/to/images --dry-run

# 自动删除（保留第一个）
image-deduplicator --folder /path/to/images --auto keep-first

# 禁用彩色输出
image-deduplicator --no-color

# 禁用进度条
image-deduplicator --no-progress
```

## 详细文档

查看 [USAGE.md](USAGE.md) 获取完整的使用指南，包括：
- 详细的命令行选项说明
- 配置文件使用方法
- 删除策略详解
- 常见问题解答
- 故障排除指南

## 开发

运行测试：

```bash
pytest
```

运行测试并查看覆盖率：

```bash
pytest --cov=src --cov-report=html --cov-report=term
```

## 项目结构

```
image-deduplicator/
├── src/
│   └── image_deduplicator/
│       ├── __init__.py
│       ├── models.py       # 核心数据模型
│       ├── scanner.py      # 文件扫描器
│       ├── hasher.py       # 哈希计算器
│       ├── detector.py     # 重复检测器
│       ├── deleter.py      # 文件删除器
│       ├── cli.py          # 命令行界面
│       └── main.py         # 主程序入口
├── tests/                  # 测试文件
├── pyproject.toml          # 项目配置
└── README.md
```

## 许可证

MIT License
