import re
import os

# Encode each segment with xml so that icelandic characters dont get distorted
encoding = '<?xml version="1.0" encoding="UTF-8"?>\n'

def segment(bookname="bok1"):
    # Takes in the file location and name of the book
    with open("././public/uploads/{}/{}.html".format(bookname, bookname), "r", encoding="utf8") as f:
        text = f.read()
    # Split the text at each header
    segments = re.split(r'<h1', text)

    # If segments and or a directory for the book does not exist create it
    if not os.path.exists("././public/uploads/{}/segments/".format(bookname)):
        os.makedirs("././public/uploads/{}/segments/".format(bookname))

    for i, segment in enumerate(segments[1:]):
        with open("././public/uploads/{}/segments/b{}.html".format(bookname, i + 1), "w", encoding="utf8") as f:
            # Write each segment into a seperate html file for later use
            f.write(encoding + '<h1' + segment)