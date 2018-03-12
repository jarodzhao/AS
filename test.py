f = True

for i in range(1, 8):
    if f:
        print(i)
        f = False
    else:
        print(str(i) + '.')