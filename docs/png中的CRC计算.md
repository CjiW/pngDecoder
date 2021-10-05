#  png中CRC计算--9.29

## crc32
```python
from zlib import crc32

crc = crc32(bytes, value)
# png中 bytes 取数据块的type和data，value 取 0
```
