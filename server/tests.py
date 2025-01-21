from ollama import chat
from ollama import Client

client = Client(
  host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)


stream = client.chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'Identify the poker cards. Print only the result, nothing more!',
        'images': ['image3.jpg']
    }],
    stream=True,
)




for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)
