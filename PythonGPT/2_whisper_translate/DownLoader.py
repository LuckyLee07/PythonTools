# -*- coding: UTF-8 -*-
import time
import pytube

# 下载YouTube视频
def video_download_pytube(video_list):
    for index, video_url in enumerate(video_list):
        # 1、创建YouTube对象
        youtube = pytube.YouTube(video_url)
        
        # 2、获取视频流(可选视频质量)
        #stream = yt.streams.filter(res='720p').first()
        stream = youtube.streams.get_highest_resolution()
                
        # 3、开始下载视频
        print('Downloding Video =====>>>', youtube.title)
        stream.download(output_path="load_mp4")


video_lists = [
    'https://www.youtube.com/watch?v=JxIZbV_XjAs',
    
]

if __name__ == '__main__':
    video_download_pytube(video_lists)

