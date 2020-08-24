def html_sending(s):
    str1 = " "
    str2 = str1.join(s)
    str3 = "<html><head><title>Hello</title></head><body><h1>" + str2 + "</h1></body></html>"
    html_file = open('test.html', 'w')
    html_file.write(str3)
    html_file.close()

hello = ['a', 'hellp', 'happy']



html_sending(hello)