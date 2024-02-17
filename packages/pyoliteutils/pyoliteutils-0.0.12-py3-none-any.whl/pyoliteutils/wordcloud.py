import base64
from IPython.display import Image, display
import matplotlib.pyplot as plt

def wordcloud(
        content,
        format='svg'
        ):

    url = "https://quickchart.io/wordcloud?format="+format+"&text="+content
    #print(url)
    display(Image(url=url, format=format))