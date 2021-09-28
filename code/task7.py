from zlib import decompress, compress


def unfilter(lineData_list, png_hight, png_width):
    # 还原RGB信息
    for i in range(png_hight):
        if lineData_list[i][0] == 0:
            continue
        elif lineData_list[i][0] == 1:
            for j in range(1, (3 * png_width + 1)):
                if j < 4:
                    lineData_list[i][j] += 0
                else:
                    lineData_list[i][j] += lineData_list[i][j - 3]
                lineData_list[i][j] %= 256

        elif lineData_list[i][0] == 2:
            for j in range(1, (3 * png_width + 1)):
                lineData_list[i][j] += lineData_list[i - 1][j]
                lineData_list[i][j] %= 256

        elif lineData_list[i][0] == 3:
            for j in range(1, (3 * png_width + 1)):
                if j < 4:
                    lineData_list[i][j] += lineData_list[i - 1][j] // 2
                else:
                    lineData_list[i][j] += (lineData_list[i][j - 3] + lineData_list[i - 1][j]) // 2
                lineData_list[i][j] %= 256

        else:
            for j in range(1, (3 * png_width + 1)):
                if j < 4:
                    a, c = 0, 0
                else:
                    a = lineData_list[i][j - 3]
                    c = lineData_list[i - 1][j - 3]
                b = lineData_list[i - 1][j]

                p = a + b - c
                min_abs = min(abs(a - p), abs(b - p), abs(c - p))
                if min_abs == abs(a - p):
                    lineData_list[i][j] += a
                elif min_abs == abs(b - p):
                    lineData_list[i][j] += b
                else:
                    lineData_list[i][j] += c
                lineData_list[i][j] %= 256

    return lineData_list


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


def change_to_sum(alist):
    thesum = (2 ** 24) * alist[0] + \
             (2 ** 16) * alist[1] + \
             (2 ** 8) * alist[2] + \
             (2 ** 0) * alist[3]
    return thesum


filename = input("Please enter the path of the png image:")

f = open(filename, "rb")
png_bytes = f.read()
f.close()
pngbytes_list = list(bytearray(png_bytes))
filetype_list = pngbytes_list[:8]
is_png = (filetype_list == [0x89, 0x50, 0x4e, 0x47, 0xd, 0xa, 0x1a, 0xa])
if is_png:
    # print("It is a png")
    nu_bytes = 8
    allAata = bytes()
    png_width, png_hight = 0, 0
    otherdata_list = []
    while nu_bytes < len(pngbytes_list):
        length = change_to_sum(pngbytes_list[nu_bytes:nu_bytes + 4])
        block_data = {"Length": length,
                      "Type": png_bytes[nu_bytes + 4:nu_bytes + 8],
                      "Data": png_bytes[nu_bytes + 8:nu_bytes + 8 + length],
                      "CRC": pngbytes_list[nu_bytes + 8 + length:nu_bytes + 8 + length + 4]}
        if block_data["Type"].decode() == "IDAT":
            allAata += block_data["Data"]
            if not otherdata_list:
                otherdata_list.append(png_bytes[:nu_bytes])

        elif block_data["Type"].decode() == "IHDR":
            png_width = change_to_sum(block_data["Data"][0:4])
            png_hight = change_to_sum(block_data["Data"][4:8])
        elif block_data["Type"].decode() == "IEND":
            otherdata_list.append(png_bytes[nu_bytes:])
        nu_bytes += 8 + length + 4

    # 解压
    unzipedData = decompress(allAata)
    lineData_list = []
    # 分行
    for n in range(png_hight):
        lineData_list.append(list(unzipedData[n * (3 * png_width + 1):(n + 1) * (3 * png_width + 1)]))
    # 还原
    unfilterLine_list = unfilter(lineData_list, png_hight, png_width)

    #################################################################
    # 在此处修改RGB信息

    for i in range(png_hight):
        for j in range(1, 3 * png_width + 1, 3):
            gray = int(unfilterLine_list[i][j] * 0.299 + unfilterLine_list[i][j + 1] * 0.587 + unfilterLine_list[i][
                j + 2] * 0.114)
            # gray = (unfilterLine_list[i][j] + unfilterLine_list[i][j + 1] + unfilterLine_list[i][j + 2]) // 3
            unfilterLine_list[i][j], unfilterLine_list[i][j + 1], unfilterLine_list[i][j + 2] = gray, gray, gray

    # Sobel算子
    gray_list_1 = []
    gray_list_x = []
    gray_list_y = []
    gray_list_2 = []
    for unfilterline in unfilterLine_list:
        gray_list_1.append(unfilterline[1::3])
        gray_list_x.append(unfilterline[1::3])
        gray_list_2.append(unfilterline[1::3])
        gray_list_y.append(unfilterline[1::3])
    x1, x2, x3, y1, y2, y3, z1, z2, z3 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    boundary = int(input("界限(越小边缘越清晰，但噪点越多):"))
    for i in range(png_hight):
        for j in range(png_width):
            x1 = gray_list_1[i - 1][j - 1]
            x2 = gray_list_1[i - 1][j]
            x3 = gray_list_1[i - 1][(j + 1) % png_width]
            y1 = gray_list_1[i][j - 1]
            y2 = gray_list_1[i][j]
            y3 = gray_list_1[i][(j + 1) % png_width]
            z1 = gray_list_1[(i + 1) % png_hight][j - 1]
            z2 = gray_list_1[(i + 1) % png_hight][j]
            z3 = gray_list_1[(i + 1) % png_hight][(j + 1) % png_width]
            if j == 0:
                x1, y1, z1 = 0, 0, 0
            elif j == png_width - 1:
                x3, y3, z3 = 0, 0, 0
            if i == 0:
                x1, x2, x3 = 0, 0, 0
            elif i == png_hight - 1:
                z1, z2, z3 = 0, 0, 0
            gray_list_x[i][j] = -1 * x1 + 1 * x3 + -2 * y1 + 2 * y3 + -1 * z1 + 1 * z3
            gray_list_y[i][j] = -1 * z1 + 1 * x1 + -2 * z2 + 2 * x2 + -1 * z3 + 1 * x3

            if (gray_list_x[i][j] ** 2 + gray_list_y[i][j] ** 2) ** (1 / 2) < boundary:
                gray_list_2[i][j] = 255
            else:
                gray_list_2[i][j] = 0
            unfilterLine_list[i][3 * j + 1], unfilterLine_list[i][3*j+2], unfilterLine_list[i][3*j+3] = gray_list_2[i][j],gray_list_2[i][j],gray_list_2[i][j]

    #################################################################
    filterData = myfilter(unfilterLine_list, png_hight, png_width)
    alldata = []
    for i in filterData:
        alldata += i
    unzipbytes = bytearray(alldata)

    zipbytes = compress(bytes(unzipbytes))

    f = open("./mypng.png", "w+b")

    f.write(otherdata_list[0] + len(zipbytes).to_bytes(length=4, byteorder='big') + \
            b'IDAT' + zipbytes + b'abcd' + otherdata_list[-1])
    f.close()
else:
    print("It is not a png!")
