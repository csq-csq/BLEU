from nltk.translate.bleu_score import sentence_bleu,SmoothingFunction
import Baidu_Text_transAPI

if __name__ == '__main__':
    for i in range(35,41):
        reference = [[]]
        candidate = []
        a='data/original/'+str(i)+'.txt'
        b='data/new/'+str(i)+'.txt'
        c='data/result/'+str(i)+'.txt'
        f=open(a,'r+',encoding='utf-8')
        g=open(b,'w+',encoding='utf-8')
        h=open(c,'w+',encoding='utf-8')
        for line in f.readlines():
            line=line.strip()
            line=line.replace('\u2003','')
            line=line.replace(' ','')
            line = line.replace('习近平总书记', '习总书记')
            if line!='':
                lines=line.split('。')
                for l in lines:
                    l = l.strip()
                    l = l.replace('\u2003', '')
                    l = l.replace(' ', '')
                    if l != '':
                        reference[0].append(l)
        # for line in g.readlines():
        #     line=line.strip()
        #     line=line.replace('\u2003','')
        #     line=line.replace(' ','')
        #     if line!='':
        #         candidate.append(line)
        for line in reference[0]:
            temp = Baidu_Text_transAPI.baiduTranslate('zh','en',line)
            temp = Baidu_Text_transAPI.baiduTranslate('en','zh',temp)
            candidate.append(temp)
            g.write(temp+'\n')
        scores=[]
        for j in range(len(candidate)):
            s1=[reference[0][j]]
            s2=candidate[j]
            smooth = SmoothingFunction()
            if len(s2)<=4:
                score=sentence_bleu(s1, s2, smoothing_function=smooth.method1,weights=(0.5,0.5,0,0))
            elif len(s2)<=6:
                score=sentence_bleu(s1, s2, smoothing_function=smooth.method1,weights=(0.33,0.33,0.33,0))
            else:
                score = sentence_bleu(s1, s2, smoothing_function=smooth.method1)
            scores.append(score)
            h.write("score"+str(j)+"="+str(score)+'\n')
        score=sum(scores)/len(scores)
        h.write("final result:"+str(score))
        f.close()
        g.close()
        h.close()



