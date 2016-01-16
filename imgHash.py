# coding=utf-8
import glob
import os
import sys

from PIL import Image

EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'


def avhash(im):
    """ 计算指纹hash数值 """
    if not isinstance(im, Image.Image):
        im = Image.open(im)  # 如果不是图像类型则以图像类型打开
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.  # 求灰度平均值
    return reduce(lambda x, (y, z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),  # 灰度比较二值列表进行 enumerate 返回索引元组
                  0)  # 由enumerate计算hash指纹


def hamming(h1, h2):
    """ 计算汉明距离 """
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h


if __name__ == '__main__':
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        # 输入参数 python <本脚本名称> <目标路径名称> <要搜索的文件夹路径>
        print "Usage: %s image.jpg [dir]" % sys.argv[0]
    else:
        im, wd = sys.argv[1], '.' if len(sys.argv) < 3 else sys.argv[2]  # 没有第三参数的时候使用搜索目标文件当前目录
        h = avhash(im)  # 得到目标图片的hash指纹

        os.chdir(wd)
        images = []
        for ext in EXTS:  # 搜集目标文件夹中的所有图像文件　保存到列表images中
            images.extend(glob.glob('*.%s' % ext))

        seq = []
        prog = int(len(images) > 50 and sys.stdout.isatty())  # sys.stdout.isatty() 为True 则为运行在终端中
        for f in images:
            seq.append((f, hamming(avhash(f), h)))  # 将目标值与搜索文件夹中的文件hash比较得出汉明距离放入seq列表中
            if prog:
                perc = 100. * prog / len(images)
                x = int(2 * perc / 5)
                print '\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']',
                print '%.2f%%' % perc, '(%d/%d)' % (prog, len(images)),
                sys.stdout.flush()
                prog += 1

        if prog: print
        for f, ham in sorted(seq, key=lambda i: i[1]):  # 排序输出
            print "%d\t%s" % (ham, f)