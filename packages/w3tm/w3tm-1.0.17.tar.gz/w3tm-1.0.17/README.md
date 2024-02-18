# intro
W3TM is a simple command line tool to merge war3 terian images to a single png file

# install

```shell
pip install w3tm
```

# usage

```text
usage: w3tm [-h] [-o OUTPUT] [-v] input

W3TM command line tool

positional arguments:
  input                 输入文件夹

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        输出文件名称(默认:result.png)
  -v, --version         show program's version number and exit

示例:
  w3tm -h
  w3tm  D:\game\MPQMaster\w3x.mpq\TerrainArt\LordaeronFall
  w3tm -o test.png D:\game\MPQMaster\w3x.mpq\TerrainArt\LordaeronFall
```