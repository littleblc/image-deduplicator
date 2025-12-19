# 设计文档

## 概述

图片去重工具是一个基于 Python 的命令行应用程序，通过计算文件哈希值来识别重复的图片文件。系统采用模块化设计，将文件扫描、哈希计算、重复检测和用户交互分离为独立组件，确保代码的可维护性和可测试性。

核心工作流程：
1. 用户指定目标文件夹
2. 系统递归扫描并识别所有图片文件
3. 计算每个图片文件的 SHA-256 哈希值
4. 将具有相同哈希值的文件分组
5. 向用户展示重复组
6. 根据用户选择删除重复文件

## 架构

系统采用分层架构，包含以下主要层次：

```
┌─────────────────────────────────────┐
│      用户界面层 (CLI Interface)      │
│  - 命令行交互                        │
│  - 进度显示                          │
│  - 结果展示                          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      业务逻辑层 (Business Logic)     │
│  - 重复检测                          │
│  - 删除策略                          │
│  - 工作流协调                        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      核心服务层 (Core Services)      │
│  - 文件扫描器                        │
│  - 哈希计算器                        │
│  - 文件操作器                        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      文件系统层 (File System)        │
│  - 操作系统文件 API                  │
└─────────────────────────────────────┘
```

### 模块划分

1. **scanner.py** - 文件扫描模块
   - 递归遍历文件夹
   - 识别图片文件
   - 报告扫描进度

2. **hasher.py** - 哈希计算模块
   - 计算文件 SHA-256 哈希值
   - 优化内存使用（流式读取）
   - 缓存哈希结果

3. **detector.py** - 重复检测模块
   - 分组相同哈希的文件
   - 生成重复报告

4. **deleter.py** - 文件删除模块
   - 实现删除策略
   - 安全删除文件
   - 错误处理

5. **cli.py** - 命令行界面模块
   - 用户输入处理
   - 菜单显示
   - 结果格式化输出

6. **main.py** - 主程序入口
   - 协调各模块
   - 控制主工作流

## 组件和接口

### FileScanner 类

```python
class FileScanner:
    """文件扫描器，负责递归扫描文件夹并识别图片文件"""
    
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    
    def scan(self, folder_path: str, progress_callback: Optional[Callable] = None) -> List[str]:
        """
        扫描指定文件夹，返回所有图片文件路径
        
        参数:
            folder_path: 目标文件夹路径
            progress_callback: 可选的进度回调函数
            
        返回:
            图片文件路径列表
            
        异常:
            ValueError: 如果文件夹路径无效
            PermissionError: 如果没有访问权限
        """
        pass
    
    def is_image_file(self, file_path: str) -> bool:
        """判断文件是否为支持的图片格式"""
        pass
```

### FileHasher 类

```python
class FileHasher:
    """文件哈希计算器，使用 SHA-256 算法"""
    
    CHUNK_SIZE = 8192  # 8KB 块大小，用于流式读取
    
    def __init__(self):
        self._hash_cache: Dict[str, str] = {}
    
    def compute_hash(self, file_path: str) -> str:
        """
        计算文件的 SHA-256 哈希值
        
        参数:
            file_path: 文件路径
            
        返回:
            十六进制格式的哈希字符串
            
        异常:
            FileNotFoundError: 如果文件不存在
            IOError: 如果读取文件失败
        """
        pass
    
    def compute_hashes(self, file_paths: List[str], progress_callback: Optional[Callable] = None) -> Dict[str, str]:
        """
        批量计算文件哈希值
        
        返回:
            文件路径到哈希值的映射字典
        """
        pass
```

### DuplicateDetector 类

```python
class DuplicateDetector:
    """重复文件检测器"""
    
    def find_duplicates(self, file_hashes: Dict[str, str]) -> List[List[str]]:
        """
        根据哈希值查找重复文件
        
        参数:
            file_hashes: 文件路径到哈希值的映射
            
        返回:
            重复组列表，每组包含具有相同哈希的文件路径列表
        """
        pass
    
    def group_by_hash(self, file_hashes: Dict[str, str]) -> Dict[str, List[str]]:
        """将文件按哈希值分组"""
        pass
```

### FileDeleter 类

