import os
import google.generativeai as genai

genai.configure(api_key ='AIzaSyBfzHhBvP6ZLmSIiW8Gb91uuLEJF2RfKpo')
model = genai.GenerativeModel('gemini-pro')

# response = model.generate_content("List 5 planets each with an interesting fact")
# print(response.text)


chat = model.start_chat()
config = {
    "max_output_tokens": 2048,
    "temperature": 0.9,
    "top_p": 1
}
response = chat.send_message('hello, tell me a story about India')
print(response.candidates[0].content.parts[0].text)


