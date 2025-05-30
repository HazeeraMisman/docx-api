# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from docx import Document
import base64
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def extract_text_get():
    file_base64 = request.args.get('file_base64')
    print("Header received:", "Yes" if file_base64 else "No")

    # Health check endpoint
    if not file_base64:
        return "API is running!"

    try:
        docx_bytes = base64.b64decode(file_base64)
        file_stream = io.BytesIO(docx_bytes)
        doc = Document(file_stream)

        text = "\n".join([para.text for para in doc.paragraphs])
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
