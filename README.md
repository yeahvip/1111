# PDF 解析服务

本项目是一个 Python Flask Web 服务，用于解析 PDF 文件。它能够提取文本内容、识别和提取表格数据，以及从图片中提取文字（OCR）。

## 功能

- 提取 PDF 中的纯文本。
- 从 PDF 中识别和提取表格。
- 从 PDF 中提取图片，并使用 Tesseract OCR 从图片中提取文本。
- 提供一个 HTTP API 端点 `/parse_pdf` 用于上传和处理 PDF 文件。

## 系统依赖

在运行此服务之前，你需要安装以下系统级依赖：

- **Tesseract OCR**: 用于图像文字识别。
  ```bash
  # 对于 Debian/Ubuntu:
  sudo apt-get update
  sudo apt-get install -y tesseract-ocr
  # 对于 macOS (使用 Homebrew):
  # brew install tesseract
  ```
- **Ghostscript**: `camelot-py` (用于表格提取) 的依赖。
  ```bash
  # 对于 Debian/Ubuntu:
  sudo apt-get install -y ghostscript
  # 对于 macOS (使用 Homebrew):
  # brew install ghostscript
  ```
- **Tk**: `camelot-py` 的另一个依赖 (通常与 Python 一起安装，但有时需要显式安装开发包)。
   ```bash
   # 对于 Debian/Ubuntu:
   sudo apt-get install -y tk tk-dev
   # 对于 macOS: 通常通过安装 Python 来解决
   ```

## 安装

1.  **克隆仓库 (如果适用)**
    ```bash
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **创建并激活 Python 虚拟环境** (推荐)
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate   # Windows
    ```

3.  **安装 Python 依赖**
    ```bash
    pip install -r requirements.txt
    ```

## 运行服务

执行以下命令来启动 Flask 开发服务器：

```bash
python app.py
```

服务默认会在 `http://0.0.0.0:5000` 上运行。
你可以通过浏览器或 API 工具访问 `http://localhost:5000/parse_pdf` (尽管这是一个 POST 端点，直接在浏览器中打开不会有太大作用)。

## API 使用

### 端点: `POST /parse_pdf`

用于上传 PDF 文件并获取解析结果。

**请求:**

-   **方法:** `POST`
-   **URL:** `http://localhost:5000/parse_pdf`
-   **Body:** `multipart/form-data`
    -   `file`: (必需) 要上传的 PDF 文件。

**示例 (使用 curl):**

```bash
curl -X POST -F "file=@/path/to/your/sample.pdf" http://localhost:5000/parse_pdf
```
将 `/path/to/your/sample.pdf` 替换为你本地 PDF 文件的实际路径。

**成功响应 (200 OK):**

响应为一个 JSON 对象，包含以下字段：

-   `filename`: (字符串) 上传的原始文件名。
-   `text`: (字符串) 从 PDF 中提取的全部文本内容。如果提取失败或无文本，可能为 `null` 或空字符串。
-   `tables`: (列表) 从 PDF 中提取的表格列表。每个表格是一个二维列表 (列表的列表，代表行和单元格)。如果未找到表格或提取失败，可能为空列表。
-   `image_ocr_results`: (列表) 从 PDF 中的图片提取的 OCR 结果列表。每个元素是一个对象，包含：
    -   `image_path`: (字符串) 提取的图片文件名 (主要用于标识，实际文件是临时的)。
    -   `text`: (字符串) 从该图片中 OCR 得到的文本。如果OCR失败或图片不含文字，文本可能为空。
    如果提取图像或OCR时出错，此字段可能包含错误信息对象。

**示例 JSON 响应:**
```json
{
  "filename": "my_document.pdf",
  "image_ocr_results": [
    {
      "image_path": "img_b1f7b7c3-fb38-4061-a311-784719e989b1_page_1_image_0.png",
      "text": "这是从图片中识别的文字。"
    }
  ],
  "tables": [
    [
      ["表头1", "表头2", "表头3"],
      ["数据1A", "数据1B", "数据1C"],
      ["数据2A", "数据2B", "数据2C"]
    ]
  ],
  "text": "这是PDF中的一些示例文本。\n下一页包含一个表格和一张图片。\n..."
}
```

**错误响应:**

-   `400 Bad Request`: 如果请求无效 (例如，没有文件，文件类型不支持，文件过大等)。
    ```json
    {
      "error": "No file part in the request"
    }
    ```
-   `500 Internal Server Error`: 如果在处理 PDF 过程中发生服务器内部错误。
    ```json
    {
      "error": "An error occurred while processing the PDF: [具体错误信息]"
    }
    ```

## 项目结构

```
.
├── app.py               # Flask 应用主文件，包含 API 端点
├── pdf_parser.py        # PDF 解析核心逻辑模块
├── requirements.txt     # Python 依赖列表
└── README.md            # 本文档
```

## 注意事项
- **表格提取**: `camelot-py` 提供了两种表格提取策略：`lattice` (适用于有清晰线条的表格) 和 `stream` (适用于没有线条的表格)。`pdf_parser.py` 目前首先尝试 `lattice`，如果效果不佳或未找到表格，则会尝试 `stream`。您可能需要根据 PDF 的具体情况调整这些参数或 `camelot` 的其他高级设置（如 `line_scale`, `edge_tol` 等）以获得最佳效果。
- **OCR 准确性**: OCR 的准确性高度依赖于 PDF 中图像的质量、分辨率、字体以及 Tesseract OCR 引擎的能力。对于扫描质量差或包含复杂背景/字体的图像，效果可能不佳。
- **性能**: 处理大型或结构复杂的 PDF 文件可能会消耗较多时间和内存。服务配置了 `MAX_CONTENT_LENGTH` (默认为 16MB) 来限制上传文件的大小。
- **临时文件**: 服务在处理过程中使用临时文件存储上传的 PDF 和从 PDF 中提取的图像。这些临时文件在请求处理完成后会自动清理。
- **并发性**: 当前的 Flask 开发服务器是单线程的。对于生产环境，应使用生产级 WSGI 服务器（如 Gunicorn 或 uWSGI）来运行应用，以支持并发请求。
```
