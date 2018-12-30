# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 11:42:56 2018

@author: Nicolaj
"""

#!/usr/bin/python

import tkinter as tk

def main():
    pass

def helloCallBack():
    print('hello Call Back')


if __name__ == '__main__':
    w, h = 300, 200
    window = tk.Tk()
    window.title("A figure in a canvas")
    canvas = tk.Canvas(window, width=w, height=h)
    canvas.pack()

    #top = tk.Tk()
    B1 = tk.Button(window, text ="Hello", command = helloCallBack)

    B1.pack()
    window.mainloop()


    main()



