import subprocess

def video_add_mp4(file_name,mp4_file):
    outfile_name = mp4_file.split('.')[0] + '-new.mp4'
    cmd = f'D:\\ffmpeg\\ffmpeg-n4.4-154-g79c114e1b2-win64-gpl-4.4\\bin\\ffmpeg.exe -i {mp4_file} -i {file_name} -acodec copy -vcodec copy {outfile_name}'
    print(cmd)
    subprocess.call(cmd,shell=True)

if __name__ == '__main__':
    a = 'mymp4_6.mp4'    # 视频
    b = 'before.mp4'    # 音频
    video_add_mp4(b,a)