import requests
import os
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import pdfplumber
from flask import jsonify
from transformers import BartTokenizer

load_dotenv()


def extract_text_from_pdf(pdf_file):
    """
    Extract text from the PDF file
    :param pdf_file: Uploaded PDF file
    :return: Extracted text or error response
    """
    try:
        text = []

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    # Attempt to normalize spaces
                    cleaned_text = " ".join(page_text.split())
                    text.append(cleaned_text)

        if not text:
            return jsonify({'error': 'No text found in the PDF.'}), 400
        return "\n".join(text)

    except Exception as e:
        return jsonify({'error': f'Failed to process PDF: {str(e)}'}), 500


def split_text_into_chunks(text, max_chunk_size=4900):
    """
    Splits the input text for the translation into chunks of up to max_chunk_size characters
    without splitting words.

    :param text: The input text to be translated
    :param max_chunk_size: Maximum size of each chunk (default is 4900 characters as GoogleTranslate max limit is 5000)
    :return: A list of text chunks
    """
    chunks = []
    text_length = len(text)
    start = 0

    while start < text_length:
        # Determine the end index of the chunk
        end = min(start + max_chunk_size, text_length)

        # If the end is in the middle of a word, backtrack to the last space
        if end < text_length and text[end] != " ":
            space_index = text.rfind(" ", start, end)
            if space_index != -1:  # Found a space
                end = space_index
            # If no space is found, the chunk will be cut at max_chunk_size

        # Append the chunk and move the start index
        chunks.append(text[start:end])
        start = end + 1  # Move to the next character after the space

    return chunks


def chunk_text_by_tokens(text, max_tokens=900):
    """
    Chunk the text into smaller parts based on the max_tokens
    :param text: translated text
    :param max_tokens: maximum tokens to process at a time
    :return:
    """
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    tokens = tokenizer.encode(text)
    for i in range(0, len(tokens), max_tokens):
        chunk_ids = tokens[i: i + max_tokens]
        yield tokenizer.decode(chunk_ids, skip_special_tokens=True)


HF_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


def query(payload):
    """
    Query the Hugging Face Inference API to summarize the text
    :param payload: input payload for the API
    :return: response.json()
    """
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)

    return response.json()


# DeepL API Configuration
API_KEY = os.getenv("DL_API_KEY")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY = API_KEY


def translate_with_API(text, target_lang, translator="Google"):
    # Translate text using DeepL API
    translated_text = None
    error_message = None

    if translator == "DeepL":
        try:
            print("Using the DeepL Free API (limited)")
            response = requests.post(
                DEEPL_API_URL,
                data={
                    'auth_key': DEEPL_API_KEY,
                    'text': text,
                    'target_lang': target_lang.upper()
                },
                timeout=10
            )
            response.raise_for_status()
            translated_text = response.json().get('translations', [{}])[0].get('text', '')

        except requests.exceptions.RequestException as e:
            print(f"DeepL translation failed: {str(e)}")

    elif translator == "Google":
        try:
            print("Using the GoogleTranslate API")
            # %%
            translator = GoogleTranslator(source='auto', target=target_lang.lower())
            results = []
            chunks = split_text_into_chunks(text)
            for i, chunk in enumerate(chunks):
                print(f"Processing chunk {i + 1}/{len(chunks)}...")
                result = translator.translate(chunk)
                results.append(result)

            translated_text = " ".join(results)
        except Exception as e:
            return jsonify({'error': f'GoogleAPI translation failed: {str(e)}'}), 500
    if translated_text:
        print("TRANSLATION SUCCESSFUL")
        return translated_text, {'original_text': text, 'translated_text': translated_text}
    else:
        print("TRANSLATION FAILED")
        return jsonify({'error': 'Translation failed'}), 500
