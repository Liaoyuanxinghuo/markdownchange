# MarkdownChanger

将Markdown文件中的本地图片转换为Base64编码，使Markdown文件可以独立使用，无需额外图片文件。

## 功能特点

- 支持单个Markdown文件处理
- 支持批量处理文件夹中的所有Markdown文件
- 自动识别并转换本地图片（PNG、JPG、JPEG、GIF、BMP、WEBP）
- 忽略网络图片链接
- 转换后的文件自动命名为 `原文件名-base64.md`
- 简洁美观的图形化界面

## 使用方法

### 直接运行Python脚本

1. 确保已安装Python 3.7或更高版本
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行程序：
   ```bash
   python markdown_changer.py
   ```

### 构建EXE文件

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行构建脚本：
   ```bash
   build.bat
   ```
3. 构建完成后，可执行文件位于 `dist\MarkdownChanger.exe`

## 界面说明

1. **选择文件夹**：选择包含Markdown文件的文件夹，将处理该文件夹下所有的.md文件
2. **选择文件**：选择单个Markdown文件进行处理
3. **开始转化**：点击按钮开始转换处理
4. **日志窗口**：显示处理进度和结果

## 注意事项

- 转换后的文件会自动命名为 `原文件名-base64.md`
- 网络图片链接不会被转换
- 原始文件不会被修改
- Base64编码会增加文件大小，建议仅对小图片使用
