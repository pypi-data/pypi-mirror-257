from setuptools import setup, find_packages

from fakeoai import __version__

setup(
    name="fakeoai",
    version=__version__,
    packages=find_packages('fakeoai'),
    author="baobao",
    author_email="1727283040@qq.com",
    description="A Package to build ChatGPT Ofical WebSite",
    license="MIT",
    keywords="openai chatgpt",
    include_package_data=True
)
