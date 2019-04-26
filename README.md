# html_offset
タグのオフセットを取得するためのHTMLパーサーです

## 概要
HTMLファイルからタグの位置情報を取得するためのHTMLパーサーです。

## 実装
HTMLParserとdictを多重継承する形で書いています。

## 使い方
以下のようにHTMLテキストを`parser.feed`に与えることでオフセットを取得できます。
~~~Python
>>> from html_offset import OffsetHTMLParser
>>> text= '<html><head><title>Hello World!!</title></head></html>'
>>> parser = OffsetHTMLParser()
>>> parser.feed(text)
>>> parser
{'title': [{'tag': 'title', 'attrs': [], 'start': {'word': '<title>', 'offset': {'start': {'line_id': 0, 'offset': 12}, 'end': {'line_id': 0, 'offset': 19}}}, 'end': {'word': '</title>', 'offset': {'start': {'line_id': 0, 'offset': 32}, 'end': {'line_id': 0, 'offset': 40}}}}], 'head': [{'tag': 'head', 'attrs': [], 'start': {'word': '<head>', 'offset': {'start': {'line_id': 0, 'offset': 6}, 'end': {'line_id': 0, 'offset': 12}}}, 'end': {'word': '</head>', 'offset': {'start': {'line_id': 0, 'offset': 40}, 'end': {'line_id': 0, 'offset': 47}}}}], 'html': [{'tag': 'html', 'attrs': [], 'start': {'word': '<html>', 'offset': {'start': {'line_id': 0, 'offset': 0}, 'end': {'line_id': 0, 'offset': 6}}}, 'end': {'word': '</html>', 'offset': {'start': {'line_id': 0, 'offset': 47}, 'end': {'line_id': 0, 'offset': 54}}}}]}
~~~
この時parserインスタンス自体が辞書を兼ねているため、以下のようにも取得できます。
~~~Python
>>> parser['title']
[{'tag': 'title', 'attrs': [], 'start': {'word': '<title>', 'offset': {'start': {'line_id': 0, 'offset': 12}, 'end': {'line_id': 0, 'offset': 19}}}, 'end': {'word': '</title>', 'offset': {'start': {'line_id': 0, 'offset': 32}, 'end': {'line_id': 0, 'offset': 40}}}}]
~~~

## オフセット辞書の構造
parserインスタンスに格納されるオフセット辞書の構造を説明します。
以下のようなHTMLテキストを与えた場合について説明します。
~~~Python
>>> text = "<a href=\"http://xxx.yyy.com\">リンク</a>"
>>> parser.feed(text)
>>> parser
~~~







