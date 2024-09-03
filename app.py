from flask import Flask, render_template, request
import google.generativeai as genai
import requests
import base64
import time
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash') 

# WordPress details
wordpress_api_endpoint = "https://nustudy.com/wp-json/wp/v2/posts" 
wordpress_username = os.getenv('WORDPRESS_USERNAME')
wordpress_password = os.getenv('WORDPRESS_PASSWORD')

def generate_content(prompt):
    # Generate text using the Gemini model
    response = model.generate_content(prompt) 

    # Check for response text and handle potential empty responses
    if response.text:
        return response.text
    else:
        # Handle potential content filtering gracefully
        return "কন্টেন্ট তৈরি করতে সমস্যা হয়েছে। অনুগ্রহ করে প্রম্পটটি পর্যালোচনা করুন অথবা সম্ভাব্য নিরাপত্তা উদ্বেগগুলি পরীক্ষা করুন।"

def post_to_wordpress(content, title):
    # Basic Authentication for WordPress
    credentials = f"{wordpress_username}:{wordpress_password}"
    token = base64.b64encode(credentials.encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json'
    }

    # Data to be sent in the POST request
    data = {
        'title': title,
        'content': content,
        'status': 'draft'  # You can change this to 'publish' if you want to publish directly
    }

    response = requests.post(wordpress_api_endpoint, headers=headers, json=data)

    if response.status_code == 201:  # 201 Created indicates a successful post
        print("Post created successfully!")
        return response.json()['link']  # Return the link to the newly created post
    elif response.status_code == 429:  # Handle 429 Too Many Requests error
        retry_after = int(response.headers.get('Retry-After', 5)) 
        print(f"Rate limited, retrying after {retry_after} seconds...")
        time.sleep(retry_after)
        return post_to_wordpress(content, title) 
    else:
        print(f"Error creating post: {response.status_code} - {response.text}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']

    # Input validation: check if the prompt is empty or contains only whitespace
    if not prompt or prompt.isspace():
        return "Please enter a valid prompt before generating content."

    enhanced_prompt = f"""
    {prompt} : write a details blog post.
    """
    generated_content = generate_content(enhanced_prompt)

    # Use the prompt as the title for the WordPress post
    post_url = post_to_wordpress(generated_content, prompt) 
    if post_url:
        return f"Content generated and posted to WordPress! <a href='{post_url}' target='_blank'>View Post</a>"
    else:
        return "Error posting to WordPress. Please check your credentials and try again."

if __name__ == '__main__':
    app.run(debug=True)