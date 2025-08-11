from flask import Flask, request, render_template
import os

from FaqGenerator_v2 import AssignmentFAQGenerator  
# from linkedin_matching import LinkedInMatcher  # example for the other tool

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        input_text = request.form.get("input_text")
        if input_text:
            # Run FAQ Generator
            faq_generator = AssignmentFAQGenerator()
            faq_generator.process_document(input_text)  # if file path, adjust for uploads
            result = "\n".join([f"Q: {p['question']}\nA: {p['answer']}" for p in faq_generator.faq_pairs])
    return render_template("index.html", result=result)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


