from setuptools import setup

setup(
    name='w3tm',
    version='1.0.13',
    description='W3TM command line tool',
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