# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_bingimagecreator']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-bingimagecreator',
    'version': '0.1.0',
    'description': 'A nonebot plugin for Bing DALL-E 3',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-BingImageCreator\n</div>\n\n# 介绍\n- 本插件调用Bing的绘图接口，仅需提供Bing的cookies即可调用DALL-E 3进行绘图。\n- 本插件支持多cookies和代理设置。\n- 在不支持NewBing的地区请设置代理。\n-  核心代码来源于[BingImageCreator](https://github.com/abersheeran/BingImageCreator)\n# 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot_plugin_BingImageCreator.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-BingImageCreator"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-BingImageCreator\n  ```\n\n# 配置文件\n\n在Bot根目录下的.env文件中追加如下内容：\n\n```\nbing_cookies = ["cookies1","cookies2","cookies3",......]\n```\n\n可选内容：\n```\nbing_proxy = "http://127.0.0.1:8001"    # 无法访问NewBing的地区请配置此项\n```\ncookies获取方法参考[此处](https://github.com/acheong08/BingImageCreator#chromium-based-browsers-edge-opera-vivaldi-brave)\n\n# 使用方法\n\n- 直接发送: 画图 XXXXXX\n',
    'author': 'Alpaca',
    'author_email': 'alpaca@bupt.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
