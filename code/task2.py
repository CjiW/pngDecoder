filename = input("Please enter the path of the png image:")
f = open(filename, "rb")
png_bytes = f.read()
pngBytes_list = list(bytearray(png_bytes))
filetype_list = pngBytes_list[:8]
if filetype_list == [0x89, 0x50, 0x4e, 0x47, 0xd, 0xa, 0x1a, 0xa]:
    info_data = pngBytes_list[16:29]
    width = 2 ** 0 * info_data[3] + \
            2 ** 8 * info_data[2] + \
            2 ** 16 * info_data[1] + \
            2 ** 24 * info_data[0]
    height = 2 ** 0 * info_data[7] + \
             2 ** 8 * info_data[6] + \
             2 ** 16 * info_data[5] + \
             2 ** 24 * info_data[4]
    bit_depth = info_data[8]
    color_type = info_data[9]
    compression = info_data[10]
    Filter = info_data[11]
    interlace = info_data[12]
    print("""width: %d, 
height: %d, 
bit_depth: %d, 
color_type: %d, 
compression: %d, 
filter: %d, 
interlace: %d, """ % (width, height, bit_depth, color_type, compression, Filter, interlace))

