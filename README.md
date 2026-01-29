# 济南天气数据可视化分析系统 (Jinan Weather Visualization)

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Flask](https://img.shields.io/badge/Framework-Flask-green) ![Plotly](https://img.shields.io/badge/Visualization-Plotly-orange)

## 📖 项目介绍 (Introduction)
该项目基于 **济南市 2015-2024 年天气数据（3000+条）**，构建了一个基于 Web 的数据可视化应用。系统使用 **Flask** 作为后端框架，结合 **Pandas** 进行数据清洗与处理，并利用 **Plotly** 实现动态、交互式的图表展示。用户可以通过浏览器查看济南市近十年的气温变化趋势、特定日期（10月31日）的温度变化、年度极值对比以及天气类型分布。

## 🛠️ 技术栈 (Tech Stack)

* **开发环境**: PyCharm 2025.1
* **编程语言**: Python 3.12
* **Web 框架**: Flask
* **数据处理**: Pandas (读取/清洗/日期处理), re (字符串处理)
* **数据可视化**: Plotly (支持动态交互与下拉菜单)
* **前端技术**: HTML5, CSS3, JavaScript (Main.js 调用 Plotly)

## 📊 功能展示 (Features)

本项目包含五个主要的可视化图表，通过前端页面进行交互展示：

1.  **济南市 2015-2024 年温度变化趋势 (折线图)**
    * 展示主要时间段内的最高温与最低温走势。
    * *分析*: 观察到近十年来最高温度有逐渐上升的趋势，温室效应日益明显。

2.  **10月31日历史温度变化 (折线图)**
    * 筛选每年 10 月 31 日（作者生日）的数据进行特定展示。
    * *分析*: 展示特定日期在不同年份的温度波动情况。

3.  **年度最高/最低温度对比 (柱状图)**
    * 计算并展示每一年的年度最高温和最低温。
    * *分析*: 极端温度（最高和最低）均呈现逐年攀升的趋势。

4.  **2024年白天天气分布 (扇形图)**
    * 统计并展示 2024 年全年的白天天气类型占比。
    * *分析*: 晴天居多 (40-45%)，其次是多云。

5.  **2024年夜间天气分布 (扇形图)**
    * 统计并展示 2024 年全年的夜间天气类型占比。
    * *分析*: 夜间阴天的情况显著多于白天。

## 📂 项目结构 (Project Structure)

```text
├── data/
│   └── jinan_weather_2015_2024.csv  # 原始天气数据源
├── static/
│   ├── css/
│   │   └── style.css                # 页面样式定义
│   └── js/
│       └── main.js                  # 调用 Plotly.js 函数绘制图表
├── templates/
│   └── index.html                   # 用户界面容器
├── app.py                           # Flask 应用主程序
├── requirements.txt                 # 项目依赖
└── README.md                        # 项目说明文档
```

## 🚀 快速开始 (Quick Start)

如果您想在本地运行本项目，请按照以下步骤操作：

1.  **环境准备**
    * 确保已安装 **Python 3.12**。
    * 推荐使用 **PyCharm 2025.1** 或其他代码编辑器打开项目根目录。

2.  **安装依赖库**
    本项目依赖 Flask 进行 Web 服务，Pandas 进行数据处理，Plotly 进行可视化。请在终端运行以下命令安装：
    ```bash
    pip install flask pandas plotly
    ```

3.  **检查数据文件**
    确保项目目录中包含数据文件：`data/jinan_weather_2015_2024.csv`。

4.  **运行应用**
    在终端中运行以下命令启动项目：
    ```bash
    python app.py
    ```
    
5.  **访问页面**
    程序启动后，打开浏览器访问终端显示的本地地址（通常为 `http://127.0.0.1:5000`），即可看到数据可视化大屏。
