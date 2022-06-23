total_count = 100000000/2

with open("/Users/jay/Desktop/access2.log", 'w') as f:
    count = 0
    while count < total_count:
        with open("/Users/jay/Desktop/access.log") as file:
            while (line := file.readline()):
                f.write(str(count) + "-->" + line)
                count += 1
                if count > total_count:
                    break
