from flask import Flask, request, jsonify, render_template, session
import os
import time
from functions.ml_api_utils import chunk_text_by_tokens, query, translate_with_API, extract_text_from_pdf

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route('/')
def index():
    """
    Render the main page index.html template
    :return: rendered index.html template
    """
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    """
    Translate the text extracted from the PDF file using the GoogleTranslate API or DeepL API
    (As the GoogleTranslate API doesn't seem to have any limits, it's used by default)
    :return: translated_data
    """
    pdf_file = request.files['file']
    target_lang = request.form['target_lang']
    session['target_lang'] = target_lang

    # Extract text and translate
    text = extract_text_from_pdf(pdf_file)
    print("-------------------------- TRANSLATING TEXT -------------------------------")

    _, translated_data = translate_with_API(text, target_lang, translator="Google")
    print(translated_data)

    return jsonify(translated_data)


@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Summarize the translated text using the Hugging Face Inference API
    Implements retry logic in case the API returns a "too busy" response.
    :return: return jsonify({'summary': final_combined_summary})
    """
    translated_text = request.form['translated_text']
    target_lang = session.get('target_lang')

    # Translate the text back to English before summarization
    text_back_to_english, _ = translate_with_API(translated_text, "EN", translator="Google")

    print("-------------------------- CHUNKING TEXT BY TOKENS -------------------------------")

    chunks = list(chunk_text_by_tokens(text_back_to_english, max_tokens=900))

    print("-------------------------- STARTING SUMMARIZATION WITH HF INFERENCE API -------------------------------")
    summaries = []
    max_retries = 3  # Number of retry attempts
    wait_time = 5  # Wait time in seconds before retrying

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        payload = {"inputs": chunk, "parameters": {"truncation": True, "max_length": 1024}}

        retries = 0
        while retries < max_retries:
            summary = query(payload)

            if isinstance(summary, list) and all("summary_text" in item for item in summary):
                summaries.append(summary)
                break  # Successfully retrieved summary, move to the next chunk

            # If model is too busy, retry after waiting
            print(f"Model too busy, retrying in {wait_time} seconds... ({retries + 1}/{max_retries})")
            time.sleep(wait_time)
            retries += 1
        else:
            # If retries are exhausted, log error and return failure response
            print(f"Failed to summarize chunk {i + 1} after {max_retries} attempts.")
            return jsonify({'error': f"Summarization failed for chunk {i + 1}. Please try again later."}), 500

    combined_summary = " ".join(
        item["summary_text"] for summary in summaries for item in summary if "summary_text" in item
    )

    print("-------------------------- SUMMARIZATION SUCCESSFUL -------------------------------")
    print(f"Summaries List: {summaries}")

    # Translate the final summary back to the target language
    final_combined_summary, _ = translate_with_API(combined_summary, target_lang, translator="Google")

    print(f"Final Summary: {final_combined_summary}")
    return jsonify({'summary': final_combined_summary})


if __name__ == '__main__':
    app.run(port=5000, debug=False)
