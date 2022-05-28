import threading, time

for i in range(10):
    def myfunc(a, b):
        d = 4
        while d > 0:
            print('сумма :',a + b)
            d -= 1
            time.sleep(0.5)
    for j in range(4):
        thr1 = threading.Thread(target = myfunc, args = (1, 2)).start()

    for g in range(3):
        print('основной поток')
