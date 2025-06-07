import urllib.parse

base_path = "https://pub-a0a268c371304a3ebfc9bccb8e3a3152.r2.dev/video/Luke%201/"
author = "克里斯麦肯"
pic = "R-C.jpeg"

for i in range(21):
    title = f"路加福音1章（{i}）讲"
    filename = f"路加福音1章（{i}）讲.mp3"
    encoded_filename = urllib.parse.quote(filename, safe='')
    url = base_path + encoded_filename
    print(f"{{ title: '{title}', author: '{author}', url: '{url}', pic: '{pic}' }},")
