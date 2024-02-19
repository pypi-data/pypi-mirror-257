from setuptools import setup

# 读取README文件
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='w3tm',
    version='1.0.19',
    description='W3TM command line tool',
    # 项目介绍
    long_description=long_description,
    long_description_content_type='text/markdown',  # 或者 'text/x-rst' 如果使用reStructuredText
    classifiers=[
        'Development Status :: 3 - Alpha',  # 开发状态
        'Intended Audience :: Developers',  # 目标用户
        'Topic :: Software Development :: Build Tools',  # 主题
        'Topic :: Games/Entertainment',  # 主题
        'License :: OSI Approved :: MIT License',  # 许可证
        'Programming Language :: Python :: 3',  # 编程语言和版本
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
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