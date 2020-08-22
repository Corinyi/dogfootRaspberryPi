
html_left = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>hello</title>
    </head>
    <body>

    <h2>left</h2>

    </body>
    </html>
"""

html_right = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>hello</title>
    </head>
    <body>

    <h2>right</h2>

    </body>
    </html>
"""
i=3
while(i != 0):
    i = int(input("input: "))
    if (i == 1):
        html_file = open('index.html', 'w')
        html_file.write(html_left)
        html_file.close()
    if (i ==2):
        html_file = open('index.html', 'w')
        html_file.write(html_right)
        html_file.close()
