def write_txt(path, data): 
    with open(path, 'w', encoding='utf-8') as f:
        for d in data:
            f.write(d)
            f.write('\n')
        
        f.close()
        print("write over")

def read_txt1():
    qq = []
    with open(r'C:\Users\wuziyang\Desktop\22.txt', 'r', encoding='utf-8') as f:
        l = f.readline()
        while l:
            s = l.replace('\n', '').replace('[', '').replace(']', '')
            qq.append(s)
            l = f.readline()
        f.close()
    with open(r'C:\Users\wuziyang\Desktop\ron.txt', 'w', encoding='utf-8') as f:
        for d in qq:
            f.write(d)
            f.write('\n')
        
        f.close()
        print("write over")

def read_txt2():
    qq = []
    with open(r'C:\Users\wuziyang\Desktop\11.txt', 'r', encoding='utf-8') as f:
        l = f.readline()
        while l:
            if '[' in l:
                t = []
                s = l.replace('\n', '').replace('[', '').replace(']', '')
                t.append(s.split('  '))
                while l:
                    l = f.readline()
                    if ']' in l:
                        s = l.replace('\n', '').replace('[', '').replace(']', '')
                        t.append(s.split('  '))
                        break
                    else:
                        s = l.replace('\n', '').replace('[', '').replace(']', '')
                        t.append(s.split('  '))
                qq.append(t)
            l = f.readline()


        f.close()
    with open(r'C:\Users\wuziyang\Desktop\operate_v.txt', 'w', encoding='utf-8') as f:
        for d in qq:
            f.write(str(d))
            f.write('\n')
        
        f.close()
        print("write over")

def read_txt3():
    qq = []
    with open(r'C:\Users\wuziyang\Desktop\operate_v.txt', 'r', encoding='utf-8') as f:
        l = f.readline()
        while l:
            l = l.replace('\'', '').replace('[', '').replace('\n', '').replace(']', '').replace(' ', '')
            qq.append(l)
            l = f.readline()

        f.close()
    with open(r'C:\Users\wuziyang\Desktop\operate_v1.txt', 'w', encoding='utf-8') as f:
        for d in qq:
            f.write(str(d))
            f.write('\n')
        
        f.close()
        print("write over")

read_txt3()