from zlib import decompress

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|(1{[?-_+~<>i!lI;:,^`. ")


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
    # 计算灰度

    for i in range(png_hight):
        for j in range(1, 3 * png_width + 1, 3):
            gray = (unfilterLine_list[i][j] + unfilterLine_list[i][j + 1] + unfilterLine_list[i][j + 2]) // 3
            unfilterLine_list[i][j], unfilterLine_list[i][j + 1], unfilterLine_list[i][j + 2] = gray, gray, gray
    output = ''
    print("width:%d  hight:%d" % (png_width, png_hight))
    nu_down = int(input("please set the number of characters in  Vertical direction:\n"))
    nu_right = int(input("please set the number of characters in  Horizontal direction:\n"))
    down = png_hight // nu_down
    right = png_width // nu_right
    for i in range(0, png_hight, down):
        for j in range(1, 3 * png_width + 1, right * 3):
            sum = 0
            for yy in unfilterLine_list[i:i + down]:
                for xx in yy[j:j + right * 3:3]:
                    sum += xx
            output += ascii_char[sum // (down * right) // 4]
        output += "\n"
    f = open("./output.txt", "w+")
    f.write(output)
    f.close()
