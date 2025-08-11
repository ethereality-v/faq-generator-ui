from flask import Flask, request, render_template, redirect, url_for, flash
import os
import tempfile
from FaqGenerator_v2 import AssignmentFAQGenerator

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")  # for flash messages

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        # 1) Handle textarea input
        input_text = request.form.get("input_text", "").strip()

        # 2) Handle file upload (optional)
        uploaded = request.files.get("file")
        temp_path = None
        try:
            if uploaded and uploaded.filename:
                # Save to a temp file
                suffix = os.path.splitext(uploaded.filename)[1].lower()
                fd, temp_path = tempfile.mkstemp(suffix=suffix)
                os.close(fd)
                uploaded.save(temp_path)
                # use the file path as input
                to_process = temp_path
            else:
                to_process = input_text

            if not to_process:
                flash("Please paste text or upload a file.", "warning")
                return render_template("index.html", result=result)

            faq_generator = AssignmentFAQGenerator()
            success = faq_generator.process_document(to_process)
            if not success:
                flash("Failed to process document. Check file or text.", "error")
                return render_template("index.html", result=result)

            result = "\n\n".join([f"Q: {p['question']}\nA: {p['answer']}" for p in faq_generator.faq_pairs])
        finally:
            # cleanup temp file if created
            if temp_path and os.path.exists(temp_path):
                try: os.remove(temp_path)
                except Exception: pass

    return render_template("index.html", result=result)
