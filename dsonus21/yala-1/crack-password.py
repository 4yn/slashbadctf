with open('rockyou.txt', 'r') as f:
    line = f.readline()

    while line:
        passwd = line.strip()
        m = sha256()
        m.update((prefix + passwd).encode('utf-8'))
        if m.hexdigest() == target:
            print(f'!!! {prefix + passwd}')
            break

        line = f.readline()