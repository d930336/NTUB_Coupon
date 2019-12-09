import os

def ErrorWrite(filename,content):
    if os.path.exists(filename):
        f = open(filename, 'a' , encoding='utf-8')
        f.write(content)
        f.close()
    else:
        f = open(filename, 'w' , encoding='utf-8')
        f.write(content)
        f.close()


