#!/usr/bin/env python3
'''A binary clock: displays the current time (HHMMSS) in binary-coded decimal.'''

import time
from itertools import zip_longest
from gpiozero import LED

def main():
    #                 H8                M8                S8
    leds = [ None,    LED(14), None,    LED(24), None,    LED(12),
    #        H40      H4       M40      M4       S40      S4
             LED(22), LED(15), LED(11), LED(25), LED(13), LED(16),
    #        H20      H2       M20      M2       S20      S2
             LED(10), LED(18), LED(5),  LED(8),  LED(19), LED(20),
    #        H10      H1       M10      M1       S10      S1
             LED(9),  LED(23), LED(6),  LED(7),  LED(26), LED(21)]

    try:
        while True: 
            t = time.strftime('%H%M%S')
            print(t)
            b = bcd(t)
            s = vertical_strings(b)
            print(s + '\n')
            light(s, leds)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print('done')

# bcd :: iterable(characters '0'-'9') -> [str]
def bcd(digits):
    'Convert a string of decimal digits to binary-coded-decimal.'
    def bcdigit(d):
        'Convert a decimal digit to BCD (4 bits wide).'
        # [2:] strips the '0b' prefix added by bin(). 
        return bin(d)[2:].rjust(4, '0')
    return (bcdigit(int(d)) for d in digits)

# vertical_strings :: iterable(str) -> str
def vertical_strings(strings):
    'Orient an iterable of strings vertically: one string per column.'
    iters = [iter(s) for s in strings]
    concat = ''.join
    return ''.join(map(concat,
                         zip_longest(*iters, fillvalue=' ')))

def light(strings, leds):
    x = 0
    for l in strings:
        if l == '1' and leds[x] is not None:
            leds[x].on()
        elif l == '0' and leds[x] is not None:
            leds[x].off()
        x = x + 1 

if __name__ == '__main__':
    main()