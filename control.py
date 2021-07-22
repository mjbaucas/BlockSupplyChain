import time 

global_start = time.time()
time_limit = 600

counter = 0

try:
    while True:
        try:
            counter+=1
            if time.time() > global_start + time_limit:
                print(counter)
                break
        except Exception as e:
            print(e)
        time.sleep(2)
except KeyboardInterrupt:
    print(counter)
    pass
