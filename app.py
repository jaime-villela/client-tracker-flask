import openai
import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  #  Replace with your OpenAI API key

def analyze_sentiment(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or another suitable engine
            prompt=f"Analyze  the sentiment of the following text: '{text}'.  Return only 'positive',  'negative', or 'neutral'.",
            max_tokens=10,  # Limit response length 
            n=1,
            stop=None,
            temperature=0.5,  # Adjust for creativity vs.  accuracy
        )
        sentiment = response.choices[0].text.strip().lower()
        return sentiment
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return None

@app.route('/')
def index():
    text = "The service is bad"  # Replace with  actual client conversation
    sentiment = analyze_sentiment(text)

    if sentiment is None:
        emoji = "❓"  # Unknown status
    elif sentiment == "positive":
        emoji = "😊"  # Positive sentiment
    elif sentiment == "negative":
        emoji = "😞"  # Negative sentiment
    else:
        emoji = "😐"  # Neutral sentiment
    
    return render_template('index.html', emoji=emoji)

if __name__ == '__main__':
    app.run(debug=True)
