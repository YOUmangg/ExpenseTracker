from groq import Groq
import os
import random
import datetime

os.environ["GROQ_API_KEY"] = "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"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def send_query_date_extract(role="user", content = f'{datetime.datetime.now()}'):
    ans = client.chat.completions.create(
        messages=[
            {
                "role": role,
                "content": f"Fetch me the date in the following format : %Y-%m-%d %H:%M:%S from this {content}. Just return the date, no characters before or after.",
            }
        ],
        model="llama3-8b-8192",
    )
    return str(ans.choices[0].message.content)

#.choices[0].message.content

def tell_class(content, classes, role="user"):
    ans = client.chat.completions.create(
        messages=[
            {
                "role": role,
                "content": f'Just tell me to which of the following classes, the {content} belongs to: {classes}. If you find "Auto", it comes under "Travel". You can also suggest just the name of a new class, in case you find it appropriate. Just tell me the name of the class it belongs to, no characters before or after.',
            }
        ],
        model="llama-3.2-90b-vision-preview",
    )
    return ans.choices[0].message.content