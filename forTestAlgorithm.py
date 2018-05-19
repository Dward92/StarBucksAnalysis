# -*- coding: utf-8 -*-
# __Author__: Sdite, amyy4, JX-Soleil, hzgege
# __Email__ : a122691411@gmail.com

import time
import heapq
import pandas as pd

# 大顶堆求前k小
def topKHeap(A, k):
    res = []
    for elem in A:
        elem = -elem
        if len(res) < k:
            heapq.heappush(res, elem)
        else:
            topkSmall = res[0]
            if elem > topkSmall:
                heapq.heapreplace(res, elem)

    return list(map(lambda x: -x, res))

# 非递归实现
def qSelect(A, k):
    if len(A) < k:
        return A

    s = []
    res = []
    s.append(A)

    while s:
        B = s.pop()
        if not B:
            break
        pivot = B[0]
        left = [x for x in B[1:] if x < pivot] + [pivot]
        lLen = len(left)
        if lLen == k:
            res += left
        elif lLen > k:
            s.append(left)
        else:
            res += left
            k -= lLen
            right = [x for x in B[1:] if x >= pivot]
            s.append(right)

    return res

if __name__ == '__main__':
    csv_file = pd.read_csv("directory.csv")

    start = time.clock()
    distance = csv_file.apply(
        lambda x:calcDistance(0, 0, x.Longitude, x.Latitude),
                              axis=1)
    end = time.clock()

    print('遍历计算点间距离时间: %fs' % (end - start))

    useTime = dict()
    useTime['heap'] = []
    useTime['qSelect'] = []
    useTime['pandas'] = []

    for k in range(1, 25601):
        start = time.clock()
        topKHeap(distance, k)
        end = time.clock()
        h = end - start
        useTime['heap'].append(h)


        start = time.clock()
        qSelect(list(distance), k)
        end = time.clock()
        q = end - start
        useTime['qSelect'].append(q)


        start = time.clock()
        distance.nsmallest(k)
        end = time.clock()
        n = end - start
        useTime['pandas'].append(n)

        print("k: %d 大顶堆: %.15fs  快速选择: %.15fs  pandas: %.15fs" % (k, h, q, n))

    import pickle
    with open('config/tmp.pickle', 'wb') as f:
        pickle.dump(useTime, f)

    # with open('config/tmp.pickle', 'rb') as f:
    #     useTime = pickle.load(f)
    #
    # trace1 = Bar(
    #     y=useTime['heap'],
    #     x=list(range(1, 25601)),
    #     name='大顶堆'
    # )
    # trace2 = Bar(
    #     y=useTime['qSelect'],
    #     x=list(range(1, 25601)),
    #     name='快速选择'
    # )
    # trace3 = Bar(
    #     y=useTime['pandas'],
    #     x=list(range(1, 25601)),
    #     name='pandas'
    # )
    # data = [trace1, trace2, trace3]
    # layout = Layout(
    #     barmode='group'
    # )
    # fig = Figure(data=data, layout=layout)
    # py.plot(fig, filename='html/时间比较.html')