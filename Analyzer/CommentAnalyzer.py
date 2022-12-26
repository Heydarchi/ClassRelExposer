import re
from AbstractAnalyzer import * 
class CommentAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.pattern = dict()
        self.replaceByStr = dict()

    def initPatterns(self):
        self.pattern["cpp"]=["(\\/\\/).*", "(\\/\\*).*([a-zA-Z0-9\\s]*|\\r|\\n).*(\\*\\/)", "(\\\").*[\\r\\na-zA-Z0-9\\s].*(\\\")"]
        self.pattern["java"]=["(\\/\\/).*", "(\\/\\*).*([a-zA-Z0-9\\s]*|\\r|\\n).*(\\*\\/)", "(\\\").*[\\r\\na-zA-Z0-9\\s].*(\\\")"]

        self.replaceByStr["cpp"]=["//@", "/*@*/", "\"@\""]
        self.replaceByStr["java"]=["//@", "/*@*/", "\"@\""]

    def analyze(self, filePath, lang):
        for regxx in self.pattern[lang]:
            pass
        txt = "The rain in Spain"
        x = re.findall("^The.*Spain$", txt)
        print (x)

if __name__ == "__main__" :
    commentAnalyzer = CommentAnalyzer()
    commentAnalyzer.analyze("haha", "ll")