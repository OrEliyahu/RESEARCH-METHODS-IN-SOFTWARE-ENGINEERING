from urllib.request import urlopen
import time


with open("questions_ids.txt") as questions_file:
    for q in questions_file.read().splitlines():
        print(q)        
        urlopen("http://127.0.0.1:5000/compare?q=" + q)
        time.sleep(5)