#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Simon Liu"

def get_F(sub):
    F = [0]
    for i in range(2, len(sub)+1):
        sample_list = []
        sub_T = sub[0:i]
        sub_t_len = len(sub_T)
        for i in range(1, sub_t_len):
            if sub_T[0:i] == sub_T[-i:]:
                sample_list.append(sub_T[0:i])
        if len(sample_list) > 0:
            len_total = []
            for value in sample_list:
                len_total.append(len(value))
            F.append(max(len_total))
        else:
            F.append(0)
    return F

"""
void getNext(int *next, const char *sub)

{
       next[0] = -1;
       int k = -1;
       int len = strlen1(sub);
       for (int i = 1; i < len; i++)
       {
              while (sub[k+1]!=sub[i] &&k>-1)  //如果下一个不相同，往前回溯，等于前一个值 。
              {        
                     k = next[k];
              }
              if (sub[k+1] == sub[i])
              {
                     k = k + 1;
              }
              next[i] = k;
       }
}

intsearchKMP(const char *src, const char *sub)

{
       int slen = strlen1(src);
       int tlen = strlen1(sub);
       //得到next
       int *next = (int*)malloc(sizeof(int)*tlen);
       getNext(next, sub);
       //模式匹配
       int k = -1;
       for (int i = 0; i < slen; i++)
       {
              // 判断当前要不要回退
              while (k>-1 && sub[k+1]!= src[i]) // 回溯
              {
                     k = next[k];
              }
              if (src[i] == sub[k+1])
              {
                     ++k;
              }
              if (k == tlen - 1)
              {
                     free(next);
                     next = NULL;
                     return i - tlen + 1;
              }
       }
       free(next);
       next = NULL;
       return -1;
}

"""


def match(T, sub):
    """
    abaabaabbabaaabaabbabaab
 1  abaabbabaab                k=2
 2     abaabbabaab             k=4
 3           abaabbabaab       k=1
 4              abaabbabaab    k=0
 5               abaabbabaab

    :return:
    """
    F = get_F(sub)
    k = 0
    for i in range(len(T)):
        while k > 0 and T[i] != sub[k]:
            k = F[k-1]
            if k > len(sub)-1:
                break
        if T[i] == sub[k]:
            k += 1
        if k == len(sub):
            return i - len(sub)+1


def simple_matching(t, p):
    for i in range(len(t)):
        k, j = i, 0
        while t[k] == p[j]:
            k += 1
            j += 1
            if j > len(p)-1:
                break
        if j == len(p):
            return i


if __name__ == '__main__':
    print match('abaabaabbabaaabaabbabaab', 'abaabbabaab')
    print simple_matching('abaabaabbabaaabaabbabaab', 'abaabbabaab')


