from flask import Flask, request, jsonify, render_template, session
import os
from functions.ml_api_utils import chunk_text_by_tokens, query, translate_with_API, extract_text_from_pdf

app = Flask(__name__)

# Just for testing purposes in development
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
    (As the GoogleTranslate Api doesn't seem to have any limits it's used by default)
    :return: translated_data
    """
    pdf_file = request.files['file']
    target_lang = request.form['target_lang']
    session['target_lang'] = target_lang

    # Calling the extract_text_from_pdf function, translate_with_API function and returning the translated_data
    text = extract_text_from_pdf(pdf_file)

    _, translated_data = translate_with_API(text, target_lang, translator="Google")
    print(translated_data)

    return jsonify(translated_data)



@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Summarize the translated text using the Hugging Face Inference API
    :return: return jsonify({'summary': final_combined_summary})
    """
    translated_text = request.form['translated_text']
    target_lang = session.get('target_lang')
    # As the HF Model only supports English, we need to translate the text back to English (a more efficient solution can be implemented)
    text_back_to_english, _ = translate_with_API(translated_text, "EN", translator="Google")

    print("-------------------------- CHUNKING TEXT BY TOKENS -------------------------------")

    chunks = list(
        chunk_text_by_tokens(text_back_to_english, max_tokens=900))  # Adjust max_tokens if necessary

    print("-------------------------- STARTING SUMMARIZATION WITH HF INFERENCE API -------------------------------")
    summaries = []

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        payload = {"inputs": chunk,
                   "parameters": {
                       "truncation": True,
                       "max_length": 1024  # Adjust based on the model's limit
                   }}
        summary = query(payload)
        summaries.append(summary)

    combined_summary = " ".join(
        item["summary_text"] for summary in summaries for item in summary
        if "summary_text" in item
    )

    print("-------------------------- SUMMARIZATION SUCCESSFUL -------------------------------")
    print("-------------------------- TEST IS HERE -------------------------------")

    print(f"Summaries List: {summaries}")



    # Translate the final summary back to the target language
    final_combined_summary, x = translate_with_API(combined_summary, target_lang, translator="Google")
    print("-------------------------- 2nd TEST IS HERE -------------------------------")

    print(f"Final Summary: {final_combined_summary}")
    return jsonify({'summary': final_combined_summary})


if __name__ == '__main__':
    app.run(port=5000, debug=False)
