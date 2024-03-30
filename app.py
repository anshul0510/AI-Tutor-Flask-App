from flask import Flask, request, jsonify
import openai
from googleapiclient.discovery import build
from PIL import Image
import pytesseract

app = Flask(__name__)

openai.api_key = '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'

youtube_api_key = 'AIzaSyDM5CqqIs7NMaZ8aPfVnFVo0sBUXnDo100'

youtube = build('youtube', 'v3', developerKey=youtube_api_key)

conversation_memory = {}

@app.route('/')
def hello_world():
    return 'Hello, World! This is AI Tutor.'

@app.route('/asks', methods=['POST'])
def ask_Video_question():
    if request.method == 'POST':
        data = request.get_json()
        question = data.get('question')
        image_path = data.get('image')  
        user_id = data.get('user_id')  
        try:
            
            conversation = conversation_memory.get(user_id, [])

            conversation.append({"role": "user", "content": question})
            conversation_memory[user_id] = conversation

            if image_path:
                image_text = process_image_query(image_path)
                conversation.append({"role": "user", "content": image_text})
                conversation_memory[user_id] = conversation

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    *conversation  
                ]
            )
            answer = response.choices[0].message['content']

            print("Generated answer:", answer)

            search_response = youtube.search().list(
                q=question,
                part='snippet',
                maxResults=5  
            ).execute()

            video_links = []
            for item in search_response['items']:
                if item['id']['kind'] == 'youtube#video':
                    video_id = item['id']['videoId']
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    video_links.append(video_url)

            return jsonify({'answer': answer, 'video_links': video_links})
        except Exception as e:
            print("Error:", e)
            return jsonify({'error': str(e)})

def process_image_query(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, request, jsonify
# import openai
# from googleapiclient.discovery import build

# # Set up Flask app
# app = Flask(__name__)

# # Set up OpenAI API key
# api_key = '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'

# # Set up YouTube API key
# youtube_api_key = 'AIzaSyDM5CqqIs7NMaZ8aPfVnFVo0sBUXnDo100'

# # Create YouTube API client
# youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# @app.route('/')
# def hello_world():
#     return 'Hello, World! This is AI Tutor.'

# @app.route('/asks', methods=['POST'])
# def ask_Video_question():
#     if request.method == 'POST':
#         data = request.get_json()
#         question = data.get('question')
#         try:
#             # Call OpenAI GPT-3.5 model to generate response
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": question}
#                 ]
#             )
#             answer = response.choices[0].message['content']

#             # Search for relevant YouTube videos
#             search_response = youtube.search().list(
#                 q=question,
#                 part='snippet',
#                 maxResults=5  # Number of videos to retrieve
#             ).execute()

#             # Extract video links from search results
#             video_links = []
#             for item in search_response['items']:
#                 if item['id']['kind'] == 'youtube#video':
#                     video_id = item['id']['videoId']
#                     video_url = f'https://www.youtube.com/watch?v={video_id}'
#                     video_links.append(video_url)

#             return jsonify({'answer': answer, 'video_links': video_links})
#         except Exception as e:
#             return jsonify({'error': str(e)})

# @app.route('/ask', methods=['POST'])
# def ask_question():
#     if request.method == 'POST':
#         data = request.get_json()
#         question = data.get('question')
#         try:
#             # Call OpenAI GPT model to generate response
#             openai.api_key = api_key
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": question}
#                 ]
#             )
#             answer = response.choices[0].message['content']
#             return jsonify({'answer': answer})
#         except Exception as e:
#             return jsonify({'error': str(e)})


# if __name__ == '__main__':
#     app.run(debug=True)
