from zlib import decompress, compress, crc32
import numpy as np


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


def get_unfilterlist(png_name):
    global png_width, png_hight, unfilterLinelist, otherdata_list
    f = open(png_name, "rb")
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
        all_blocks = []
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
            all_blocks.append(block_data)

        # 解压
        unzipedData = decompress(allAata)
        lineData_list = []
        # 分行
        for n in range(png_hight):
            lineData_list.append(list(unzipedData[n * (3 * png_width + 1):(n + 1) * (3 * png_width + 1)]))
        # 还原
        unfilterLinelist = unfilter(lineData_list, png_hight, png_width)
        return [png_hight, png_width, unfilterLinelist, otherdata_list, all_blocks]
    else:
        return 0


def mywrite(filterData, filename):
    alldata = []
    for i in filterData:
        alldata += i
    unzipbytes = bytearray(alldata)

    zipbytes = compress(bytes(unzipbytes))

    bytes_withoutcrc = otherdata_list[0][:29] + \
                       len(zipbytes).to_bytes(4, "big") + b'IDAT' + zipbytes + \
                       int(0).to_bytes(4, "big") + b'IEND'
    crc1 = crc32(bytes_withoutcrc[12:29], 0)
    crc2 = crc32(b'IDAT'+ zipbytes, 0)
    crc3 = crc32(b'IEND', 0)

    f = open(filename, "w+b")

    f.write(bytes_withoutcrc[:29] + crc1.to_bytes(4, "big") + bytes_withoutcrc[29:-8] + crc2.to_bytes(4, "big") + \
            bytes_withoutcrc[-8:] + crc3.to_bytes(4, "big"))
    f.close()


global all_blocks
all_list = get_unfilterlist(input("Please enter the path of the png image:"))
characterpngdatalist = get_unfilterlist("./character.png")
characterpnghight = characterpngdatalist[0]
characterpngwidth = characterpngdatalist[1]
characterpngdataArray = np.array(characterpngdatalist[2])
bw_characterArray = characterpngdataArray[:, 1::3]
characterpnglist = np.hsplit(bw_characterArray, 64)

if all_list:
    png_hight = all_list[0]
    png_width = all_list[1]
    unfilterLine_list = all_list[2]
    unfilterLine_array = np.array(unfilterLine_list)
    unfilterData_array = unfilterLine_array[:, 1::3]
    otherdata_list = all_list[3]
    #################################################################
    # 在此处修改RGB信息
    for i in range(png_hight):
        for j in range(1, 3 * png_width + 1, 3):
            gray = int(unfilterLine_list[i][j] * 0.299 + unfilterLine_list[i][j + 1] * 0.587 + unfilterLine_list[i][
                j + 2] * 0.114)
            # gray = (unfilterLine_list[i][j] + unfilterLine_list[i][j + 1] + unfilterLine_list[i][j + 2]) // 3
            unfilterLine_list[i][j], unfilterLine_list[i][j + 1], unfilterLine_list[i][j + 2] = gray, gray, gray

    print("width:%d  hight:%d" % (png_width, png_hight))

    down = characterpnghight
    right = characterpngwidth // 64
    for i in range(0, png_hight, down):
        for j in range(1, png_width + 1, right):
            sum = 0
            for yy in unfilterLine_list[i:i + down]:
                for xx in yy[j * 3 - 2:j * 3 - 2 + right * 3:3]:
                    sum += xx
            characterpng = characterpnglist[63-sum // (down * right) // 4]
            if j + right <= png_width and i + down <= png_hight:
                unfilterData_array[i:i + down, j:j + right] = characterpng

    for i in range(png_hight):
        for j in range(png_width):
            unfilterLine_list[i][3 * j + 1], unfilterLine_list[i][3 * j + 2], unfilterLine_list[i][3 * j + 3] = \
                unfilterData_array[i][j], unfilterData_array[i][j], unfilterData_array[i][j]
    #################################################################
    filterData = myfilter(unfilterLine_list, png_hight, png_width)
    mywrite(filterData, "mypng.png")
else:
    print("It is not a png!")
