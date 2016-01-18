# coding=utf-8
import glob
import os
import sys
from PIL import Image
from collections import Counter  # 统计模块

EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'


def convert(data):
    """ 数值转换　"""
    convert_iter = []
    for rgb in data:
        rgb_c = []
        for pixl in rgb:
            if pixl in xrange(0, 64):
                rgb_c.append(0)
            elif pixl in xrange(64, 128):
                rgb_c.append(1)
            elif pixl in xrange(128, 192):
                rgb_c.append(2)
            else:
                rgb_c.append(3)
        tu = tuple(rgb_c)
        convert_iter.append(tu)
    print "convert_iter: ", convert_iter
    return convert_iter


def base_vector(vector):
    base_vector_list = []
    for i in xrange(vector):
        for j in xrange(vector):
            for k in xrange(vector):
                base_vector_list.append((i, j, k))
    return base_vector_list


def calculate_vector(im):
    """计算生成向量"""
    if not isinstance(im, Image.Image):
        im = Image.open(im)  # 如果不是图像类型则以图像类型打开
    # re_p resize 的比例尺度
    # size = im.size
    im = im.resize((8, 8), Image.ANTIALIAS).convert('RGB')

    xx = Counter([i for i in base_vector(4)])  # 将每一个可能都添加到统计中默认为１次（这个１是脏数据本省不存在的）后来要处理掉的

    rgb_convert = convert(im.getdata())
    rgb_convert = sorted(rgb_convert, key=lambda tup: (tup[0], tup[1], tup[2]))
    count = xx + Counter(rgb_convert)
    print "向量数值", count.values()  # 这里列表中的１的值要跟换为０排除上面的脏数据
    return count.values()  # 列表可迭代对象　也可以直接用count.values() 返回列表内容


def PearsonCorrelationSimilarity(vec1, vec2):
    """向量相似度系数计算"""
    value = range(len(vec1))
    sum_vec1 = sum([vec1[i] for i in value])
    sum_vec2 = sum([vec2[i] for i in value])
    square_sum_vec1 = sum([pow(vec1[i], 2) for i in value])
    square_sum_vec2 = sum([pow(vec2[i], 2) for i in value])
    product = sum([vec1[i] * vec2[i] for i in value])
    numerator = product - (sum_vec1 * sum_vec2 / len(vec1))
    dominator = ((square_sum_vec1 - pow(sum_vec1, 2) / len(vec1)) * (
        square_sum_vec2 - pow(sum_vec2, 2) / len(vec2))) ** 0.5
    if dominator == 0:
        return 0
    result = numerator / (dominator * 1.0)
    # 返回相关系数
    return result


if __name__ == '__main__':
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        # 输入参数 python <本脚本名称> <目标路径名称> <要搜索的文件夹路径>
        print "Usage: %s image.jpg [dir]" % sys.argv[0]
    else:
        im, wd = sys.argv[1], '.' if len(sys.argv) < 3 else sys.argv[2]  # 没有第三参数的时候使用搜索目标文件当前目录
        h = calculate_vector(im)  # 得到目标图片的特征向量

        os.chdir(wd)
        images = []
        for ext in EXTS:  # 搜集目标文件夹中的所有图像文件　保存到列表images中
            images.extend(glob.glob('*.%s' % ext))
        seq = []
        prog = int(len(images) > 50 and sys.stdout.isatty())  # sys.stdout.isatty() 为True 则为运行在终端中
        for f in images:
            seq.append((f, PearsonCorrelationSimilarity(calculate_vector(f), h)))  # 将目标值与搜索文件夹中的文件特征向量比较得出相关系数放入seq列表中
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