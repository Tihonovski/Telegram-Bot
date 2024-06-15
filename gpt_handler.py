# gpt_handler.py
import openai
from config import OPENAI_API_KEY
from web_search import search_web

openai.api_key = OPENAI_API_KEY

def detect_language(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a language detection assistant."},
            {"role": "user", "content": f"Detect the language of the following text: {text}"}
        ],
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.0,
    )
    language = response.choices[0].message['content'].strip()
    return language

def gpt_response(prompt, language):
    search_results = search_web(prompt)
    search_text = "\n".join(search_results)

    gpt_prompt = f"""Answer the following query in {language} based on these search results:
    Query: {prompt}
    Search Results:
    {search_text}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that answers questions based on the provided search results in {language}."},
            {"role": "user", "content": gpt_prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].message['content'].strip()
