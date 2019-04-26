from html.parser import HTMLParser
from collections import defaultdict
from copy import deepcopy
import re

class OffsetHTMLParser(HTMLParser,dict):
    def __init__(self):
        super(OffsetHTMLParser, self).__init__()
        self.stack = defaultdict(lambda:[])     #開始タグの一時格納用
    def handle_starttag(self, tag, attrs):
        pos,word = self.get_info()   #現在の位置とタグ全体の文字列を取得
        #辞書に追加
        self.stack[tag].append({"tag":tag,
                                "attrs":attrs,
                                "start":{
                                    "word":word,    #開始タグ全体
                                    "offset":{
                                        "start":{
                                            "line_id":pos[0]-1,
                                            "offset":pos[1]
                                        },
                                        "end":{
                                            "line_id":pos[0]-1,
                                            "offset":pos[1]+len(word)
                                        }
                                    }
                                }
                               })
        self.now = tag  #現在のタグを更新

    def __missing__(self,key):
        self[key] = []
        return self[key]

    def handle_endtag(self, tag):
        if self.stack.get(tag) is None or not self.stack[tag]:
            #終了タグに対応する開始タグが見つけられなかった場合
            return
        corres = self.stack[tag].pop(-1) #対応する開始タグの取得
        pos,word = self.get_info()   #現在の位置とタグ全体の文字列を取得
        corres["end"] = {
            "word":word,      #終了タグ全体
            "offset":{
                "start":{
                    "line_id":pos[0]-1,
                    "offset":pos[1]
                },
                "end":{
                    "line_id":pos[0]-1,
                    "offset":pos[1]+len(word)
                }
            }
        }
        self[corres["tag"]].append(corres)   #マッチしたタグの追加

    def get_info(self):
        """
        現在位置とタグ全体の文字列を返す
        """
        #現在位置取得
        pos = self.getpos()
        #テキストを取得
        sentence = self.rawdata.splitlines()[pos[0]-1][pos[1]:]
        #タグ全文を取得
        m = re.search("<(\".*?\"|\'.*?\'|[^\'\"])*?>",sentence)
        assert m is not None,"正規表現で本文からタグを取得できませんでした"
        return pos,m.group(0)   #現在位置とタグ全体の文字列を返す
    
    def feed(self,data):
        self.stack = defaultdict(lambda:[]) #stackを初期化
        super(OffsetHTMLParser, self).feed(data)

    def reset(self):
        self.stack = defaultdict(lambda:[]) #stackを初期化
        self.clear()    #辞書を初期化
        super(OffsetHTMLParser,self).reset()

    def deepcopy(self):
        return deepcopy(self.copy())

if __name__ == "__main__":
    text = "<html><head><title></title></head><body><h1>見出し1</h1>内容1\n内容2</body></html>"
    parser = OffsetHTMLParser()
    parser.feed(text)
    splitext = text.splitlines()
    for offset in parser["body"]:
        print(offset)
        for idx,t in enumerate(splitext[offset["start"]["offset"]["start"]["line_id"]:offset["end"]["offset"]["end"]["line_id"]+1]):
            print(t)
    print(parser)
    parser.reset()
    #print(parser.deepcopy())
