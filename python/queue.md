# 同步的队列类

queue 模块实现多生产者，多消费者队列。当信息必须安全的在多线程之间交换时，它在线程编程中是特别有用的

## 1. Queue、LifoQueue和PriorityQueue的公共方法

### 1.1 Queue.qsise()

返回队列的大致大小

### 1.2 Queue.empty()

如果队列为空，返回 True ，否则返回 False

### 1.3 Queue.full()

如果队列是满的返回 True ，否则返回 False

### 1.4 Queue.put(item, block=True, timeout=None)

将 item 放入队列。如果可选参数 block 是 true 并且 timeout 是 None (默认)，则在必要时阻塞至有空闲插槽可用。如果 timeout 是个正数，将最多阻塞 timeout 秒，如果在这段时间没有可用的空闲插槽，将引发 Full 异常。反之 (block 是 false)，如果空闲插槽立即可用，则item 放入队列，否则引发 Full 异常 ( 在这种情况下，timeout 将被忽略)

### 1.5 Queue.put_nowait(item)

相当于 put(item, False)

### 1.6 Queue.get(block=True, timeout=None)

从队列中移除并返回一个项目。如果可选参数 block 是 true 并且 timeout 是 None (默认值)，则在必要时阻塞至项目可得到。如果 timeout 是个正数，将最多阻塞 timeout 秒，如果在这段时间内项目不能得到，将引发 Empty 异常。反之 (block 是 false) , 如果一个项目立即可得到，则返回一个项目，否则引发 Empty 异常

### 1.7 Queue.get_nowait()

相当于 get(False)

### 1.8 Queue.task_done()

表示前面排队的任务已经被完成。被队列的消费者线程使用。每个 get() 被用于获取一个任务， 后续调用 task_done() 告诉队列，该任务的处理已经完成

### 1.9 Queue.join()

阻塞至队列中所有的元素都被接收和处理完毕。
当条目添加到队列的时候，未完成任务的计数就会增加。每当消费者线程调用 task_done() 表示这个条目已经被回收，该条目所有工作已经完成，未完成计数就会减少。当未完成计数降到零的时候， join() 阻塞被解除

## 2. queue.Queue(先进先出)

```python
from queue import Queue
# maxsize设置队列中，数据上限，小于或等于0则不限制，容器中大于这个数则阻塞，直到队列中的数据被消掉
q = Queue(maxsize=0)

#写入队列数据
q.put(0)
q.put(1)
q.put(2)

#输出当前队列所有数据
print(q.queue)
#删除队列数据，并返回该数据
q.get()
#输也所有队列数据
print(q.queue)

# 输出:
# deque([0, 1, 2])
# deque([1, 2])
```

## 3. queue.LifoQueue

```python
from queue import LifoQueue

# maxsize设置队列中，数据上限，小于或等于0则不限制，容器中大于这个数则阻塞，直到队列中的数据被消掉
lq = LifoQueue(maxsize=0)

#队列写入数据
lq.put(0)
lq.put(1)
lq.put(2)

#输出队列所有数据
print(lq.queue)
#删除队尾数据，并返回该数据
lq.get()
#输出队列所有数据
print(lq.queue)

#输出:
# [0, 1, 2]
# [0, 1]
```

## 4. queue.PriorityQueue

```python
from queue import PriorityQueue
# 存储数据时可设置优先级的队列, 优先级设置数越小等级越高
pq = PriorityQueue(maxsize=0)

#写入队列，设置优先级
pq.put((9,'a'))
pq.put((7,'c'))
pq.put((1,'d'))

#输出队例全部数据
print(pq.queue)
# [(9, 'a'), (7, 'c'), (1, 'd')]

#取队例数据，可以看到，是按优先级取的。
pq.get()
pq.get()
print(pq.queue)

#输出：
# [(9, 'a')]
```

## 5. collections.deque

```python
from collections import deque
#双边队列
dq = deque(['a','b'])

#增加数据到队尾
dq.append('c')
#增加数据到队左
dq.appendleft('d')

#输出队列所有数据
print(dq)
#移除队尾，并返回
print(dq.pop())
#移除队左，并返回
print(dq.popleft())

#输出:
#deque(['d', 'a', 'b', 'c'])
#c
#d
```
