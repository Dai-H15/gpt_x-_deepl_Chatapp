import openai,deepl

def set_apikey():
    openai.api_key = "any"
    openai.api_base = "any"
    translator = deepl.Translator("any")
    
    return translator
    

