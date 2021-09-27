from zlib import decompress


def unfilter(lineData_list, png_hight, png_width):
    # 还原RGB信息
    r_list, g_list, b_list = [], [], []
    for i in range(png_hight):

        if lineData_list[i][0] == 1:
            for j in range(1, (3 * png_width + 1)):
                if j < 4:
                    lineData_list[i][j] += 0
                else:
                    lineData_list[i][j] += lineData_list[i][j - 3]
                lineData_list[i][j] = int(lineData_list[i][j] % 256)

        elif lineData_list[i][0] == 2:

            if i != 0:
                for j in range(1, (3 * png_width + 1)):
                    lineData_list[i][j] += lineData_list[i - 1][j]
                    lineData_list[i][j] = int(lineData_list[i][j] % 256)

        elif lineData_list[i][0] == 3:
            for j in range(1, (3 * png_width + 1)):
                if j < 4:
                    a = 0
                else:
                    a = lineData_list[i][j - 3]
                if i == 0:
                    b = 0
                else:
                    b = lineData_list[i - 1][j]
                lineData_list[i][j] += (a + b) // 2
                lineData_list[i][j] = int(lineData_list[i][j] % 256)

        elif lineData_list[i][0] == 4:
            for j in range(1, (3 * png_width + 1)):
                if j < 4:
                    a, c = 0, 0
                else:
                    a = lineData_list[i][j - 3]
                    c = lineData_list[i - 1][j - 3]
                if i == 0:
                    b, c = 0, 0
                else:
                    b = lineData_list[i - 1][j]

                p = a + b - c
                pa, pb, pc = abs(a - p), abs(b - p), abs(c - p)
                if pa <= pb and pa <= pc:
                    count = a
                elif pb <= pc:
                    count = b
                else:
                    count = c
                lineData_list[i][j] = int((lineData_list[i][j] + count) % 256)

        r_list.append(lineData_list[i][1::3])
        g_list.append(lineData_list[i][2::3])
        b_list.append(lineData_list[i][3::3])

    return [r_list, g_list, b_list]


def change_to_sum(alist):
    thesum = (2 ** 24) * alist[0] + \
             (2 ** 16) * alist[1] + \
             (2 ** 8) * alist[2] + \
             (2 ** 0) * alist[3]
    return thesum


filename = input("Please enter the path of the png image:")
f = open(filename, "rb")
png_bytes = f.read()
pngbytes_list = list(bytearray(png_bytes))
filetype_list = pngbytes_list[:8]
is_png = (filetype_list == [0x89, 0x50, 0x4e, 0x47, 0xd, 0xa, 0x1a, 0xa])
if is_png:
    # print("It is a png")
    nu_bytes = 8
    allAata = bytes()
    png_width, png_hight = 0, 0
    while nu_bytes < len(pngbytes_list):
        length = change_to_sum(pngbytes_list[nu_bytes:nu_bytes + 4])
        block_data = {"Length": length,
                      "Type": png_bytes[nu_bytes + 4:nu_bytes + 8],
                      "Data": png_bytes[nu_bytes + 8:nu_bytes + 8 + length],
                      "CRC": pngbytes_list[nu_bytes + 8 + length:nu_bytes + 8 + length + 4]}
        if block_data["Type"].decode() == "IDAT":
            allAata += block_data["Data"]

        elif block_data["Type"].decode() == "IHDR":
            png_width = change_to_sum(block_data["Data"][0:4])
            png_hight = change_to_sum(block_data["Data"][4:8])
        nu_bytes += 8 + length + 4
    # 解压
    unzipedData = decompress(allAata)
    lineData_list = []
    # 分行
    for n in range(png_hight):
        lineData_list.append(list(unzipedData[n * (3 * png_width + 1):(n + 1) * (3 * png_width + 1)]))
    # 还原
    rgb_list = unfilter(lineData_list, png_hight, png_width)
    r_list = rgb_list[0]
    g_list = rgb_list[1]
    b_list = rgb_list[2]


    while 1:
        i = int(input("please enter x:"))
        j = int(input("please enter y:"))
        if j < png_width and i < png_hight:
            print("r:%d g:%d b:%d" % (r_list[i][j] * 257, g_list[i][j] * 257, b_list[i][j] * 257))
        else:
            print("!!! OUT OF RANGE !!!")


else:
    print("It is not a png!")
