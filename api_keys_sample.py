"""Import libraries"""

import deepl
from openai import OpenAI


def set_apikey():
    client = OpenAI(api_key="any", base_url="any")
    translator = deepl.Translator("any")
    return translator, client