```python
class FileDeleter:
    """文件删除器，实现各种删除策略"""
    
    class DeletionStrategy(Enum):
        KEEP_FIRST = "keep_first"      # 保留每组第一个
        KEEP_LAST = "keep_last"        # 保留每组最后一个
        MANUAL = "manual"              # 手动选择
    
    def delete_duplicates(
        self, 
        duplicate_groups: List[List[str]], 
        strategy: DeletionStrategy,
        dry_run: bool = False
    ) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        删除重复文件
        
        参数:
            duplicate_groups: 重复组列表
            strategy: 删除策略
            dry_run: 如果为 True，只返回将要删除的文件，不实际删除
            
        返回:
            (成功删除的文件列表, 失败的文件及原因列表)
        """
        pass
    
    def select_files_to_delete(
        self, 
        duplicate_groups: List[List[str]], 
        strategy: DeletionStrategy
    ) -> List[str]:
        """根据策略选择要删除的文件"""
        pass
    
    def safe_delete(self, file_path: str) -> bool:
        """安全删除单个文件"""
        pass
```

### CLI 类

```python
class CLI:
    """命令行界面"""
    
    def display_welcome(self):
        """显示欢迎信息"""
        pass
    
    def prompt_folder_path(self) -> str:
        """提示用户输入文件夹路径"""
        pass
    
    def display_progress(self, current: int, total: int, message: str):
        """显示进度信息"""
        pass
    
    def display_duplicate_groups(self, duplicate_groups: List[List[str]]):
        """显示重复文件组"""
        pass
    
    def prompt_deletion_strategy(self) -> FileDeleter.DeletionStrategy:
        """提示用户选择删除策略"""
        pass
    
    def confirm_deletion(self, files_to_delete: List[str]) -> bool:
        """确认删除操作"""
        pass
    
    def display_results(self, deleted: List[str], failed: List[Tuple[str, str]]):
        """显示删除结果"""
        pass
```

## 数据模型

### ImageFile

```python
@dataclass
class ImageFile:
    """图片文件信息"""
    path: str           # 完整文件路径
    size: int           # 文件大小（字节）
    hash: str           # SHA-256 哈希值
    
    def __post_init__(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"文件不存在: {self.path}")
```

### DuplicateGroup

```python
@dataclass
class DuplicateGroup:
    """重复文件组"""
    hash: str                    # 共同的哈希值
    files: List[ImageFile]       # 该组中的所有文件
    
    def __post_init__(self):
        if len(self.files) < 2:
            raise ValueError("重复组必须包含至少 2 个文件")
        # 按路径排序
        self.files.sort(key=lambda f: f.path)
    
    @property
    def count(self) -> int:
        """返回组中文件数量"""
        return len(self.files)
    
    @property
    def total_size(self) -> int:
        """返回组中所有文件的总大小"""
        return sum(f.size for f in self.files)
    
    @property
    def wasted_space(self) -> int:
        """返回重复文件浪费的空间（保留一个文件）"""
        return self.total_size - self.files[0].size
```

### ScanResult

```python
@dataclass
class ScanResult:
    """扫描结果"""
    total_files: int                      # 扫描到的总文件数
    duplicate_groups: List[DuplicateGroup] # 重复组列表
    scan_time: float                      # 扫描耗时（秒）
    
    @property
    def duplicate_count(self) -> int:
        """返回重复文件总数"""
        return sum(group.count for group in self.duplicate_groups)
    
    @property
    def unique_count(self) -> int:
        """返回唯一文件数"""
        return self.total_files - self.duplicate_count + len(self.duplicate_groups)
    
    @property
    def total_wasted_space(self) -> int:
        """返回所有重复文件浪费的总空间"""
        return sum(group.wasted_space for group in self.duplicate_groups)
```


## 正确性属性

*属性是指在系统的所有有效执行中都应该成立的特征或行为——本质上是关于系统应该做什么的形式化陈述。属性作为人类可读规范和机器可验证正确性保证之间的桥梁。*

### 属性 1: 路径验证正确性
*对于任何*文件夹路径输入，验证函数应该正确返回该路径是否存在且可访问
**验证: 需求 1.2**

### 属性 2: 递归扫描完整性
*对于任何*有效的文件夹路径，扫描应该访问该文件夹及其所有子文件夹中的每个文件
**验证: 需求 1.4**

### 属性 3: 图片文件识别正确性
*对于任何*文件名，如果其扩展名为 .jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff（不区分大小写），则应被识别为图片文件
**验证: 需求 2.1**

