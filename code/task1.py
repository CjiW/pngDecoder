filename = input("Please enter the path of the png image:")
f = open(filename, "rb")
png_bytes = f.read()
pngbytes_list = list(bytearray(png_bytes))
filetype_list = pngbytes_list[:8]
if filetype_list == [0x89, 0x50, 0x4e, 0x47, 0xd, 0xa, 0x1a, 0xa]:
    # print("It is a png")
    nu_bytes = 8
    block_list = []
    while nu_bytes < len(pngbytes_list):
        length = (2 ** 24) * pngbytes_list[nu_bytes] + \
                 (2 ** 16) * pngbytes_list[nu_bytes + 1] + \
                 (2 ** 8) * pngbytes_list[nu_bytes + 2] + \
                 (2 ** 0) * pngbytes_list[nu_bytes + 3]
        block_data = {"Length": length,
                      "Type": png_bytes[nu_bytes + 4:nu_bytes + 8],
                      "CRC": pngbytes_list[nu_bytes + 8 + length:nu_bytes + 8 + length + 4]}
        nu_bytes += 8 + length + 4
        block_list.append(block_data)

    print("Length    Type    CRC")
    for i in block_list:
        print("%6s   %5s    %5s" % (str(i["Length"]), i["Type"].decode(), str(i["CRC"])))

else:
    print("It is not a png!")

