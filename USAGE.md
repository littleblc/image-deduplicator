# 图片去重工具使用指南

## 简介

图片去重工具（Image Deduplicator）是一个命令行应用程序，用于扫描指定文件夹中的所有图片文件，识别内容相同但可能名称不同的重复图片，并提供批量删除功能。

## 功能特性

- ✅ 递归扫描文件夹及其所有子文件夹
- ✅ 支持多种图片格式：.jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff
- ✅ 基于文件内容（SHA-256 哈希）识别重复，而非文件名
- ✅ 彩色终端输出（可选，需要 colorama）
- ✅ 进度条显示（可选，需要 tqdm）
- ✅ 多种删除策略
- ✅ 安全确认机制
- ✅ 预览模式（dry-run）
- ✅ 配置文件支持
- ✅ 详细的日志记录

## 安装

### 基本安装

```bash
pip install image-deduplicator
```

### 从源码安装

```bash
# 在项目目录中安装
pip install -e .
```

### 安装可选依赖

为了获得最佳体验，建议安装可选依赖：

```bash
pip install image-deduplicator[optional]
```

或者单独安装：

```bash
pip install tqdm colorama Pillow
```

## 使用方法

### 基本用法

#### 交互式模式

最简单的使用方式，程序会引导您完成所有步骤：

```bash
image-deduplicator
```

程序会提示您：
1. 输入要扫描的文件夹路径
2. 查看扫描结果和重复文件组
3. 选择删除策略
4. 确认删除操作

#### 指定文件夹

直接指定要扫描的文件夹：

```bash
image-deduplicator --folder /path/to/images
```

#### 预览模式

查看将要删除的文件，但不实际删除：

```bash
image-deduplicator --folder /path/to/images --dry-run
```

#### 自动删除模式

跳过交互式选择，自动使用指定策略删除：

```bash
# 保留每组第一个文件（按路径排序）
image-deduplicator --folder /path/to/images --auto keep-first

# 保留每组最后一个文件（按路径排序）
image-deduplicator --folder /path/to/images --auto keep-last
```

### 命令行选项

```
usage: image-deduplicator [-h] [--folder FOLDER] [--dry-run] 
                          [--auto {keep-first,keep-last}]
                          [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                          [--no-color] [--no-progress] [--version]

选项说明:
  -h, --help            显示帮助信息并退出
  --folder FOLDER       要扫描的文件夹路径
  --dry-run             预览模式：显示将要删除的文件但不实际删除
  --auto {keep-first,keep-last}
                        自动删除模式：
                        - keep-first: 保留每组第一个文件
                        - keep-last: 保留每组最后一个文件
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        日志级别（默认: INFO）
  --no-color            禁用彩色输出
  --no-progress         禁用 tqdm 进度条
  --version             显示版本信息并退出
```

### 使用示例

#### 示例 1: 扫描并交互式删除

```bash
image-deduplicator --folder ~/Pictures
```

#### 示例 2: 预览将要删除的文件

```bash
image-deduplicator --folder ~/Downloads --dry-run --auto keep-first
```

#### 示例 3: 自动删除，保留第一个文件

```bash
image-deduplicator --folder /media/photos --auto keep-first
```

#### 示例 4: 禁用彩色输出和进度条

```bash
image-deduplicator --folder ~/Pictures --no-color --no-progress
```

#### 示例 5: 启用调试日志

```bash
image-deduplicator --folder ~/Pictures --log-level DEBUG
```

## 配置文件

### 配置文件位置

配置文件位于：`~/.image-deduplicator/config.json`

首次运行时，程序会自动创建默认配置文件。

### 配置选项

```json
{
  "supported_extensions": [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".tiff"
  ],
  "chunk_size": 8192,
  "default_strategy": "keep_first",
  "enable_cache": true,
  "log_level": "INFO"
}
```

#### 配置项说明

- **supported_extensions**: 支持的图片文件扩展名列表
- **chunk_size**: 读取文件时的块大小（字节），用于优化内存使用
- **default_strategy**: 默认删除策略（keep_first 或 keep_last）
- **enable_cache**: 是否启用哈希缓存
- **log_level**: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）

### 修改配置

您可以手动编辑配置文件来自定义行为：

```bash
# Linux/Mac
nano ~/.image-deduplicator/config.json

# Windows
notepad %USERPROFILE%\.image-deduplicator\config.json
```

