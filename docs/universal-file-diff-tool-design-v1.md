# 通用文件对比工具设计文档（Universal File Diff Tool）

- 版本：V1.0
- 作者：项目设计方案
- 目标：实现一个支持 Word、Excel、PPT、HTML、代码、目录 的通用文件对比工具。

---

## 1. 项目目标

开发一个通用文件对比系统，支持多种文件格式的差异分析，并生成可视化报告。

### 1.1 支持文件类型

| 类型 | 支持程度 |
|---|---|
| Word (`.docx`) | 文本对比 |
| Excel (`.xlsx`) | 表格对比 |
| PPT (`.pptx`) | 文本对比 |
| HTML | 文本对比 |
| TXT | 文本对比 |
| 源代码 | 行级对比 |
| 文件夹 | 树结构对比 |

### 1.2 系统应用场景

- DevOps 版本对比
- 配置管理
- 软件发布验证
- ASPICE 项目管理
- 文档变更分析

---

## 2. 系统总体架构

```text
Web UI
   |
API层(FastAPI)
   |
--------------------------------
|         |          |         |
解析层     Diff引擎     存储层    报告生成
```

### 2.1 UI 层

**功能：**
- 上传文件
- 选择对比对象
- 查看差异结果

**技术：**
- Streamlit（初期）
- React（高级版本）

### 2.2 API 层

**职责：**
- 接收请求
- 调用解析器
- 调用 Diff 引擎
- 返回结果

**推荐框架：**
- FastAPI

**接口示例：**
- `POST /compare`

输入：`fileA`、`fileB`  
输出：`diff_result`

### 2.3 Diff 引擎

目录：`diff_engine/`

**功能：**
- 文本 Diff
- 表格 Diff
- 树结构 Diff

### 2.4 文件解析层

目录：`parsers/`

**功能：**
- 解析不同文件格式
- 转换为统一模型

**支持：**
- Word 解析
- Excel 解析
- PPT 解析
- HTML 解析
- 代码解析
- 文件夹解析

### 2.5 存储层

**用途：**
- 存储上传文件
- 存储 Diff 结果

目录：`storage/`
- `uploads/`
- `reports/`

---

## 3. 核心设计思想

核心原则：**所有文件先转换为统一数据模型，再进行对比。**

### 3.1 统一模型：`DocumentObject`

```python
class DocumentObject:
    type
    content
```

### 3.2 支持类型

| 类型 | 描述 |
|---|---|
| `text` | 文本文件 |
| `table` | 表格文件 |
| `tree` | 目录结构 |

### 3.3 示例

**文本文件：**

```json
{
  "type": "text",
  "content": ["line1", "line2"]
}
```

**Excel 文件：**

```json
{
  "type": "table",
  "rows": [["A", "B"], ["1", "2"]]
}
```

**目录结构：**

```json
{
  "type": "tree",
  "nodes": []
}
```

---

## 4. Diff 引擎设计

目录：`diff_engine/`

包含：
- `text_diff.py`
- `table_diff.py`
- `tree_diff.py`

### 4.1 文本 Diff 设计

适用：
- Word
- HTML
- TXT
- 源代码

算法：
- Myers Diff（可用 `difflib` 实现）

输出结构：
- `added`
- `deleted`
- `modified`

示例：

```text
Line 5:
Old:
speed=100

New:
speed=120
```

### 4.2 表格 Diff 设计

适用：Excel

函数：
- `compare_table(table1, table2)`

输出示例：

```text
Cell A2:
100 -> 120
```

比较方法：
- 行比较
- 列比较
- 单元格比较

高级版本：
- Key-based compare

示例：

```text
ID=1001
speed: 100 -> 120
```

### 4.3 树结构 Diff 设计

适用：
- 文件夹
- Word 结构
- HTML 结构

函数：
- `compare_tree(tree1, tree2)`

输出：
- added files
- deleted files
- changed files

示例：

```text
Added:
/doc/new.docx
```

---

## 5. 文件解析层设计

目录：`parsers/`

文件：
- `word_parser.py`
- `excel_parser.py`
- `ppt_parser.py`
- `html_parser.py`
- `code_parser.py`
- `folder_parser.py`

统一接口：
- `parse(file)`

返回：`DocumentObject`

---

## 6. Word 解析设计

文件格式：`.docx = zip + xml`

解析内容：
- 段落
- 文本
- 表格

输出：`type="text"`

示例：
- `Paragraph1`
- `Paragraph2`

高级版本支持：
- Word 结构 Diff（paragraph / table / image）

---

## 7. Excel 解析设计

解析结果：`TableObject`

结构：
- columns: A B C
- rows: `1 2 3` / `4 5 6`

支持：
- Multiple sheets（Sheet1、Sheet2）

输出：`type="table"`

---

## 8. PPT 解析设计

结构：slides

输出：`type="text"`

示例：
- Slide1 Title
- Slide1 Content

---

## 9. HTML 解析设计

方法：DOM 解析

工具：BeautifulSoup

输出：`type="text"`

内容：text nodes

高级版本：DOM diff

---

## 10. 代码 Diff 设计

方法：直接文本 Diff

推荐：
- `git diff --no-index fileA fileB`

优点：
- 成熟算法
- 工业标准

---

## 11. 文件夹 Diff 设计

支持：目录 vs 目录

示例：
- `release_v1/`
- `release_v2/`

输出：
- added files
- deleted files
- changed files

算法：
- 递归扫描
- Hash 比较

结构：`file_tree`

---

## 12. Hash 机制设计

支持：
- MD5
- SHA256

用途：
- 快速判断文件是否变化

逻辑：

```python
if hashA == hashB:
    skip diff
```

可显著提升性能。

---

## 13. API 设计

推荐：FastAPI

### 13.1 上传文件
- `POST /upload`
- 返回：`file_id`

### 13.2 文件对比
- `POST /compare`
- 输入：`fileA`、`fileB`
- 返回：`diff_result`

---

## 14. UI 设计

初级版本：Streamlit

功能：
- 上传文件 A
- 上传文件 B
- 点击 Compare
- 查看结果

显示方式：
- 左右对比（类似 Beyond Compare）

---

## 15. 报告输出设计

支持：HTML 报告

输出：`diff_report.html`

内容：
- 文件差异
- Excel 差异
- Word 差异

可供企业直接使用。

---

## 16. 存储结构设计

```text
project/
   core/
   parsers/
   diff_engine/
   api/
   ui/
   storage/
       uploads/
       reports/
```

说明：
- `core`：核心模型（如 `document_model.py`）
- `parsers`：文件解析模块
- `diff_engine`：Diff 算法模块
- `api`：FastAPI 接口
- `ui`：Web 界面
- `storage`：文件存储

---

## 17. 扩展设计

插件化结构：

```text
plugins/
   word
   excel
   ppt
   html
   code
```

未来支持：
- PDF
- XML
- JSON
- YAML

实现方式：
- 新增 parser 即可
- 无需修改核心系统

---

## 18. DevOps 集成设计

支持自动版本对比：
- 如 `release_v1` vs `release_v2`
- 自动生成 `diff_report.html`

CI 集成：
- 支持 Git commit 后自动执行 diff 并生成报告
