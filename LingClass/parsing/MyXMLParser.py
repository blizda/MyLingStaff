import xml.sax

class MyXMLParser(xml.sax.ContentHandler):
    def __init__(self):
        self.workStr = ''
        self.isText = False
        self.textMas = []
    def startElement(self, name, attr):
        if name == 'text':
            self.workStr = ''
            self.isText = True
    def characters(self, content):
        if self.isText:
            self.workStr = self.workStr + content
    def endElement(self, tag):
        if tag == 'text':
            self.isText = False
            str = self.workStr
            if(str):
                self.textMas.append(str.replace('\n', ' '))
                self.textMas.append('')
            self.workStr = ''
    def retData(self):
        return self.textMas

