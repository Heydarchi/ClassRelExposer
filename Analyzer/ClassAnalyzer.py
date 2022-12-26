import re
from AbstractAnalyzer import * 
class ClassAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.pattern = dict()
        self.innerPattern = dict()

    def initPatterns(self):
        self.pattern["cpp"]=("(\\;|\\{|\\})*(\\r|\\n)*\\s*(\\r|\\n)*(\\/\\/\\s?[a-zA-Z0-9_].*(\\r|\\n)?)?(\\r|\\n)?\\s?(class)\\s+([a-zA-Z0-9_])*\\s*[:{;]")
        self.pattern["java"]=("(\\;|\\{|\\})*(\\r|\\n)*\\s*(\\r|\\n)*(\\/\\/\\s?[a-zA-Z0-9_].*(\\r|\\n)?)?(\\r|\\n)?\\s?(public|private)?\\s+(static)?\\s?(class|interface)\\s+(([a-zA-Z0-9_])*\\s*)*[:{;]")

        self.innerPattern["cpp"]=("(class)\\s+([a-zA-Z0-9_])*\\s*[:{;]")
        self.innerPattern["java"]=("(class|interface)\\s+([a-zA-Z0-9_])*\\s*")

    def analyze(self, filePath, pattern):
        txt = "The rain in Spain"
        x = re.findall("^The.*Spain$", txt)
        print (x)

if __name__ == "__main__" :
    classAnalyzer = ClassAnalyzer()
    classAnalyzer.analyze("haha", "ll")