# 亚马逊ASIN监控系统（商品信息、可售状态与链接状态）

本项目用于批量监控亚马逊 ASIN 页面信息，聚焦以下三类结果：

- 商品信息（如标题、五点描述、核心参数等）
- 可售状态（如是否可售、是否缺货等）
- 链接状态（如链接是否可访问、是否失效）

当前核心脚本位于 `ASIN_gen` 目录，适合用于日常巡检、竞品跟踪和数据留档。

## 功能概览

- 批量读取 `urls.txt` 中的商品链接并抓取页面数据
- 提取商品核心字段并输出结构化结果
- 记录可售状态与链接状态，便于后续筛查
- 导出 Excel 结果文件用于分析与汇总

## 目录结构

```text
ASIN/
├─ ASIN_gen/
│  ├─ ASIN_crawler.py        # 主爬虫脚本
│  ├─ cookie_get.py          # cookie/鉴权辅助脚本
│  ├─ urls.txt               # 待抓取链接列表（每行一个）
│  ├─ .gitignore             # 忽略敏感信息和生成文件
│  ├─ auth_us.json           # 本地鉴权文件（已忽略，不上传）
│  └─ Amazon_Monitor_us.xlsx # 生成结果文件（已忽略，不上传）
├─ UK/
└─ US/
```

## 环境要求

- Python 3.9 及以上版本
- 建议安装常用依赖（按实际代码导入为准）：
  - `requests`
  - `pandas`
  - `openpyxl`

示例安装命令：

```bash
pip install requests pandas openpyxl
```

## 使用方法

1. 在 `ASIN_gen/urls.txt` 中准备待监控商品链接（每行一个 URL）
2. 准备本地 cookie/鉴权信息（例如 `auth_us.json`，仅本地使用）
3. 执行主脚本：

```bash
python ASIN_gen/ASIN_crawler.py
```

4. 在 `ASIN_gen` 下查看生成的 Excel 结果文件

## 输入与输出

- 输入：
  - `ASIN_gen/urls.txt`（监控链接列表）
  - 本地鉴权信息（如 `auth_us.json`）
- 输出：
  - 监控结果 Excel（如 `Amazon_Monitor_us.xlsx`）

## 数据安全与提交规范

为避免泄露敏感信息，仓库已忽略以下内容：

- `ASIN_gen/auth_us.json`
- `ASIN_gen/*.xlsx`

请勿提交 cookie、账号凭据及业务敏感数据。

## 免责声明

本项目仅用于内部业务分析与研究用途。实际使用时请遵守目标平台条款、当地法律法规及公司合规要求。
