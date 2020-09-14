import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlretrieve
from pytube import YouTube
from moviepy.editor import *
import speech_recognition as sr
from os import path
import shutil
import wave
import numpy as np
import pylab as plt

os.makedirs("../test", exist_ok=True)
#設定使用的瀏覽器，並且將網頁設定在Google圖片搜尋(chromedriver要放在桌面)
driver = webdriver.Chrome('C:/Users/Big data/Desktop/chromedriver.exe')
url = 'https://www.youtube.com/?hl=zh-TW&gl=TW'
driver.get(url)

#輸入想搜尋的東西，並且使用Google圖片搜尋此物品
input_str = input("請輸入想搜尋的東西: ")
#input_str = "JoJos Bizarre Adventure"
driver.find_element_by_name('search_query').send_keys(input_str)
driver.find_element_by_id('search-icon-legacy').click()

time.sleep(5)

EE_BS=BeautifulSoup(driver.page_source,'lxml')
total_img=EE_BS.find_all('a',{"id":"video-title"})
#url = driver.current_url
#print(url)

#print(total_img[0])
for i in range(len(total_img)):
    if(total_img[i].get('title')):
        #driver.get(total_img[i].get('title'))
        title = total_img[i].get('title')
        url = total_img[i].get('href')
        url = "https://www.youtube.com/" + url
        #print(title)
        #print(url)

        YouTube(url).streams.first().download()

        video = VideoFileClip(title+'.mp4')
        video.audio.write_audiofile('test.wav')

        os.makedirs("../test", exist_ok=True)
        shutil.move("test.wav", "../test")
        #video.close()
        #os.remove(title+".mp4")

        CutTimeDef = 60  # 以1s截斷檔案
        # CutFrameNum =0

        path = r"..\test"
        files = os.listdir(path)
        files = [path + "\\" + f for f in files if f.endswith('.wav')]

        for i in range(len(files)):
            FileName = files[i]
            print("CutFile File Name is ", FileName)
            f = wave.open(r"" + FileName, "rb")
            params = f.getparams()
            print(params)
            nchannels, sampwidth, framerate, nframes = params[:4]
            CutFrameNum = framerate * CutTimeDef
            # 讀取格式資訊
            # 一次性返回所有的WAV檔案的格式資訊，它返回的是一個組元(tuple)：聲道數, 量化位數（byte    單位）, 採
            # 樣頻率, 取樣點數, 壓縮型別, 壓縮型別的描述。wave模組只支援非壓縮的資料，因此可以忽略最後兩個資訊

            print("CutFrameNum=%d" % (CutFrameNum))
            print("nchannels=%d" % (nchannels))
            print("sampwidth=%d" % (sampwidth))
            print("framerate=%d" % (framerate))
            print("nframes=%d" % (nframes))
            str_data = f.readframes(nframes)
            f.close()  # 將波形資料轉換成陣列
            # Cutnum =nframes/framerate/CutTimeDef
            # 需要根據聲道數和量化單位，將讀取的二進位制資料轉換為一個可以計算的陣列
            wave_data = np.fromstring(str_data, dtype=np.short)
            wave_data.shape = -1, 2
            wave_data = wave_data.T
            temp_data = wave_data.T
            # StepNum = int(nframes/200)
            StepNum = CutFrameNum
            StepTotalNum = 0;
            haha = 0
            while StepTotalNum < nframes:
                # for j in range(int(Cutnum)):
                print("Stemp=%d" % (haha))
                FileName = "..\\testcutresults\\" + files[i][-17:-4] + "-" + str(haha + 1) + ".wav"
                print(FileName)
                temp_dataTemp = temp_data[StepNum * (haha):StepNum * (haha + 1)]
                haha = haha + 1;
                StepTotalNum = haha * StepNum;
                temp_dataTemp.shape = 1, -1
                temp_dataTemp = temp_dataTemp.astype(np.short)  # 開啟WAV文件
                f = wave.open(FileName, "wb")  #
                # 配置聲道數、量化位數和取樣頻率
                f.setnchannels(nchannels)
                f.setsampwidth(sampwidth)
                f.setframerate(framerate)
                # 將wav_data轉換為二進位制資料寫入檔案
                f.writeframes(temp_dataTemp.tostring())
                f.close()

        shutil.copytree('../test', './w')
        shutil.rmtree('../test')
        os.makedirs("../test", exist_ok=True)

        path = r".\w"
        files = os.listdir(path)
        files = [path + "\\" + f for f in files if f.endswith('.wav')]
        freq_wav = len(files)

        for freq in range(1, freq_wav):
            if freq %3 == 0:
                time.sleep(300)
            r = sr.Recognizer()
            with sr.WavFile("./w/test-{}.wav".format(freq)) as source:
                audio = r.record(source)

            f = open(title+'.txt', 'a')

            try:
                respones = r.recognize_google(audio, language='zh-tw')
                print("Transcription: " + r.recognize_google(audio, language='zh-tw'))
                # print(type(respones))
                f.write(respones)
            except LookupError:
                print("Could not understand audio")

        shutil.rmtree('./w')
        os.makedirs("../test", exist_ok=True)
