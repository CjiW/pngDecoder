import zlib

filename = input("Please enter the path of the png image:")
f = open(filename, "rb")
png_bytes = f.read()
pngbytes_list = list(bytearray(png_bytes))
filetype_list = pngbytes_list[:8]
if filetype_list == [0x89, 0x50, 0x4e, 0x47, 0xd, 0xa, 0x1a, 0xa]:
    # print("It is a png")
    nu_bytes = 8
    data_list = []
    allAata = bytes()
    png_width, png_hight = 0, 0
    while nu_bytes < len(pngbytes_list):
        length = (2 ** 24) * pngbytes_list[nu_bytes] + \
                 (2 ** 16) * pngbytes_list[nu_bytes + 1] + \
                 (2 ** 8) * pngbytes_list[nu_bytes + 2] + \
                 (2 ** 0) * pngbytes_list[nu_bytes + 3]
        block_data = {"Length": length,
                      "Type": png_bytes[nu_bytes + 4:nu_bytes + 8],
                      "Data": png_bytes[nu_bytes + 8:nu_bytes + 8 + length],
                      "CRC": pngbytes_list[nu_bytes + 8 + length:nu_bytes + 8 + length + 4]}
        if block_data["Type"].decode() == "IDAT":
            allAata += block_data["Data"]
        elif block_data["Type"].decode() == "IHDR":
            png_width = (2 ** 24) * block_data["Data"][0] + \
                        (2 ** 16) * block_data["Data"][1] + \
                        (2 ** 8) * block_data["Data"][2] + \
                        (2 ** 0) * block_data["Data"][3]
            png_hight = (2 ** 24) * block_data["Data"][4] + \
                        (2 ** 16) * block_data["Data"][5] + \
                        (2 ** 8) * block_data["Data"][6] + \
                        (2 ** 0) * block_data["Data"][7]
        nu_bytes += 8 + length + 4

    unzipedData = zlib.decompress(allAata)
    lineData_list = []
    r_list = []
    g_list = []
    b_list = []
    for n in range(png_hight):
        r_list.append([])
        g_list.append([])
        b_list.append([])

        lineData_list.append(list(unzipedData[n * (3 * png_width + 1):(n + 1) * (3 * png_width + 1)]))
    # 还原RGB信息
    for i in range(png_hight):
        if lineData_list[i][0] == 0:
            continue
        elif lineData_list[i][0] == 1:
            for j in range(4, (3 * png_width + 1)):
                lineData_list[i][j] += lineData_list[i][j - 3]
                lineData_list[i][j] %= 256

        elif lineData_list[i][0] == 2:
            for j in range(1, (3 * png_width + 1)):
                lineData_list[i][j] += lineData_list[i - 1][j]
                lineData_list[i][j] %= 256

        elif lineData_list[i][0] == 3:
            for j in range(4, (3 * png_width + 1)):
                lineData_list[i][j] += (lineData_list[i][j - 3] + lineData_list[i - 1][j]) // 2
                lineData_list[i][j] %= 256

        else:
            for j in range(4, (3 * png_width + 1)):
                a = lineData_list[i][j - 3]
                b = lineData_list[i - 1][j]
                c = lineData_list[i - 1][j - 3]
                p = a + b - c
                min_abs = min(abs(a - p), abs(b - p), abs(c - p))
                if min_abs == abs(a - p):
                    lineData_list[i][j] += a
                elif min_abs == abs(b - p):
                    lineData_list[i][j] += b
                else:
                    lineData_list[i][j] += c
                lineData_list[i][j] %= 256
        r_list[i] = lineData_list[i][1::3]
        g_list[i] = lineData_list[i][2::3]
        b_list[i] = lineData_list[i][3::3]
    while 1:
        i = int(input("please enter x:"))
        j = int(input("please enter y:"))
        if j < png_width and i < png_hight:
            print("r:%d g:%d b:%d" % (r_list[i][j], g_list[i][j], b_list[i][j]))
        else:
            print("!!! OUT OF RANGE !!!")

else:
    print("It is not a png!")

f.close()
