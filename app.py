import pyautogui
from pynput.keyboard import Listener
from pynput import keyboard
import polars as pl
import time
import json

class Rec:
    def __init__(self):
        self.teclas = []
        self.times = []
        self.time_start = time.time()    
        
    def key_code(self, key):
        
        print(key)
        
        self.teclas.append(str(key))
        
        if key == keyboard.Key.esc:
            return False
        
        if key == keyboard.Key.enter:
            print('acionou enter')
        
        self.times.append(round(time.time() - self.time_start,1))

        self.time_start = time.time()

    def start(self):
        with Listener(on_press=self.key_code) as listener:
            listener.join()


def write_json(teclas, times):
    with open('json.json', 'w') as f:
        f.write(json.dumps({'teclas':teclas[:-1], "segundos":times}, indent=4))


def leitura_arquivo():
    return pl.read_csv('dados.txt', separator=';')


record = Rec()
record.start()


write_json(record.teclas, record.times)
print('passei')