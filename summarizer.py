import spacy
from collections import Counter

def extract_keywords(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = [token.lemma_ for token in doc if token.is_stop == False and token.is_punct == False]
    keyword_freq = Counter(keywords)
    return keyword_freq.most_common(10)

async def generate_summary(chatgpt, keywords):
    prompt = f"Resumir un chat de Twitch con las siguientes palabras clave: {', '.join(keywords)}"
    summary = await chatgpt.generate_response(prompt)
    return summary