### 属性 4: 非图片文件跳过
*对于任何*不是支持格式的文件，扫描结果中不应包含该文件
**验证: 需求 2.2**

### 属性 5: 完整路径记录
*对于任何*被识别的图片文件，扫描结果应包含该文件的完整绝对路径
**验证: 需求 2.3**

### 属性 6: 文件计数准确性
*对于任何*扫描操作，报告的图片文件总数应等于实际找到的图片文件数量
**验证: 需求 2.4**

### 属性 7: 哈希计算一致性
*对于任何*文件，多次计算其哈希值应得到相同的结果
**验证: 需求 3.1**

### 属性 8: 相同内容识别为重复
*对于任何*两个内容完全相同的文件，无论文件名是否相同，它们应该具有相同的哈希值并被标记为重复
**验证: 需求 3.2, 3.3**

### 属性 9: 重复组完整性
*对于任何*扫描结果，所有具有相同哈希值的文件应该被分组在同一个重复组中
**验证: 需求 4.1**

### 属性 10: 重复组信息完整性
*对于任何*重复组的显示输出，应包含组编号、文件数量、每个文件的完整路径和文件大小
**验证: 需求 4.2, 4.3**

### 属性 11: 文件路径排序
*对于任何*重复组，组内文件应按路径字母顺序排列
**验证: 需求 4.5**

### 属性 12: 删除确认流程
*对于任何*删除操作，在实际删除文件之前必须经过用户确认步骤
**验证: 需求 5.3, 6.1**

### 属性 13: 删除操作正确性
*对于任何*确认的删除操作，所有选定的文件应被删除，未选定的文件应保持不变
**验证: 需求 5.4**

### 属性 14: 删除结果报告准确性
*对于任何*删除操作，报告的成功删除数量和失败数量之和应等于尝试删除的文件总数
**验证: 需求 5.5**

### 属性 15: 取消操作安全性
*对于任何*取消的删除操作，所有文件应保持不变，没有文件被删除
**验证: 需求 6.2**

### 属性 16: 删除失败处理
*对于任何*删除失败的文件，系统应记录失败原因并继续处理其他文件
**验证: 需求 6.3**

### 属性 17: 重复组保留不变量
*对于任何*删除操作，每个重复组至少保留一个文件
**验证: 需求 6.4**

### 属性 18: 哈希缓存一致性
*对于任何*文件，如果其内容未改变，从缓存获取的哈希值应与重新计算的哈希值相同
**验证: 需求 7.2**

### 属性 19: 无效输入错误处理
*对于任何*无效的用户输入，系统应显示错误提示并允许用户重新输入
**验证: 需求 8.3**

### 属性 20: 操作结果摘要完整性
*对于任何*完成的操作，系统应显示包含关键统计信息的结果摘要
**验证: 需求 8.4**

## 错误处理

### 文件系统错误

1. **路径不存在**
   - 检测: 使用 `os.path.exists()` 验证
   - 处理: 显示友好错误消息，提示用户重新输入
   - 恢复: 循环提示直到获得有效路径

2. **权限不足**
   - 检测: 捕获 `PermissionError` 异常
   - 处理: 记录无法访问的路径，继续处理其他文件
   - 恢复: 在最终报告中列出跳过的文件

3. **文件被占用**
   - 检测: 捕获删除时的 `OSError` 异常
   - 处理: 将文件标记为删除失败，记录原因
   - 恢复: 继续删除其他文件

4. **磁盘空间不足**
   - 检测: 捕获 `IOError` 异常
   - 处理: 停止操作，显示错误消息
   - 恢复: 回滚已删除的文件（如果可能）

### 数据完整性错误

1. **文件在扫描后被删除**
   - 检测: 在计算哈希时捕获 `FileNotFoundError`
   - 处理: 跳过该文件，记录警告
   - 恢复: 继续处理其他文件

2. **文件在扫描后被修改**
   - 检测: 比较文件修改时间
   - 处理: 重新计算哈希值
   - 恢复: 使用最新的哈希值

3. **哈希计算失败**
   - 检测: 捕获读取文件时的异常
   - 处理: 记录错误，跳过该文件
   - 恢复: 继续处理其他文件

### 用户输入错误

1. **无效的菜单选项**
   - 检测: 验证输入是否在有效选项范围内
   - 处理: 显示错误提示和有效选项列表
   - 恢复: 重新显示菜单，等待新输入

