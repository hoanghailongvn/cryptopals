a = 3

def test():
    global a
    a = 10
    print(a)
    

test()
print(a)