## 删除策略

### 保留第一个文件（keep-first）

按文件路径字母顺序排序，保留每组的第一个文件，删除其余文件。

**适用场景**：
- 希望保留路径较短的文件
- 希望保留原始位置的文件

### 保留最后一个文件（keep-last）

按文件路径字母顺序排序，保留每组的最后一个文件，删除其余文件。

**适用场景**：
- 希望保留最近整理的文件
- 希望保留特定命名模式的文件

### 手动选择（交互模式）

在交互模式下，您可以查看每个重复组的详细信息后再决定使用哪种策略。

## 日志文件

### 日志位置

日志文件位于：`~/.image-deduplicator/error.log`

### 日志内容

日志文件记录：
- 程序启动和退出信息
- 扫描和处理进度
- 成功删除的文件
- 删除失败的文件及原因
- 错误和警告信息

### 查看日志

```bash
# Linux/Mac
tail -f ~/.image-deduplicator/error.log

# Windows
type %USERPROFILE%\.image-deduplicator\error.log
```

## 安全性

### 多重确认机制

1. **预览重复组**：在删除前显示所有重复文件组
2. **策略选择**：明确选择删除策略
3. **删除确认**：显示将要删除的文件列表，要求最终确认
4. **警告提示**：提醒操作不可撤销

### 保护机制

- 每个重复组至少保留一个文件
- 删除失败时继续处理其他文件
- 详细的错误日志记录
- 支持预览模式（dry-run）

## 性能优化

### 内存优化

- 使用流式读取处理大文件（8KB 块）
- 哈希缓存避免重复计算
- 增量处理文件列表

### 速度优化

- 高效的文件扫描算法
- SHA-256 哈希计算
- 批量文件操作

### 性能指标

- 扫描速度：约 100 个文件/10秒
- 哈希计算：约 10MB/秒
- 内存使用：处理 1000 个文件时约 100MB

## 常见问题

### Q: 如何撤销删除操作？

A: 删除操作是不可撤销的。建议先使用 `--dry-run` 预览将要删除的文件。

### Q: 程序会删除所有重复文件吗？

A: 不会。每个重复组至少保留一个文件。

### Q: 支持哪些图片格式？

A: 默认支持 .jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff。可以通过配置文件添加其他格式。

### Q: 如何判断两个图片是否重复？

A: 程序计算每个文件的 SHA-256 哈希值。如果两个文件的哈希值相同，则认为它们内容完全相同。

### Q: 程序会修改原始文件吗？

A: 不会。程序只读取文件内容计算哈希值，不会修改文件。只有在用户确认后才会删除文件。

### Q: 如何处理符号链接？

A: 程序会跟随符号链接并处理链接指向的实际文件。

### Q: 扫描大量文件时程序很慢怎么办？

A: 可以尝试：
1. 启用哈希缓存（默认已启用）
2. 调整 chunk_size 配置
3. 使用 SSD 存储
4. 减少同时运行的其他程序

### Q: 如何禁用彩色输出？

A: 使用 `--no-color` 选项：
```bash
image-deduplicator --no-color
```

### Q: 如何禁用进度条？

A: 使用 `--no-progress` 选项：
```bash
image-deduplicator --no-progress
```

## 故障排除

### 权限错误

如果遇到权限错误：
1. 确保对目标文件夹有读取权限
2. 确保对要删除的文件有写入权限
3. 在 Linux/Mac 上可能需要使用 `sudo`（不推荐）

### 文件被占用

如果文件正在被其他程序使用：
1. 关闭正在使用该文件的程序
2. 程序会跳过被占用的文件并继续处理其他文件

### 配置文件错误

如果配置文件格式错误：
1. 程序会自动使用默认配置
2. 检查 JSON 格式是否正确
3. 删除配置文件让程序重新创建

## 贡献

欢迎贡献代码、报告问题或提出建议！

## 许可证

本项目采用 MIT 许可证。

## 更新日志

### v0.1.0 (2024-12-19)

- ✨ 初始版本发布
- ✨ 支持基本的图片去重功能
- ✨ 支持多种删除策略
- ✨ 添加彩色输出支持（colorama）
- ✨ 添加进度条支持（tqdm）
- ✨ 添加配置文件支持
- ✨ 添加详细的帮助文档
