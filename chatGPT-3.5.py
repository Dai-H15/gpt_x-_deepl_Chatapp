import openai
import json
import os
import deepl


def export_prompt(prompt):
    with open('prompt.data', 'w') as f:
        json.dump(prompt, f)


def import_prompt():
    if os.path.exists('prompt.data'):
        with open('prompt.data', 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError("プロンプトファイルが存在しません")


def ask_gpt():
    print("____________________\n\nコマンドプロンプト上で簡単にChatGPTの操作ができるしトークン数の節約をしながら記憶の半永久保存も簡単にできるくん ver.6.9.2 \n\nmade_by :Dai-H15  s1f102200828@iniad.org\n____________________\n")

    # 初期化
    question = ""
    messages = [{"role": "system", "content": "You are a helpful assistant. Also you are super engineer.You can answer all questions."}]
    user_question = ""
    total = 0
    raw_mode = False
    translator = deepl.Translator("any")
    end = 0

    try:

        from api_keys import set_apikey
        print("api_keysを検出しました。APIキーを読み込みます。\n")
        translator = set_apikey()
        try:
            openai.Model.retrieve("gpt-3.5-turbo")
            print("openAI APIの読み込みに成功しました。gpt-3.5-turboが使用可能です。\n")
            print("現在のベースURLは '{}' です\n".format(openai.api_base))
            error_openAI = False

        except openai.error.AuthenticationError:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: openAI API設定が無効です。settingsから指定してください\n")
            error_openAI = True
        except openai.error.PermissionError:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: openAI API設定が無効です。settingsから指定してください\n")
            error_openAI = True
        except openai.error.InvalidRequestError:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: openAI API設定が無効です。settingsから指定してください\n")
            error_openAI = True
        try:
            translator.get_usage().character
            print("DeepL APIの読み込みに成功しました。DeepLによる自動翻訳が使用可能です。\n")
            error_DeepL = False
        except deepl.exceptions.AuthorizationException:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: DeepL API設定が無効です。settingsから指定してください\n")
            error_DeepL = True
        except ValueError:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: DeepL API設定が無効です。settingsから指定してください\n")
            error_DeepL = True
    except openai.error.AuthenticationError:
        print(" ----------\n ( 警告 ) \n ----------\nAPIキーの読み込みに失敗しました。settingsから指定してください。\n")
        print(" ----------\n ( 情報 ) \n ----------\n現在のベースURLは '{}' です\n".format(openai.api_base))
        error_openAI = True
        error_DeepL = True
    except ImportError:
        print(" ----------\n ( 警告 ) \n ----------\nエラー: api_keysの書式が不正な可能性があります。各APIキーをsettingsから指定してください")
        error_openAI = True
        error_DeepL = True
    # 会話内容のインポート
    import_ans = input("今までの会話内容をインポートしますか？ :yes/no  :")

    if import_ans == "yes":
        try:
            prompt = import_prompt()

            # 以前の会話内容の表示
            if input("プロンプトをインポートしました。以前の会話内容を表示しますか？ :yes/no :") == "yes":
                for pr in prompt:
                    print("________________________________________________________________________________________________\n")
                    print("Role :  \n", pr["role"])
                    print("\n", pr["content"])
                    print("________________________________________________________________________________________________\n")
                print("\n----------\n ( 情報 ) \n ----------\n表示されたプロンプトが、日本語を含んでいる場合、以降の操作はrawモードを有効にして実行するか、新規内容で続行する必要があります。くわしくは各ヘルプを参照してください。\n")
            print("\n")
            for pr in prompt:
                messages.append(pr)
            else:
                print("コマンド入力画面に移行します\n")
        # ファイルが存在しない場合
        except FileNotFoundError:
            print("ファイルが存在しないため、新規内容で開始します。\n")

        # インポートせずに新規内容で開始

    elif import_ans == "no":
        print("新規内容で開始します\n")
    else:
        print("想定外の内容が入力されました")
        return 1

    print("________________________________________________________________________________________________\n")

    # 会話生成本体
    while True:

        # 条件分岐
        if raw_mode is True:
            print_raw = "有効"
        else:
            print_raw = "無効"
        if error_openAI:
            print("OpenAI API設定エラー settingsからセットアップしてください")
        if error_DeepL:
            print("DeepL APIの設定エラー settingsからセットアップしてください")

        print("rawモード :", print_raw)
        input_type = input("\nコマンドを選択してください: ")

        # 1行のみ質問を入力
        if input_type == "one":
            if (error_openAI or error_DeepL) is True:
                print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
                continue
            user_question = input("質問を入力してください  exitでコマンド入力に戻る: ")
            if user_question == "":
                print("内容を確認できませんでした。\n")
                continue
            if user_question == "exit":
                user_question = ""
                print("\n")
                continue
            else:
                if raw_mode is False:
                    question = translator.translate_text(user_question, target_lang="EN-US")
                    print("\n言語処理が完了しました\n")
                else:
                    question = user_question
                    print("rawモードが有効です")
        # 複数行の質問の入力。実際は繋げてるだけ
        elif input_type == "mult":
            if (error_openAI or error_DeepL) is True:
                print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
                continue
            while end == 0:
                user_question = input("質問を入力してください(end)で入力終了,exitでプログラムを終了: ")
                if user_question == "exit":
                    print("\n")
                    user_question = ""
                    end = 1
                if user_question == "end":
                    end = 1
                    user_question = ""
                if raw_mode is True:
                    print("rawモードがオンです。")
                    question += (user_question+" \n ")
                    user_question = ""
                    continue
                if raw_mode is False:
                    if user_question == "":
                        continue
                    print("rawモードはオフです。\n翻訳中...")
                    tra_q = translator.translate_text(user_question, target_lang="EN-US")
                    question += str(tra_q)
                    user_question = ""
                    continue
            user_question = ""
            end = 0


        # 会話内容のエクスポート

        elif input_type == "save":
            print("会話内容をファイルにエクスポートします。次回以降にインポートすることで会話を続けることができます。\n")
            if raw_mode is False:

                export_prompt(messages[1:])
            else:
                print("----------\n ( 警告 ) \n ----------\nrawモードが有効化されています。次回以降の動作時に詳細設定からrawモードを有効化する必要があります。\n")
                export_prompt(messages[1:])
            print("完了しました。")

            continue
            # 会話内容を初期化

        elif input_type == "new":
            messages = [{"role": "system", "content": "You are a helpful assistant. Also you are super engineer.You can answer all questions."}]
            print("会話内容をリセットしました。\n")
            total = 0
            continue

        elif input_type == "info":
            if (error_openAI or error_DeepL) is True:
                print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
                continue
            print("現在消費しているトークン数：{}/4097  使用率: {} % \n".format(total, round(total/4097, 3)*100))
            x = translator.get_usage().character
            print("DeepLアカウントの使用状況: {}/{} 使用率:  {} % \n".format(x.count, x.limit, round(x.count/x.limit*100, 2)))
            continue

        elif input_type == "settings":
            while True:
                print("\n________________\n\n変更する設定を選んでください\n 1.自動翻訳機能(rawモード)\n 2.API設定\n 3.初期プロンプトの指定\n exit:設定を終了\n ")
                u_type = input(">>>")
                if u_type == "1":
                    print("このプログラムは、ChatGPTにおけるトークン数の消費量削減のために、送信時、受信時に適した状態にする機能が搭載されています。\nしかし、ソースコードを送信する際や、使用しているAPIは自動翻訳のため、意図した回答が得られない状況が発生するおそれがあります。通常はこの機能を有効にしておくことをおすすめしますが、こういった状況に陥った場合にオフにすることも可能です")
                    print("\n既定の設定では自動翻訳が有効化されているため、rawモードは無効になっています")
                    tra_inp = input("rawモードを有効にしますか？ yes/no : ")
                    if tra_inp == "no":
                        raw_mode = False
                        print("rawモードが無効化されました\n")
                        continue
                    elif tra_inp == "yes":
                        raw_mode = True
                        print("rawモードが有効化されました。トークン数にご注意ください。\n")
                        print(" ----------\n ( 情報 ) \n ----------\n本設定を有効にすると、以降保存されるプロンプトも翻訳されずに追記されていくので注意してください。\n________________________________________________\n")

                    else:
                        print("予期しない入力を受け付けました。トップに戻ります\n")

                elif u_type == "2":
                    while True:
                        print("\n________________\n\nAPI設定メニュー\n\n1: openai.api_keyの変更\n2: openai.api_baseの変更\n3: DeepLAPIキーの変更 \nexit: 設定メニューにもどる\n")
                        try:
                            openai.Model.retrieve("gpt-3.5-turbo")
                            error_openAI = False
                            print("gpt-3.5-turboが使用可能です")
                        except openai.error.PermissionError:
                            error_openAI = True
                            print("openAI にアクセスできません。権限がないAPIキーです")
                        except openai.error.AuthenticationError:
                            error_openAI = True
                            print("openAI にアクセスできません。無効なAPIキー、もしくはURLとの組み合わせが無効です")

                        except openai.error.InvalidRequestError:
                            error_openAI = True
                            print("openAI にアクセスできません。不正なURLです")
                        except openai.error.APIConnectionError:
                            print("openAI にアクセスできません。不正なURLです")
                            error_openAI = True
                        except openai.error.APIError:
                            print("openAI にアクセスできません。設定されたURLから無効な応答が返されました。")
                            error_openAI = True
                        try:
                            translator.get_usage().character
                            print("DeepLが使用可能です")
                            error_DeepL = False
                        except deepl.exceptions.AuthorizationException:
                            print("DeepLにアクセスできません。無効なDeepLAPIキーが設定されています。")
                            error_DeepL = True
                        except ValueError:
                            print("DeepLにアクセスできません。無効なDeepLAPIキーが設定されています。")
                            error_DeepL = True
                        u_api = input("\n項目を選択してください\n>>>")

                        if u_api == "1":
                            print("OpenAI APIのAPIキーを変更します。")
                            openai_key = input("\napi_keyを貼り付けてください\n>>> ")
                            openai.api_key = openai_key
                            print("APIキーの変更に成功しました。")
                            continue

                        elif u_api == "2":
                            openai_base = input("\nopenai.api_baseとして指定するURLを入力してください。\n>>> ")
                            openai.api_base = openai_base
                            print("openai.api_baseの変更に成功しました。")
                            continue

                        elif u_api == "3":
                            print("Deepl APIのAPIキーを変更します。")
                            deepl_key = input("APIキーを貼り付けてください\n>>> ")
                            try:
                                translator = deepl.Translator(deepl_key)
                                print("APIキーの変更に成功しました。DeepLを使用した翻訳が可能です。")
                                continue
                            except ValueError:
                                print("無効なAPIキーです。再度設定し直してください。")

                        elif u_api == "exit":
                            print("トップメニューに戻ります。\n")
                            break

                        else:
                            print("\n予期しない入力がされました。")
                        print("API設定メニューに戻ります\n")

                    continue

                elif u_type == "3":
                    print("初めにGPTに渡すプロンプトの内容を変更できます。\n")
                    u_prompt = input("新しく設定するプロンプトを入力してください。'default'と入力することで初期状態に戻すことができます。\n >>>")
                    if u_prompt == "default":
                        messages[0] = {"role": "system", "content": "You are a helpful assistant. Also you are super engineer.You can answer all questions."}
                        print("初期状態に戻りました。\n")
                        print("settingsメニューに戻ります。")
                        continue

                    else:
                        print("日本語で入力しましたか?")
                        u_lang = input("yes/no \n>>>")
                        if u_lang == "yes":
                            print("翻訳してから変更されます。\n")
                            messages[0] = {"role": "system", "content": "{}".format(translator.translate_text(u_prompt, target_lang="EN-US"))}

                        elif u_lang == "no":
                            messages[0] = {"role": "system", "content": "{}".format(u_prompt)}

                        print("正常に変更されました。\n")
                        print("現在の初期プロンプトは、'{}'\n".format(messages[0]["content"]))
                        print("settingsメニューに戻ります。")
                        continue

                elif u_type == "exit":
                    print("コマンド入力に戻ります。\n")
                    break
                else:
                    print("予期しない入力がされました。\n")
            continue

        elif input_type == "view":
            print("\n会話内容を表示します。\n")
            for message in messages[1:]:
                print("________________________________________________________________________________________________\n")
                print("Role :  \n", message["role"])
                print("\n", message["content"])
                print("________________________________________________________________________________________________\n")
            print("\n")
            continue

        elif input_type == "translate":
            if (error_openAI or error_DeepL) is True:
                print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
                continue
            if raw_mode is True:
                print("rawモードが有効化されています。本機能を実行することができません。")
                continue

            print(" ----------\n ( 警告 ) \n ----------\nこの操作はDeepLのトークン数を大量に消費するため、推奨されません。可能であれば他の製品の翻訳機能を使用することを推奨します。また、通信状況によっては時間がかかるおそれがあります")
            user = input("それでも実行しますか？  yes/no :\n")
            if user == "yes":
                print("________________________________________________________________________________________________\n")
                print("翻訳中・・・")
                print("________________________________________________________________________________________________\n")
                for message in messages[1:]:
                    data = translator.translate_text(message['content'], target_lang="JA")
                    print("________________________________________________________________________________________________\n")
                    print("Role :  \n", message["role"])
                    print("\n", data)
                    print("________________________________________________________________________________________________\n")
                    print("\n")
                print("\n完了しました")
                continue
            else:
                print("トップに戻ります。")
                continue

        elif input_type == "exit":
            user_question = "exit"
        # その他コマンドを入力された場合にもどる

        elif input_type == "help":
            print("コマンド  \none:一文のみ入力 \nmult:連続入力  \nsave:プロンプトをエクスポートして終了 \nnew:会話を新しくやり直す \ninfo:現在のトークン数を表示する(インポート直後は無効) \nview:会話内容を全表示する \ntranslate:会話内容を日本語化して表示する \nexit:保存せずに終了する \nsettings:詳細設定を表示する\nprint:テキストファイル形式で会話内容を出力します。\n")
            continue

        elif input_type == "print":
            if (error_openAI or error_DeepL) is True:
                print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
                continue
            print("talkフォルダーを作成し、会話内容を.txtファイル形式で保存します。\n")
            os.makedirs("talk", exist_ok=True)
            while (True):
                if raw_mode is False:
                    print("rawモードがオフになっています。内容を日本語化してから保存しますか？ yes/no")
                    tra_set = input("\n>>>")
                    if (tra_set != "yes") and (tra_set != "no"):
                        print("想定外の入力が発生しました\n")
                        continue
                else:
                    print("rawモードが有効化されています。自動翻訳は使用できません。\n")
                    tra_set = "no"

                print("設定を保存しました。")

                filename = input("ファイル名を指定してください : ")
                if filename == "":
                    print("ファイル名が入力されていません。\n")
                else:

                    with open("./talk/{}.txt".format(filename), "w") as f:
                        for message in messages[1:]:
                            print("書き込み中～\n")
                            f.write("________________________________________________________________________________________________\n")
                            f.write("Role : {}\n".format(message["role"]))
                            if tra_set == "no":
                                f.write("{}\n".format(message["content"]))
                            elif tra_set == "yes":
                                print("翻訳中~\n")
                                f.write("{}\n".format(translator.translate_text(message["content"], target_lang="JA")))
                            f.write("________________________________________________________________________________________________\n")
                            f.write("\n")
                            f.write("\n\n")

                        print("正常に書き込みが完了しました。日本語化した場合、Shift_JISで開くと正常に閲覧できます。\n")
                        break

            print("コマンド入力画面に戻ります。")
            continue

        else:
            print("正しいコマンドを入力してください  help でコマンド例を表示\n")
            continue

        # 質問内容に"exit"と入力された場合にも終了させる

        if user_question == "exit":
            print("Seeyou :)")
            return 0

        # 回答を生成・表示

        print("ただいま考え中～\n")
        messages.append({"role": "user", "content": f"{question}"})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        if raw_mode is False:
            print("翻訳中~\n")
            result = translator.translate_text(response['choices'][0]['message']['content'], target_lang="JA")

        else:
            print("----------\n ( 情報 ) \n ----------\nrawモードが有効化されています。\n")
            result = response['choices'][0]['message']['content']

        print("ok!")

        messages.append({"role": response['choices'][0]['message']['role'],
                         "content": response['choices'][0]['message']['content']})
        user_question = ""
        print("________________________________________________________________________________________________\n")
        print("A:\n", result)

        print("________________________________________________________________________________________________\n")
        total = response['usage']["total_tokens"]


ask_gpt()
