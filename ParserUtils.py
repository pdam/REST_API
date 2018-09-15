import json
import random
from pprint import pprint

import requests


def hyphen_range(s):
    """ yield each integer from a complex range string like "1-9,12, 15-20,23"

    >>> list(hyphen_range('1-9,12, 15-20,23'))
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16, 17, 18, 19, 20, 23]

    >>> list(hyphen_range('1-9,12, 15-20,2-3-4'))
    Traceback (most recent call last):
        ...
    ValueError: format error in 2-3-4
    """
    for x in s.split(','):
        elem = x.split('-')
        if len(elem) == 1: # a number
            yield int(elem[0])
        elif len(elem) == 2: # a range inclusive
            start, end = map(int, elem)
            for i in xrange(start, end+1):
                yield i
        else: # more than one hyphen
            raise ValueError('format error in %s' % x)


def randintWithExclude( start , end , exclude):
    r = None
    while r in exclude or r is None:
         r = random.randint(start ,end)
    return r



SYMBOLS = {
    'customary'     : ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
    'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                       'zetta', 'iotta'),
    'iec'           : ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
    'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                       'zebi', 'yobi'),
}

def bytes2human(n, format='%(value).1f %(symbol)s', symbols='customary'):
    """
    Convert n bytes into a human readable string based on format.
    symbols can be either "customary", "customary_ext", "iec" or "iec_ext",

      >>> bytes2human(0)
      '0.0 B'
      >>> bytes2human(0.9)
      '0.0 B'
      >>> bytes2human(1)
      '1.0 B'
      >>> bytes2human(1.9)
      '1.0 B'
      >>> bytes2human(1024)
      '1.0 K'
      >>> bytes2human(1048576)
      '1.0 M'
      >>> bytes2human(1099511627776127398123789121)
      '909.5 Y'

      >>> bytes2human(9856, symbols="customary")
      '9.6 K'
      >>> bytes2human(9856, symbols="customary_ext")
      '9.6 kilo'
      >>> bytes2human(9856, symbols="iec")
      '9.6 Ki'
      >>> bytes2human(9856, symbols="iec_ext")
      '9.6 kibi'

      >>> bytes2human(10000, "%(value).1f %(symbol)s/sec")
      '9.8 K/sec'

      >>> # precision can be adjusted by playing with %f operator
      >>> bytes2human(10000, format="%(value).5f %(symbol)s")
      '9.76562 K'
    """
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)

def human2bytes(s):
    """
    Attempts to guess the string format based on default symbols
    set and return the corresponding bytes as an integer.
    When unable to recognize the format ValueError is raised.

      >>> human2bytes('0 B')
      0
      >>> human2bytes('1 K')
      1024
      >>> human2bytes('1 M')
      1048576
      >>> human2bytes('1 Gi')
      1073741824
      >>> human2bytes('1 tera')
      1099511627776

      >>> human2bytes('0.5kilo')
      512
      >>> human2bytes('0.1  byte')
      0
      >>> human2bytes('1 k')  # k is an alias for K
      1024
      >>> human2bytes('12 foo')
      Traceback (most recent call last):
          ...
      ValueError: can't interpret '12 foo'
    """
    init = s
    num = ""
    while s and s[0:1].isdigit() or s[0:1] == '.':
        num += s[0]
        s = s[1:]
    num = float(num)
    letter = s.strip()
    for name, sset in SYMBOLS.items():
        if letter in sset:
            break
    else:
        if letter == 'k':
            # treat 'k' as an alias for 'K' as per: http://goo.gl/kTQMs
            sset = SYMBOLS['customary']
            letter = letter.upper()
        else:
            raise ValueError("can't interpret %r" % init)
    prefix = {sset[0]:1}
    for i, s in enumerate(sset[1:]):
        prefix[s] = 1 << (i+1)*10
    return int(num * prefix[letter])



def sizeof_fmt(num, suffix=''):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024:
            return "%d%s%s" % (num, unit, suffix)
        num /= 1024
    return "%d%s%s" % (int(num), 'Yi', suffix)


def generateRandomMac():
    return ':'.join(map(lambda x: "%02x" % x, [ 0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]))

intervals = (
    ('w', 604800),  # 60 * 60 * 24 * 7
    ('d', 86400),    # 60 * 60 * 24
    ('h', 3600),    # 60 * 60
    ('m', 60),
    ('s', 1),
    )

def display_time(seconds, granularity=2):
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{}{}".format(value, name))
    return ','.join(result[:granularity])



def validateJSONOutputAgainstSwaggerModel(switch, jsonData ,endpoint,  resource ,username ,password):
    mismatchList=[]

    resp=requests.get("http://%s/vRest/api-docs/%s"%(switch,endpoint) , auth=(username,password))
    data = resp.json()["models"][resource]["properties"]
    pprint(data)
    for  item in data.keys():
        typeFromModel = item['type']
        if  type(json.loads(jsonData)) == list :
            for e in jsonData :
                typeFromJson= type(e[item])
                if typeFromJson != typeFromModel :
                    mismatchList.append({ item : {  'json' : typeFromJson , 'model' : typeFromModel }})
        else:
            typeFromJson= type(jsonData[item])
            if typeFromJson != typeFromModel :
                    mismatchList.append({ item : {  'json' : typeFromJson , 'model' : typeFromModel }})
    return mismatchList

