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
    app.run(debug=True)


# push to GitHub
# Run 'git init' in the terminal to initialize a Git repository.
