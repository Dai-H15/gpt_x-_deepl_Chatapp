import openai
import json
import os
import deepl


def init():  # 初期化
    print("初期化を開始します。\n")
    question = ""
    messages = [{"role": "system", "content": "You are a helpful assistant. Also you are super engineer.You can answer all questions."}]
    raw_mode = False
    translator = deepl.Translator("any")
    error = 0
    using_model = "gpt-3.5-turbo"
    models = []
    max_token = 4096
    finish_reason = ""
    EOT = False
    per_token_c = 0
    per_token_i = 0
    prompt_tokens = 0
    completion_tokens = 0
    total_m = 0

    try:
        from api_keys import set_apikey
        print("api_keysを検出しました。APIキーを読み込みます。\n")
        translator = set_apikey()
        try:
            openai.Model.retrieve("gpt-3.5-turbo")
            print("openAI APIの読み込みに成功しました。gpt-3.5-turboが使用可能です。\n")
            models.append(using_model)
            per_token_c = 0.002
            per_token_i = 0.0015
            print("現在のベースURLは '{}' です\n".format(openai.api_base))
            error_openAI = False

        except openai.error.AuthenticationError:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: openAI API設定が無効です。(AuthenticationError)\nsettingsから指定してください\n")
            print(" ----------\n ( 情報 ) \n ----------\n現在のベースURLは '{}' です\n".format(openai.api_base))
            error_openAI = True
        except openai.error.PermissionError:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: openAI API設定が無効です。(PermissionError)\nsettingsから指定してください\n")
            error_openAI = True
        except openai.error.InvalidRequestError:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: openAI API設定が無効です。(InvalidRequestError)\nsettingsから指定してください\n")
            error_openAI = True
        except openai.error.APIConnectionError:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: openAI APIにアクセスできません。(APiconnectionError)\nsettingsから指定してください\n")
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
        except deepl.exceptions.ConnectionException:
            print(" ----------\n ( 警告 ) \n ----------\nエラー: DeepLにアクセスできません。接続が無効、もしくはホストがダウンしています。")
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

    import_ans = input("今までの会話内容をインポートしますか？ :yes/no :")
    while True:
        if import_ans == "yes":
            while True:
                import_ans_num = input("インポートするデータの番号を入力してください。(1~3)\n ==>")
                try:
                    if 1 <= int(import_ans_num) <= 3:
                        break
                    print("番号が範囲外です。")
                except ValueError:
                    print("正しく入力してください。")
                    continue

            try:
                prompt = import_prompt(import_ans_num)

                # 以前の会話内容の表示
                if input("プロンプトをインポートしました。以前の会話内容を表示しますか？ :yes/no :") == "yes":
                    for pr in prompt:
                        print("________________________________________________________________________________________________\n")
                        print("Role :  \n", pr["role"])
                        print("\n", pr["content"])
                        print("________________________________________________________________________________________________\n")
                    print("\n----------\n ( 情報 ) \n ----------\n表示されたプロンプトが、日本語を含んでいる場合、以降の操作はrawモードを有効にして実行するか、新規内容で続行する必要があります。くわしくは各ヘルプを参照してください。\n")
                print("\n")
                another_prompt = input("他のスロットのデータを読み込みますか? yes/no \n ==>")
                if another_prompt == "yes":
                    continue
                elif another_prompt == "no":
                    for p in prompt:
                        messages.append(p)
                    return (question, messages, raw_mode, translator, error_openAI, error_DeepL, error, using_model, models,
                            max_token, finish_reason, EOT, per_token_c, per_token_i, prompt_tokens, completion_tokens, total_m)
                else:
                    print("正しく入力してください。")
                    continue
            # ファイルが存在しない場合
            except FileNotFoundError:
                print("ファイルが存在しないため、新規内容で開始します。\n")

            # インポートせずに新規内容で開始

        elif import_ans == "no":
            print("新規内容で開始します\n")
        else:
            print("想定外の内容が入力されました")
            error = 1
        print("処理が完了しました。\n")
        return (question, messages, raw_mode, translator, error_openAI, error_DeepL, error, using_model, models,
                max_token, finish_reason, EOT, per_token_c, per_token_i, prompt_tokens, completion_tokens, total_m)


