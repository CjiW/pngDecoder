import cv2

video = cv2.VideoWriter('mymp4.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 20, (1920, 1080))  # 创建视频流对象-格式一
for i in range(1, 2877):
    file_name = './afterimages/mypng' + str(i) + '.png'
    image = cv2.imread(file_name)
    video.write(image)  # 向视频文件写入一帧--只有图像，没有声音
    print("\r已写入%d帧" % i)
cv2.waitKey()
