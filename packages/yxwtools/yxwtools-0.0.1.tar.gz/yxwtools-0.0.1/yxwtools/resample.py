'''
重采样
'''
from pydub import AudioSegment
import sys

def wavresample(wavfile,sr=16000):
    '''
    输入wav文件目录和目标采样率
    该函数生成对应的音频文件，并直接替换掉源文件
    '''
    # 读取音频文件
    audio = AudioSegment.from_wav(wavfile)
    # 将音频重采样到16000Hz并转换为单声道
    resampled_audio = audio.set_frame_rate(sr).set_channels(1)

    # 导出处理后的音频文件
    resampled_audio.export(wavfile, format='wav')




if __name__ =="__main__":
    wavresample(sys.argv[1])

