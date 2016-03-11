# coding=utf-8
import binascii
import base64
DEFAULT_KEY = "\x59\xf3\x02\xc3\x25\x9a\x82\x30\x0b\xbb\x25\x7f\x7e\x3b\xd2\xdc"

def rc4(data, key=DEFAULT_KEY, skip=1024):
    x = 0
    box = range(256)
    


    x = 0
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        tmp = box[i]
        tmp2 = box[x]
        box[i] = box[x]
        box[x] = tmp
    

    x = 0
    y = 0
    out = []
    if skip > 0:
        for i in range(skip):
            x = (x + 1) % 256
            y = (y + box[x]) % 256
            box[x], box[y] = box[y], box[x]

    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        k = box[(box[x] + box[y]) % 256]
        # print k
        out.append(chr(ord(char) ^ k))
    return out
#  rc4 编码
def RC4encode(string,key):
    out = rc4(string,key,0)
    outStr = ''.join(out)
    b2hex = binascii.b2a_hex(outStr).upper()
    return b2hex

 #   rc4 解码
def RC4decode(string,key):
    b2hex = binascii.a2b_hex(string)
    temp = ''.join(b2hex) 
    result = rc4(temp,key,0)
    return ''.join(result)


def base64encode(rc4str):
    return base64.b64encode(rc4str)

def base64decode(base64str):
    return base64.b64decode(base64str)  

if __name__ == '__main__':
    # handle input file or stream
    import sys
    
    # rc4("pm:25", "aaa.com", 0)
    # RC4encode("pm:25", "aaa.com")
    RC4decode("768ADF9A12","aaa.com")
    print base64decode(base64encode(RC4decode("768ADF9A12","aaa.com")))
    print base64encode(RC4encode("pm:25", "aaa.com"))
    encodeData = base64encode(RC4encode("pm:25", "aaa.com"))
    print RC4decode(base64decode(encodeData), 'aaa.com')




