from datetime import datetime


def debug(content, title=None):
    with open("logs.txt", "a") as text_file:
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if title is None:
            title = ''
        else:
            title += ' - '

        print(f"[{time}] {title}{content}", file=text_file)
