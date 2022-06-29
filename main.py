from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import Baidu_Text_transAPI

if __name__ == '__main__':
    for i in range(35, 41):
        reference = [[]]
        candidate = []
        a = 'data/original/' + str(i) + '.txt'
        b = 'data/new/' + str(i) + '.txt'
        c = 'data/result/' + str(i) + '.txt'
        f = open(a, 'r+', encoding='utf-8')
        g = open(b, 'w+', encoding='utf-8')
        h = open(c, 'w+', encoding='utf-8')
        for line in f.readlines():
            # 删除空格、回车、以及其他奇奇怪怪的多余字符
            line = line.strip()
            line = line.replace('\u2003', '')
            line = line.replace(' ', '')
            line = line.replace('习近平总书记', '习总书记')  # 这是由于百度自己算法内部的奇怪bug，如果不替换的话整句话的翻译不出来
            if line != '':
                # 把段落拆分成句子
                lines = line.split('。')
                for l in lines:
                    # 继续删除多余字符
                    l = l.strip()
                    l = l.replace('\u2003', '')
                    l = l.replace(' ', '')
                    if l != '':
                        reference[0].append(l)
        # 调用百度的翻译接口来实现回译
        for line in reference[0]:
            temp = Baidu_Text_transAPI.baiduTranslate('zh', 'en', line)
            temp = Baidu_Text_transAPI.baiduTranslate('en', 'zh', temp)
            candidate.append(temp)
            g.write(temp + '\n')
        # 计算BLEU值
        scores = []
        for j in range(len(candidate)):
            s1 = [reference[0][j]]
            s2 = candidate[j]
            # 使用smooth就可以不用把一整句话再切分成单个字
            smooth = SmoothingFunction()
            # 如果字数很少，就不计算3—gram和4-gram
            if len(s2) <= 4:
                score = sentence_bleu(s1, s2, smoothing_function=smooth.method1, weights=(0.5, 0.5, 0, 0))
            elif len(s2) <= 6:
                score = sentence_bleu(s1, s2, smoothing_function=smooth.method1, weights=(0.33, 0.33, 0.33, 0))
            else:
                score = sentence_bleu(s1, s2, smoothing_function=smooth.method1)
            scores.append(score)
            # 把结果写入另一个文档保存
            h.write("score" + str(j) + "=" + str(score) + '\n')
        score = sum(scores) / len(scores)
        h.write("final result:" + str(score))
        f.close()
        g.close()
        h.close()
