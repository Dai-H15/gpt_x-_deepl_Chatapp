使用する際は原則、api_keysファイルにapikeyを入力した上で、ファイル名をapi_keys.pyに変更した上でメインのファイルを実行することをおすすめします(全部のバグを拾いきれている気がしないので)
(指摘、コメントいただけると嬉しいです)


# gpt_x-_deepl_Chatapp

大学で積極的な活用を促されているGPTを用いた簡単に記憶の半永久保存を可能にしたPythonコードです。
大学で提供されているアプリでは、1セッションが数分で終了してしまうので、jsonファイルで会話内容を出力することで続きから会話を継続できるようにしました。
また、APIでは使用できるトークン数に限りがあるため、DeepLのAPIで同時に自動翻訳させることで、会話できる量を増やせるようになっています。

追記(2024/04/17): 学内のアプデで、これらの問題はほぼすべて解決しました。ただ、色々カスタムしながら使用できる利点はまだ残っているのでまだ大丈夫です（なにが）

とりあえず動けばいいや理論で動いているため、エンコーディングの作業やタイポ、その他諸々の問題が残っているので注意してください。

OpenAI APIは大学で使用しているAPIキーがあればそれを
なければ個人契約してAPIキーを取得し、
DeepL APIに関しても同様にアカウントを作成してAPIキーを取得してください

＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿



このプログラムの特徴は以下のとおりです

1.	複数行、1行どちらの入力にも対応している

2.	自動翻訳で使用されるトークン数を削減

3.	JSON形式で会話内容を保存できるようにすることで、次回以降続きから会話を継続することができる

4.	rawモードと呼んでいる自動翻訳を無効化する機能でプログラムの送信にも対応できる

5.	APIキーやベースURLを別ファイルに保存して、起動時に自動で読み込ませたり、起動後に変更や設定が可能になっている

6.	テキスト形式で会話内容を出力できる　(日本語/English)

7.	保存された会話内容をコマンド1つで再翻訳することができる



＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿



現在対応しているコマンドは以下のとおりです。helpコマンドで出力することができる内容になっています。

one:一文のみ入力
mult:連続入力
save:プロンプトをエクスポートして終了
new:会話を新しくやり直す
info:現在のトークン数を表示(インポート直後は無効)
view:会話内容を全表示
translate:会話内容を日本語化して表示
exit:保存せずに終了
reload:アプリを再起動
settings:詳細設定を表示
print:テキストファイル形式で会話内容を出力



＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿



rawモードの詳細は以下のとおりです。settings→1から抜粋

このプログラムは、ChatGPTにおけるトークン数の消費量削減のために、送信時、受信時に適した状態にする機能が搭載されています。
しかし、ソースコードを送信する際や、使用しているAPIは自動翻訳のため、意図した回答が得られない状況が発生するおそれがあります。通常はこの機能を有効にしておくことをおすすめしますが、こういった状況に陥った場合にオフにすることも可能です。
既定の設定では自動翻訳が有効化されているため、rawモードは無効になっています



＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿



APIキーの設定方法は現在では2通り用意してあります。

1. 別ファイルにて指定

2. settingsコマンドから指定



＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿



機能は思いつく限り追加していく予定です

また、このコードは機能を充実させるため、以下のライブラリを使用しています。

openai, deepl


＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿

最近では質問以外にもGPTが活用される例が散見されます。
その流れにも対応したものにしようと思い、本機能を追加しました

GPTに渡す初期プロンプトの内容を変更できるうようになりました。
標準では英語でプロンプトが渡される仕様のため、日本語で入力した場合は翻訳が必要となっています。
そのため、プロンプトの指定後に、日本語で入力したかどうかをユーザーに質問し、翻訳が入るか入らないか変化するようになっています。
ゆくゆくは自動化したいのですが、とりあえずです。



＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿


_＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿_

・これまでの更新でモデルの変更機能や利用料金の計算など、自分でも覚えていないくらい色々機能を盛っています。
よくわからない記述やよくわからない機能があっても温かい目で見てください。

______________________________________________



Dai-H15 


