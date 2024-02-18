#打包命令:python setup.py sdist
from setuptools import setup
setup(
    name='GetPcInfo',  # 模块的名称
    version='2.0',           # 版本号
    packages=['.'],          # 模块所在的包
    description='GetPcInfo',  # 模块的简要描述
    author='pythonking',      # 作者名字
    author_email='youremail@none.com',     # 作者邮箱
    url='https://No.com',  # 模块的URL
)