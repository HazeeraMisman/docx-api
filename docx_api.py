# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from docx import Document
import base64
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "API is running!"

@app.route('/extract-text', methods=['POST'])
def extract_text():
    try:
        data = request.get_json()
        base64_docx = data.get("base64Docx")

        if not base64_docx:
            return jsonify({"error": "No file content provided"}), 400

        docx_bytes = base64.b64decode(base64_docx)
        file_stream = io.BytesIO(docx_bytes)
        doc = Document(file_stream)

        text = "\n".join([para.text for para in doc.paragraphs])
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
