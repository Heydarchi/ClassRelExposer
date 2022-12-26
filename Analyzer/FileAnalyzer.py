import re
from AbstractAnalyzer import * 
class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        pass

    def analyze(self, filePath, pattern):
        txt = "The rain in Spain"
        x = re.findall("^The.*Spain$", txt)
        print (x)

if __name__ == "__main__" :
    fileAnalyzer = FileAnalyzer()
    fileAnalyzer.analyze("haha", "ll")