2. **空输入**
   - 检测: 检查输入字符串是否为空或仅包含空白
   - 处理: 显示提示消息
   - 恢复: 重新提示用户输入

3. **中断操作 (Ctrl+C)**
   - 检测: 捕获 `KeyboardInterrupt` 异常
   - 处理: 显示确认消息，询问是否真的要退出
   - 恢复: 根据用户选择继续或退出

### 错误日志

所有错误应记录到日志文件中，包含：
- 时间戳
- 错误类型
- 错误消息
- 相关文件路径（如果适用）
- 堆栈跟踪（对于意外错误）

日志文件位置: `~/.image-deduplicator/error.log`

## 测试策略

### 单元测试

使用 `pytest` 框架进行单元测试，覆盖以下方面：

1. **FileScanner 测试**
   - 测试识别支持的图片格式
   - 测试跳过非图片文件
   - 测试递归扫描子文件夹
   - 测试处理空文件夹
   - 测试处理权限错误

2. **FileHasher 测试**
   - 测试 SHA-256 哈希计算正确性
   - 测试缓存机制
   - 测试处理大文件
   - 测试处理文件读取错误

3. **DuplicateDetector 测试**
   - 测试正确分组相同哈希的文件
   - 测试处理无重复的情况
   - 测试文件排序

4. **FileDeleter 测试**
   - 测试各种删除策略
   - 测试确保每组保留至少一个文件
   - 测试处理删除失败
   - 测试 dry-run 模式

5. **数据模型测试**
   - 测试 ImageFile 验证
   - 测试 DuplicateGroup 验证和属性
   - 测试 ScanResult 统计计算

### 基于属性的测试

使用 `hypothesis` 库进行基于属性的测试，每个测试至少运行 100 次迭代。

**重要**: 每个基于属性的测试必须使用以下格式标记其对应的设计文档中的正确性属性：
`# Feature: image-deduplicator, Property {number}: {property_text}`

1. **属性测试 1: 路径验证正确性**
   - 生成随机路径（有效和无效）
   - 验证验证函数的返回值正确性
   - 标记: `# Feature: image-deduplicator, Property 1: 路径验证正确性`

2. **属性测试 2: 递归扫描完整性**
   - 生成随机文件夹结构
   - 验证所有文件都被访问
   - 标记: `# Feature: image-deduplicator, Property 2: 递归扫描完整性`

3. **属性测试 3: 图片文件识别正确性**
   - 生成随机文件名和扩展名
   - 验证识别函数的正确性
   - 标记: `# Feature: image-deduplicator, Property 3: 图片文件识别正确性`

4. **属性测试 7: 哈希计算一致性**
   - 生成随机文件内容
   - 多次计算哈希，验证结果一致
   - 标记: `# Feature: image-deduplicator, Property 7: 哈希计算一致性`

5. **属性测试 8: 相同内容识别为重复**
   - 生成相同内容但不同名称的文件
   - 验证它们被识别为重复
   - 标记: `# Feature: image-deduplicator, Property 8: 相同内容识别为重复`

6. **属性测试 11: 文件路径排序**
   - 生成随机路径的重复文件
   - 验证排序正确性
   - 标记: `# Feature: image-deduplicator, Property 11: 文件路径排序`

7. **属性测试 13: 删除操作正确性**
   - 生成随机文件集和删除选择
   - 验证删除结果正确
   - 标记: `# Feature: image-deduplicator, Property 13: 删除操作正确性`

8. **属性测试 17: 重复组保留不变量**
   - 生成随机重复组和删除策略
   - 验证每组至少保留一个文件
   - 标记: `# Feature: image-deduplicator, Property 17: 重复组保留不变量`

9. **属性测试 18: 哈希缓存一致性**
   - 生成随机文件
   - 验证缓存和重新计算的哈希值相同
   - 标记: `# Feature: image-deduplicator, Property 18: 哈希缓存一致性`

### 集成测试

1. **端到端工作流测试**
   - 创建测试文件夹结构
   - 运行完整的扫描和删除流程
   - 验证最终结果

2. **大规模测试**
   - 测试处理 1000+ 文件的性能
   - 验证内存使用合理
   - 验证进度报告准确

3. **边界情况测试**
   - 空文件夹
   - 只有一个文件
   - 所有文件都重复
   - 没有重复文件
   - 非常大的文件（>100MB）

### 测试数据

使用以下方法生成测试数据：

