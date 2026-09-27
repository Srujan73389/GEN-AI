import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

app = Flask(__name__)
app.json.ensure_ascii = False
app.config["UPLOAD_FOLDER"] = "static"


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        language = request.form["language"]
        file = request.files["file"]

        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)

            audio_file = open(file_path, "rb")

            transcript = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file
            )

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": f"You will be provided with a sentence in English, and your task is to translate it into {language}"
                    },
                    {
                        "role": "user",
                        "content": transcript.text
                    }
                ],
                temperature=0,
                max_tokens=256
            )
            return jsonify(response.choices[0].message.content)


            
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)