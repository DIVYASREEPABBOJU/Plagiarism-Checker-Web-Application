from flask import Flask, request, jsonify
from flask_cors import CORS
import textdistance
import docx

app = Flask(__name__)
CORS(app)

# Function to read uploaded files
def read_file(file):
    if file.filename.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return ""

@app.route('/check', methods=['POST'])
def check_plagiarism():
    try:
        text1, text2 = "", ""

        # If both files uploaded
        if 'file1' in request.files and 'file2' in request.files:
            text1 = read_file(request.files['file1'])
            text2 = read_file(request.files['file2'])
        else:
            # If pasted text
            text1 = request.form.get('text1', '')
            text2 = request.form.get('text2', '')

        if not text1.strip() or not text2.strip():
            return jsonify({"error": "Both inputs are required"}), 400

        similarity = textdistance.cosine.normalized_similarity(text1, text2)
        percent = round(similarity * 100, 2)

        return jsonify({
            "similarity": f"{percent}%",
            "message": "Comparison successful"
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Plagiarism Checker Backend Active"})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)


