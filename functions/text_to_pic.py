import openai as client
import json
import logging

with open('api_key.txt', 'r') as file:
    client.api_key = file.readline().strip()

def text_to_pic(text):
    response = client.chat.completions.create(
                    model='gpt-4o-mini',
                    messages=[{"role": "system", "content": f"[Summarize below text under 10 words.] \n {text}"}],
                    temperature=0.3)

    PROMPT = f"[MAKE IT TO REALISTIC PHOTO WITH LEAST FEATURES. IT SHOULD BE SUITABLE FOR THE NEWS]{response.choices[0].message.content}"

    response = client.images.generate(
      model="dall-e-3",
      prompt = PROMPT,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    return response.data[0].url