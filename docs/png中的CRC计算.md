#  png中CRC计算--9.29
## 关于CRC



## 数据块结构
|名称|长度|作用|
| ---| --- |--- |
|Length|4 bytes|指定Chunk Data的长度|
|Chunk Type|4 bytes|指定数据块类型|
|Chunk Data|由Length指定|按照Chunk Type存放指定数据|
|CRC|4 bytes|检查是否有错误的循环冗余代码| 
## crc32
```python
from zlib import crc32

crc = crc32(bytes, value)
# png中 bytes 取数据块的Chunk Type和Chunk Data，value 取 0
```
