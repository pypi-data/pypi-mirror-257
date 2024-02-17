import openai
from rich.console import Console
import os
import time


def check_api_key_validity(api_key):
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    except openai.APITimeoutError:
        return False
    else:
        return True



