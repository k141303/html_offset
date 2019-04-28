# html_offset
タグのオフセットを取得するためのHTMLパーサーです

## 概要
HTMLファイルからタグの位置情報を取得するためのHTMLパーサーです。
HTMLParserではタグの開始オフセットのみしか取得できず、タグ文字列は推測する必要があるため、タグ文字列も同時に取得できるように変更しました。
これにより終了オフセットは、開始オフセット+タグ文字長で求めることができます。
開始タグ<xxx>と終了タグ</xxx>がマッチした場合に位置情報情報がパーサーに格納されます。
タグが正常に閉じていない場合、つまり開始タグ<xxx>のみが現れた場合、若しくは終了タグ</xxx>のみが現れた場合は、オフセット取得の対象外になります。

## 実装
HTMLParserとdictを多重継承する形で書いています。

## 使い方
以下のようにHTMLテキストを`parser.feed`に与えることでタグごとにオフセットを取得できます。
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
オフセットは以下のようにタグの種類ごとにリストに格納されます。
~~~
{"タグ1":[{オフセット1},{オフセット2}],"タグ2"[...],...}
~~~
各オフセットは、タグ種類、属性(urlなど)、開始オフセット、開始タグ文字列("<title>"などタグ全体)、終了オフセット、終了タグ文字列を持ちます。
~~~
{ "tag":"タグ1",
  "attri"[{"属性1":"文字列"}],
  "start":{ 
      "word":"開始タグ文字列",
      "offset":{"line_id":行番号,"offset":行内タグ開始位置}
    }
  "end":{
      "word":"終了タグ文字列",
      "offset":{"line_id":行番号,"offset":行内タグ開始位置}
    }
}
~~~
オフセット辞書に格納される順番はHTMLテキスト内での終了タグの登場順となります。