1. **真实图片文件**: 使用 PIL/Pillow 生成小型测试图片
2. **临时文件夹**: 使用 `tempfile` 模块创建临时测试环境
3. **模拟文件系统**: 使用 `pyfakefs` 进行文件系统操作测试

### 测试覆盖率

目标代码覆盖率: 90%+

使用 `pytest-cov` 生成覆盖率报告：
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

## 性能考虑

### 哈希计算优化

1. **流式读取**: 使用 8KB 块大小读取文件，避免一次性加载大文件到内存
2. **并行处理**: 对于多核系统，可以使用 `multiprocessing` 并行计算多个文件的哈希
3. **缓存机制**: 缓存已计算的哈希值，避免重复计算

### 内存管理

1. **生成器模式**: 使用生成器遍历文件，而不是一次性加载所有文件路径
2. **增量处理**: 分批处理文件，避免内存溢出
3. **及时释放**: 处理完文件后立即释放相关资源

### 磁盘 I/O 优化

1. **批量操作**: 批量删除文件，减少系统调用次数
2. **顺序访问**: 尽可能按文件系统顺序访问文件
3. **缓冲区大小**: 使用合适的缓冲区大小平衡速度和内存

### 性能指标

- 扫描速度: 至少 100 个文件/10秒
- 哈希计算: 至少 10MB/秒
- 内存使用: 处理 1000 个文件时不超过 100MB
- 响应时间: UI 操作响应时间 < 100ms

## 安全考虑

### 文件删除安全

1. **确认机制**: 多重确认，防止误删
2. **Dry-run 模式**: 先预览将要删除的文件
3. **日志记录**: 记录所有删除操作，便于审计

### 路径安全

1. **路径验证**: 验证路径不包含危险字符
2. **符号链接处理**: 正确处理符号链接，避免删除链接目标
3. **权限检查**: 在操作前检查文件权限

### 数据隐私

1. **本地处理**: 所有操作在本地进行，不上传任何数据
2. **临时文件清理**: 及时清理临时文件和缓存
3. **日志脱敏**: 日志中不包含敏感路径信息（可选）

## 依赖项

### 核心依赖

- Python 3.8+
- 标准库: `os`, `pathlib`, `hashlib`, `dataclasses`, `enum`, `typing`

### 测试依赖

- `pytest` >= 7.0: 测试框架
- `hypothesis` >= 6.0: 基于属性的测试
- `pytest-cov` >= 4.0: 代码覆盖率
- `pyfakefs` >= 5.0: 文件系统模拟

### 可选依赖

- `Pillow` >= 9.0: 生成测试图片
- `tqdm` >= 4.0: 进度条显示
- `colorama` >= 0.4: 彩色终端输出

## 部署和使用

### 安装

```bash
pip install image-deduplicator
```

或从源码安装：
```bash
git clone https://github.com/user/image-deduplicator.git
cd image-deduplicator
pip install -e .
```

### 使用方式

```bash
# 基本使用
image-deduplicator

# 指定文件夹
image-deduplicator --folder /path/to/images

# Dry-run 模式（不实际删除）
image-deduplicator --dry-run

# 自动删除（保留第一个）
image-deduplicator --auto keep-first
```

### 配置文件

可选的配置文件位于 `~/.image-deduplicator/config.json`:

```json
{
  "supported_extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"],
  "chunk_size": 8192,
  "default_strategy": "keep_first",
  "enable_cache": true,
  "log_level": "INFO"
}
```

## 未来扩展

### 可能的功能增强

1. **图像相似度检测**: 使用感知哈希检测相似但不完全相同的图片
2. **GUI 界面**: 提供图形用户界面
3. **批量处理**: 支持同时处理多个文件夹
4. **云存储支持**: 支持扫描云存储（如 Google Drive, Dropbox）
5. **智能保留策略**: 根据图片质量、分辨率等自动选择保留哪个文件
6. **撤销功能**: 支持撤销删除操作
7. **报告导出**: 导出扫描报告为 CSV 或 JSON 格式

### 架构扩展性

当前架构支持以下扩展：

1. **插件系统**: 可以添加自定义的删除策略
2. **存储后端**: 可以替换文件系统操作为其他存储后端
3. **哈希算法**: 可以支持其他哈希算法（如 MD5, Blake2）
4. **输出格式**: 可以添加其他输出格式（JSON, XML）
