bold = "This is text with a **bold block** word"
delimiter = "**"
count = 0
if len(delimiter) == 2:
    j = 0
    for i in range(1, len(bold)):
        if delimiter == (bold[i] + bold[j]):
            count += 1
        j += 1
    if count == 2:
        print(True)
    else:
        print(False)     