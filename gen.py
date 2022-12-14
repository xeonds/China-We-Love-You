#!/usr/bin/python3
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
from os import path
import numpy as np
import jieba

def word_segment(text):   #通过jieba进行分词并通过空格分隔,返回分词后的结果
    jieba_word=jieba.cut(text,cut_all=False)
    seg_list=' '.join(jieba_word)
    return seg_list

def generate_wordcloud(text):   #输入文本生成词云,如果是中文文本需要先进行分词处理
    d=path.dirname(__file__)
    mask = np.array(Image.open(path.join(d, "cn-mask.png")))
    font_path=path.join(d,"msYaHei.ttf")
    stopwords = set(STOPWORDS)
    wc = WordCloud(
        scale=4,
        background_color="white",
        max_words=2000,      # 词云显示的最大词数  
        mask=mask,           # 设置背景图片       
        stopwords=stopwords, # 设置停用词
        font_path=font_path, # 兼容中文字体，不然中文会显示乱码
    )
    wc.generate(text)
    wc.to_file(path.join(d, "word-cloud.png"))
    # 显示图像
    # plt.imshow(wc, interpolation='bilinear')
    # plt.axis("off")
    # plt.show()

def img2alpha(path):
    img = Image.open(path)
    img = img.convert('RGBA')
    w, h = img.size
    for x in range(0, w):
        for y in range(0, h):
            r, g, b, a = img.getpixel((x, y))
            if r+g+b==765:
                a=0                                 #改成完全透明
            img.putpixel((x, y), (r, g, b, a))      #设置像素颜色
    img.save('alpha.png')

def imgabg(bg,aim):
    dx = Image.open(aim)
    hc = Image.open(bg)
    w, h = dx.size
    dx = dx.resize((w//3, h//3))
    hc.paste(dx, (150,30), mask=dx.split()[2])
    hc.save('res.jpg')

if __name__=='__main__':
    text = open('十九大报告全文.txt').read()
    text=word_segment(text)     # 分词
    generate_wordcloud(text)    # 生成词云
    img2alpha('word-cloud.png')
    imgabg('bg.jpg','alpha.png')
    plt.imshow(plt.imread('res.jpg'))
    plt.show()
