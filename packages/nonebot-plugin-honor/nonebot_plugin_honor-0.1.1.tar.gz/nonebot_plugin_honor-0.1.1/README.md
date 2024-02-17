<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://ghproxy.com/https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://ghproxy.com/https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-honor

_✨ 在机器人内轻松查询王者荣耀英雄的各分段胜率，数据来源苏苏的荣耀助手 ✨_

<a href="https://raw.githubusercontent.com/nonebot/nonebot2/master/LICENSE">
    <img src="https://img.shields.io/github/license/forchannot/nonebot_plugin_honor" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-rename">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-honor.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-yellow.svg" alt="python">

</div>

<!-- TOC -->
- [nonebot-plugin-honor](#nonebot-plugin-honor)
  - [📖简介](#简介)
  - [🔐许可](#许可)
  - [💿 安装方法](#-安装方法)
  - [🏷️插件命令](#️插件命令)
  - [⚙️插件配置项](#️插件配置项)

## 📖简介

在机器人内轻松查询王者荣耀英雄的各分段胜率，数据来源苏苏的荣耀助手

## 🔐许可

[MIT](https://github.com/forchannot/nonebot-plugin-honor/blob/main/LICENSE)

## 💿 安装方法

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-honor
</details>

<details>
<summary>pip</summary>

    pip install nonebot-plugin-honor

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_honor"]

```
[tool.nonebot]
plugins = []
plugin_dirs = ["src/plugins"]
```
</details>



## 🏷️插件命令

`honor [英雄名称]`，支持别名{"查胜率", "英雄胜率"}

## ⚙️插件配置项

暂无