def export_prompt(prompt, export_ans_num):
    with open('prompt_' + export_ans_num + '.data', 'w') as f:
        json.dump(prompt, f)


def import_prompt(num):
    if os.path.exists('prompt_' + num + '.data'):
        with open('prompt_' + num + '.data', 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError("プロンプトファイルが存在しません")


def one(error_openAI, error_DeepL, EOT, raw_mode, translator, question):
    error = 0
    if (error_openAI or error_DeepL) is True:
        print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
        error = 1
        return question, error
    if EOT:
        print("----------\n ( 情報 ) \n ----------\nトークン数の上限に達しました。新規内容から開始してください。\nまた、printコマンドから内容の書き出しを利用できます。\n")
        error = 1
        return question, error

    user_question = input("質問を入力してください  exitでコマンド入力に戻る: ")
    if user_question == "":
        print("内容を確認できませんでした。\n")
        error = 1
    if user_question == "exit":
        user_question = ""
        print("コマンド入力画面に戻ります\n")
        error = 1

    else:
        if raw_mode is False:
            question = translator.translate_text(user_question, target_lang="EN-US")
            print("\n言語処理が完了しました\n")
        else:
            question = user_question
            print("rawモードが有効です")

    return question, error


def mult(error_openAI, error_DeepL, EOT, raw_mode, translator, question):
    error = 0
    end = 0
    if (error_openAI or error_DeepL) is True:
        print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
        error = 1
        return question, error

    if EOT:
        print("----------\n ( 情報 ) \n ----------\nトークン数の上限に達しました。新規内容から開始してください。\nまた、printコマンドから内容の書き出しを利用できます。\n")
        error = 1
        return question, error

    while end == 0:
        user_question = input("質問を入力してください(end)で入力終了,exitでプログラムを終了: ")
        if user_question == "exit":
            print("\n")
            user_question = ""
            end = 2
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
    if end == 2:
        print("コマンド入力画面に移行します\n")
        end = 0
        error = 1
        return question, error
    else:
        end = 0
        return question, error


def save(raw_mode, messages, EOT):
    if EOT:
        print("----------\n ( 情報 ) \n ----------\nトークン数の上限に達しました。プロンプトを保存できません。printコマンドから内容の書き出しを行ってください。")
        return
    print("会話内容をファイルにエクスポートします。次回以降にインポートすることで会話を続けることができます。\n")
    while True:
        export_num = input("保存するスロットを選択してください。(1~3) \n ==>")
        if 1 <= int(export_num) <= 3:
            break
        else:
            print("範囲外の数値が入力されました。")
    if raw_mode is False:

        export_prompt(messages[1:], export_num)
    else:
        print("----------\n ( 警告 ) \n ----------\nrawモードが有効化されています。次回以降の動作時に詳細設定からrawモードを有効化する必要があります。\n")
        export_prompt(messages[1:], export_num)
    print("完了しました。")


def info(error_openAI, error_DeepL, translator, using_model, max_token, total_m, prompt_tokens, completion_tokens, per_token_c, per_token_i):
    if (error_openAI or error_DeepL) is True:
        print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
        return
    print("処理が完了しました。\n__________\n\n使用されるモデル: "+using_model+"\n最大トークン数: "+str(max_token)+"\n会話生成時利用料金: $"+str(per_token_c)+"\nプロンプト入力時利用料金: $"+str(per_token_i)+"\n")

    print("現在消費しているトークン数：{}/{}  使用率: {} % \n".format(prompt_tokens+completion_tokens, max_token, round((prompt_tokens+completion_tokens)/max_token, 3)*100))
    print("現在の概算利用金額: ${} \n".format(total_m/1000))
    x = translator.get_usage().character
    print("DeepLアカウントの使用状況: {}/{} 使用率:  {} % \n__________\n\n".format(x.count, x.limit, round(x.count/x.limit*100, 2)))


def settings(error_openAI, error_DeepL, raw_mode, translator, messages, using_model, models, max_token, per_token_c, per_token_i):
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
                print("\n________________\n\nAPI設定メニュー\n\n1: openai.api_keyの変更\n2: openai.api_baseの変更\n3: 使用するモデルの変更\n4: DeepLAPIキーの変更 \nexit: 設定メニューにもどる\n")
                try:
                    openai.Model.retrieve(using_model)
                    error_openAI = False
                    print(using_model + "が使用可能です")
                except openai.error.PermissionError:
                    error_openAI = True
                    print("openAI にアクセスできません。権限がないAPIキーです")
                except openai.error.AuthenticationError:
                    error_openAI = True
                    print("openAI にアクセスできません。無効なAPIキー、もしくはURLとの組み合わせが無効です")
                except openai.error.InvalidRequestError:
                    error_openAI = True
                    print("openAI にアクセスできません。不正なURL、もしくは無効なモデルが選択されています")
                except openai.error.APIConnectionError:
                    print("openAI にアクセスできません。接続が無効、もしくはホストがダウンしています。")
                    error_openAI = True
                except openai.error.APIError:
                    print("openAI にアクセスできません。設定されたURLから無効な応答が返されました。")
                    error_openAI = True
                except openai.error.APIConnectionError:
                    print("openAI APIにアクセスできません。(APiconnectionError) 接続が無効、もしくはホストがビジー状態です\n")
                    error_openAI = True
                except openai.error.RateLimitError:
                    print("openAI APIにアクセスできません。レートリミットに達しました。しばらく待ってからやり直してください。")
                    error_openAI = True
                print(" ----------\n ( 情報 ) \n ----------\n現在のベースURLは '{}' です\n".format(openai.api_base))
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
                except deepl.exceptions.ConnectionException:
                    print("DeepLにアクセスできません。接続が無効、もしくはホストがダウンしています。")
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
                    try:
                        print("使用したいモデルを選択してください。")
                        num = 0
                        for x in models:
                            print(num, x)
                            num += 1
                        print(num, "新しく追加")
                        want_model = input("==>")
                        want_model_num = int(want_model)
                    except ValueError:
                        print("不正な入力です。")
                        continue

                    if want_model_num == num:
                        search_model = input("使用したいモデル名を正確に入力してください。exitで中止\n==>")
                        if search_model == "exit":
                            print("API設定メニューに戻ります")
                            continue

                        for s in models:
                            if s == search_model:
                                print("そのモデルはリストに登録済みです。\n")
                                break
                        else:
                            try:
                                openai.Model.retrieve(search_model)
                                print("\n"+search_model+"は利用可能です。\n")
                                print("リストに追加し、使用するモデルとして登録します。\n")
                                try:
                                    user_token_input = input("対象のモデルの最大トークン数を入力してください。\n==>")
                                    max_token = int(user_token_input)
                                    user_per_token_c_input = input("対象のモデルの会話生成時トークン数1kあたりの利用料金をドル単位で入力してください。\n==>")
                                    per_token_c = float(user_per_token_c_input)
                                    user_per_token_i_input = input("対象のモデルのプロンプト入力時トークン数1kあたりの利用料金をドル単位で入力してください。\n==>")
                                    per_token_i = float(user_per_token_i_input)

                                except ValueError:
                                    print("不正な入力です。設定は変更されませんでした。\n")
                                    continue
                                models.append(search_model)
                                using_model = search_model

                                print("処理が完了しました。\n__________\n使用されるモデル: "+using_model+"\n最大トークン数: "+str(max_token)+"\n会話生成時利用料金: $"+str(per_token_c)+"\nプロンプト入力時利用料金: $"+str(per_token_i)+"\n__________\nAPI設定メニューに戻ります。\n")
                                continue
                            except openai.error.APIConnectionError or openai.error.AuthenticationError:
                                print("エラーが発生しました。各設定、書式を確認してください。設定は変更されませんでした。\n")
                                continue
                            except openai.error.InvalidRequestError:
                                print("無効なモデル名です。再度入力してください。")
                                continue
                    elif want_model_num < num:
                        try:
                            print("使用するモデルを"+models[want_model_num]+"に変更します。\n")
                            user_token_input = input("対象のモデルの最大トークン数を入力してください。\n==>")
                            max_token = int(user_token_input)
                            user_per_token_c_input = input("対象のモデルの会話生成時トークン数1kあたりの利用料金をドル単位で入力してください。\n==>")
                            per_token_c = float(user_per_token_c_input)
                            user_per_token_i_input = input("対象のモデルのプロンプト入力時トークン数1kあたりの利用料金をドル単位で入力してください。\n==>")
                            per_token_i = float(user_per_token_i_input)
                            using_model = models[want_model_num]
                            print("変更が完了しました。\n")
                            continue
                        except ValueError:
                            print("不正な入力です。設定は変更されませんでした。")
                            continue
                    else:
                        print("不正な入力です。")
                        break

                elif u_api == "4":
                    print("Deepl APIのAPIキーを変更します。")
                    deepl_key = input("APIキーを貼り付けてください\n>>> ")
                    try:
                        translator = deepl.Translator(deepl_key)
                        print("APIキーの変更に成功しました。DeepLを使用した翻訳が可能です。")
                        continue
                    except ValueError:
                        print("無効なAPIキーです。再度設定し直してください。")
                        continue

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
                print("英語に翻訳しますか?")
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
    return error_openAI, error_DeepL, raw_mode, translator, messages, using_model, models, max_token, per_token_c, per_token_i


def view(messages):
    print("\n会話内容を表示します。\n")
    for message in messages[1:]:
        print("________________________________________________________________________________________________\n")
        print("Role :  \n", message["role"])
        print("\n", message["content"])
        print("________________________________________________________________________________________________\n")
    print("\n")


def translate(error_openAI, error_DeepL, raw_mode, translator, messages):
    if (error_openAI or error_DeepL) is True:
        print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
        return
    if raw_mode is True:
        print("rawモードが有効化されています。本機能を実行することができません。")
        return

    print(" ----------\n ( 警告 ) \n ----------\nこの操作はDeepLのトークン数を大量に消費するため、推奨されません。可能であれば他の製品の翻訳機能を使用することを推奨します。また、通信状況によっては時間がかかるおそれがあります")
    user = input("それでも実行しますか？  yes/no :")
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
        return
    else:
        print("トップに戻ります。")
        return


def print_talk(error_openAI, error_DeepL, raw_mode, translator, messages):
    if (error_openAI or error_DeepL) is True:
        print("----------\n ( 警告 ) \n ----------\n設定が無効です。API設定を確認してください\n___________________________\n")
        return
    print("talkフォルダーを作成し、会話内容を.txtファイル形式で保存します。\n")
    os.makedirs("talk", exist_ok=True)
    while True:
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
                for message in messages:
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


def make_answer(raw_mode, translator, messages, question, using_model):
    print("ただいま考え中～\n")
    messages.append({"role": "user", "content": f"{question}"})
    try:
        response = openai.ChatCompletion.create(
            model=using_model,
            messages=messages

            )
    except openai.error.InvalidRequestError:
        print("----------\n ( 警告 ) \n ----------\nエラーが発生しました。モデルを変更した場合、使用許可がされていないモデルの可能性があります。APIキー、URLを変更するか、管理者に問い合わせてください。\n")
        messages = messages[:-1]
        return messages, "", 0, 0
    if raw_mode is False:
        print("翻訳中~\n")
        result = translator.translate_text(response['choices'][0]['message']['content'], target_lang="JA")

    else:
        print("----------\n ( 情報 ) \n ----------\nrawモードが有効化されています。\n")
        result = response['choices'][0]['message']['content']

    print("ok!")

    messages.append({"role": response['choices'][0]['message']['role'], "content": response['choices'][0]['message']['content']})

    finish_reason = response["choices"][0]["finish_reason"]

    print("________________________________________________________________________________________________\n")
    print("A:\n", result)

    print("________________________________________________________________________________________________\n")
    prompt_tokens = response["usage"]["prompt_tokens"]
    completion_tokens = response["usage"]["completion_tokens"]

    return messages, finish_reason, prompt_tokens, completion_tokens


def ask_gpt():
    print("____________________\n\nコマンドプロンプト上で簡単にChatGPTの操作ができるしトークン数の節約をしながら記憶の半永久保存も簡単にできるくん ver.7.5.5 \n\nmade_by :Dai-H15  s1f102200828@iniad.org\n____________________\n")

    # 初期化
    question, messages, raw_mode, translator, error_openAI, error_DeepL, error, using_model, models, max_token, finish_reason, EOT, per_token_c, per_token_i, prompt_tokens, completion_tokens, total_m = init()
    if error == 1:
        print("プログラムを終了します。")
        return
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
        if EOT:
            print("----------\n ( 情報 ) \n ----------\nトークン数の上限に達しました。新規内容から開始してください。")

        print("rawモード :", print_raw)
        input_type = input("\nコマンドを選択してください: ")

        # 1行のみ質問を入力
        if input_type == "one":
            question, error = one(error_openAI, error_DeepL, EOT, raw_mode, translator, question)
            if error == 1:
                error = 0
                continue
        # 複数行の質問の入力。実際は繋げてるだけ
        elif input_type == "mult":
            question, error = mult(error_openAI, error_DeepL, EOT, raw_mode, translator, question)
            if error == 1:
                error = 0
                continue

        # 会話内容のエクスポート

        elif input_type == "save":
            save(raw_mode, messages, EOT)
            continue
            # 会話内容を初期化

        elif input_type == "new":
            messages = [{"role": "system", "content": "You are a helpful assistant. Also you are super engineer.You can answer all questions."}]
            print("会話内容をリセットしました。\n")
            continue

        elif input_type == "info":
            info(error_openAI, error_DeepL, translator, using_model, max_token, total_m, prompt_tokens, completion_tokens, per_token_c, per_token_i)
            continue

        elif input_type == "settings":
            error_openAI, error_DeepL, raw_mode, translator, messages, using_model, models, max_token, per_token_c, per_token_i = settings(error_openAI, error_DeepL, raw_mode, translator, messages, using_model,
                                                                                                                                           models, max_token, per_token_c, per_token_i)
            continue

        elif input_type == "view":
            view(messages)
            continue

        elif input_type == "translate":
            translate(error_openAI, error_DeepL, raw_mode, translator, messages)
            continue

        elif input_type == "exit":
            print("Seeyou :)")
            break
        # その他コマンドを入力された場合にもどる

        elif input_type == "help":
            print("コマンド  \none:一文のみ入力 \nmult:連続入力  \nsave:プロンプトをエクスポートして終了 \nnew:会話を新しくやり直す \ninfo:現在のトークン数を表示(インポート直後は無効) \nview:会話内容を全表示 \ntranslate:会話内容を日本語化して表示 \nexit:保存せずに終了 \nreload:アプリを再起動 \nsettings:詳細設定を表示 \nprint:テキストファイル形式で会話内容を出力\n ")
            continue

        elif input_type == "print":
            print_talk(error_openAI, error_DeepL, raw_mode, translator, messages)
            continue

        elif input_type == "reload":
            print("再度読み込み直します。保存されていない情報は消えますがよろしいですか？(yes / no )\n")
            if input("==>") == "yes":
                for _ in range(50):
                    print("\n")
                question, messages, raw_mode, translator, error_openAI, error_DeepL, error, using_model, models, max_token, finish_reason, EOT, per_token_c, per_token_i, prompt_tokens, completion_tokens, total_m = init()
                continue
            else:
                print("コマンド入力画面に戻ります。")
                continue

        else:
            print("正しいコマンドを入力してください  help でコマンド例を表示\n")
            continue

        # 回答を生成・表示
        messages, finish_reason, prompt_tokens, completion_tokens = make_answer(raw_mode, translator, messages, question, using_model)
        if finish_reason == "length":
            EOT = True

        total_m += prompt_tokens*per_token_i + completion_tokens*per_token_c
        continue


ask_gpt()
