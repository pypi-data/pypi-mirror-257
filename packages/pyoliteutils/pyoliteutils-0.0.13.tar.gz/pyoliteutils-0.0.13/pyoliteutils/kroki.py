import sys; import base64; import zlib; 
from IPython.display import Image, display
import matplotlib.pyplot as plt

# https://kroki.io/ 
def kroki(
        content,
        engine='plantuml', # 
        format='svg',
        server='https://plantuml.com/plantuml/'):

    payload = base64.urlsafe_b64encode(zlib.compress(content.encode('utf-8'), 9)).decode('ascii')
    #base64.urlsafe_b64encode(
    #    zlib.compress(sys.stdin.read().encode('utf-8'), 9)).decode('ascii')
    #    )
    url = "https://kroki.io/"+engine+"/"+format+"/"+payload
    #print(url)
    display(Image(url=url, format=format))

def plantuml(content):
    kroki(content, engine="plantuml")

def ditaa(content):
    kroki(content, engine="ditaa")

def graphviz(content):
    kroki(content, engine="graphviz")

def mermaid(content):
    kroki(content, engine="mermaid")