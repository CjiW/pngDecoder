# 文件头  
## 长度   
  8 字节  
## 值与含义  
|十六进制值|含义|
|---|---|
|89|检测环境是否支持八位编码，并且大于ASCII最大值，可以避免被识别为文本文件|
|50 4e 47|在 ASCII 中对应 PNG 三个字母，方便被文本编辑器识别|
|0d 0a|CRLF 换行符；0d代表 ASCII 13，即\r，CR；0a代表ASCII 10，即\n，LF|
|1a|在 DOS 系统下标志文件类型的结束|
|0a|同上即\n，LF|

# 数据块  
## 1. 关键数据块  
|名称|长度|作用|
| ---| --- |--- |
|Length|4 bytes|指定Chunk Data的长度|
|Chunk Type|4 bytes|指定数据块类型|
|Chunk Data|由Length指定|按照Chunk Type存放指定数据|
|CRC|4 bytes|检查是否有错误的循环冗余代码|  
> 由此：每一数据块长度为 ** Length值 + 12 bytes **  

   ### 数据块一（共13bytes）：IHDR  -- 文件头数据块  
  |域|长度|含义|
  |--|--|--|
  |Width|4 bytes|图片宽度（像素）|
  |Height|4 bytes|图片高度（像素）|
  |Bit Depth|1 byte|图像深度|
  |Color Type|1 byte|颜色类型|
  |Compression Method|1 byte|压缩算法|
  |Filter Method|1 byte|滤波方法|
  |Interlace Method|1 byte|扫描方法|

  #### 关于Color Type
  |Color Type|可能的Bit Depth|说明|
  |--|--|--|
  |0（000）|1，2，4，8，16|灰度|
  |2（010）|8，16|RGB|
  |3（011）|1，2，4，8|索引色|
  |4（100）|8，16|有Alpha通道的灰度|
  |6（110）|8，16|RGBA|  


   ### 数据块二(3 ~ 768 bytes)：PLTE
   - 数据块三：IDAT
   - 数据块四：IEND
## 2. 辅助数据块  
|符号|说明|
|--|--|
|bKGD|指定默认的背景颜色|
|cHRM|校准色度|
|dSIG|数字签名|
|eXIf|Exif metadata 信息|
|gAMA|指定亮度的伽马校准值|
|hIST|色彩直方图，估算颜色的使用频率|
|iCCP|ICC color profile|
|iTXt|以键值对方式存储可能的压缩文本和翻译信息|
|pHYs|指定像素大小或图片比例|
|sBIT|除了指定位深度（8，16 等等）外，保存原始数据以便恢复|
|sPLT|提出建议使用的调色板，可能有多个|
|sRGB|指明是否使用sRGB color space|
|sTER|储存立体视图（stereoscopic）的相关信息|
|tEXt|保存作者等键值对的文本信息|
|tIME|上次修改时间|
|tRNS|保存透明信息，分为不透明、全透明、Alpha|
|zTXt|保存压缩后的文本信息以及对应的压缩方式标识|
