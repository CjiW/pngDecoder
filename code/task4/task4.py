import zlib


def myfilter(lineData_list, png_hight, png_width):
    # 处理RGB信息
    for i in range(png_hight - 1, -1, -1):
        if lineData_list[i][0] == 0:
            continue
        elif lineData_list[i][0] == 1:
            for j in range(3 * png_width, 0, -1):
                if j < 4:
                    lineData_list[i][j] -= 0
                else:
                    lineData_list[i][j] -= lineData_list[i][j - 3]
                lineData_list[i][j] %= 256

        elif lineData_list[i][0] == 2:
            for j in range(3 * png_width, 0, -1):
                lineData_list[i][j] -= lineData_list[i - 1][j]
                lineData_list[i][j] %= 256

        elif lineData_list[i][0] == 3:
            for j in range(3 * png_width, 0, -1):
                if j < 4:
                    lineData_list[i][j] -= lineData_list[i - 1][j] // 2
                else:
                    lineData_list[i][j] -= (lineData_list[i][j - 3] + lineData_list[i - 1][j]) // 2
                lineData_list[i][j] %= 256

        else:
            for j in range(3 * png_width, 0, -1):
                if j < 4:
                    a, c = 0, 0
                else:
                    a = lineData_list[i][j - 3]
                    c = lineData_list[i - 1][j - 3]
                b = lineData_list[i - 1][j]

                p = a + b - c
                min_abs = min(abs(a - p), abs(b - p), abs(c - p))
                if min_abs == abs(a - p):
                    lineData_list[i][j] -= a
                elif min_abs == abs(b - p):
                    lineData_list[i][j] -= b
                else:
                    lineData_list[i][j] -= c
                lineData_list[i][j] %= 256
    return lineData_list


f = open("./processed_Data_1", "r")
readData = f.readlines()
f.close()

unzipData = []
width = int(readData[0][:-1])
hight = int(readData[1][:-1])
for i in range(2, len(readData)):
    unzipData.append(int(readData[i][:-1]))

lineData_list = []
for i in range(0, len(unzipData), width * 3 + 1):
    lineData_list.append(unzipData[i:i + width * 3 + 1])

for xx in range(len(lineData_list)):
    for yy in range(1, len(lineData_list[0])):
        lineData_list[xx][yy] = 255 - lineData_list[xx][yy]

filterData = myfilter(lineData_list, hight, width)
alldata = []
for i in filterData:
    for j in i:
        alldata.append(j)
unzipbytes = bytearray(alldata)

zipbytes = zlib.compress(bytes(unzipbytes))

f = open("./mypng.png", "wb")
info_data2 = open("./info_data2", "rb")
info_data = open("./info_data", "rb")
f.write(info_data.read() + len(zipbytes).to_bytes(length=4, byteorder='big') + \
        b'IDAT' + zipbytes + b'abcd' + info_data2.read())
f.close()
info_data.close()
info_data2.close()
