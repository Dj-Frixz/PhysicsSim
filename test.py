import numpy as np

x = {
    'a':'q',
    's':'w',
    'd':'e',
    'f':'r',
    'g':'t',
    'h':'y',
    'j':'u',
    'k':'i',
    'l':'o',
    'ò':'p'
}

y = np.array([1,2,3,4,5,6])

print(y//[1,2,3,4,5,6])