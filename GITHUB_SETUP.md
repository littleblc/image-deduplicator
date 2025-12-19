# GitHub 仓库设置指南

## 步骤 1: 初始化本地 Git 仓库

在项目目录中运行以下命令：

```bash
# 初始化 git 仓库
git init

# 添加所有文件
git add .

# 创建第一次提交
git commit -m "Initial commit: Image Deduplicator v0.1.0"
```

## 步骤 2: 在 GitHub 上创建新仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `image-deduplicator`
   - **Description**: `图片去重工具 - 扫描并删除重复的图片文件`
   - **Visibility**: 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）
   - **不要**添加 .gitignore（我们已经有了）
   - **不要**选择 license（我们已经有了）

3. 点击 "Create repository"

## 步骤 3: 连接本地仓库到 GitHub

GitHub 会显示一些命令，或者你可以使用以下命令（替换 `YOUR_USERNAME` 为你的 GitHub 用户名）：

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/image-deduplicator.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 步骤 4: 验证推送成功

访问你的仓库页面：
```
https://github.com/YOUR_USERNAME/image-deduplicator
```

你应该能看到所有文件和 README。

## 步骤 5: 更新文档中的链接

推送成功后，更新以下文件中的占位符链接：

### USAGE.md
将所有 `YOUR_USERNAME` 替换为你的实际 GitHub 用户名

### design.md
更新安装部分的 git clone 命令

### README.md
如果需要，添加仓库链接

可以使用以下命令批量替换（替换 `YOUR_USERNAME`）：

```bash
# Windows PowerShell
(Get-Content USAGE.md) -replace 'YOUR_USERNAME', '你的用户名' | Set-Content USAGE.md
(Get-Content .kiro/specs/image-deduplicator/design.md) -replace 'YOUR_USERNAME', '你的用户名' | Set-Content .kiro/specs/image-deduplicator/design.md

# 然后提交更新
git add .
git commit -m "Update repository links with actual GitHub username"
git push
```

## 可选：添加 GitHub Actions（CI/CD）

创建 `.github/workflows/test.yml` 文件来自动运行测试：

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[test]"
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=term
```

## 可选：添加 README 徽章

在 README.md 顶部添加状态徽章：

```markdown
# Image Deduplicator

[![Tests](https://github.com/YOUR_USERNAME/image-deduplicator/workflows/Tests/badge.svg)](https://github.com/YOUR_USERNAME/image-deduplicator/actions)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

## 故障排除

### 如果推送被拒绝

```bash
# 强制推送（仅在确定本地版本正确时使用）
git push -f origin main
```

### 如果需要更改远程 URL

```bash
# 查看当前远程 URL
git remote -v

# 更改远程 URL
git remote set-url origin https://github.com/YOUR_USERNAME/image-deduplicator.git
```

### 如果需要使用 SSH 而不是 HTTPS

```bash
# 更改为 SSH URL
git remote set-url origin git@github.com:YOUR_USERNAME/image-deduplicator.git
```

## 完成！

现在你的项目已经在 GitHub 上了！你可以：
- 分享仓库链接
- 接受贡献（Pull Requests）
- 使用 GitHub Issues 跟踪问题
- 使用 GitHub Actions 自动化测试
