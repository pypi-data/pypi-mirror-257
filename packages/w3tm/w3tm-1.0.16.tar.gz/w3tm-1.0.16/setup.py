from setuptools import setup

# 读取README文件
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='w3tm',
    version='1.0.16',
    description='W3TM command line tool',
    # 项目介绍
    long_description=long_description,
    long_description_content_type='text/markdown',  # 或者 'text/x-rst' 如果使用reStructuredText
    author='alexzshl',
    author_email='alexzshl@126.com',
    include_package_data=True,
    # packages=find_packages(),
    entry_points={
        'console_scripts': [
            'w3tm = main:main'
        ]
    },
    #data_files=[('Scripts', ['BLPConverter.exe'])],
    install_requires=[
        # 这里列出你的项目依赖
        'pillow~=10.2.0',
        'argparse~=1.4.0'
    ],
)