from module.web_handler import Website
from dotenv import load_dotenv
import google.generativeai as genai
import os
import gradio as gr
import re

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY', 'your_key_if_not_using_env'))
generation_config = {"temperature" : 0.9, "top_p" : 1, "top_k" : 1}
model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)

system_prompt = "You are an assistant that analyzes the contents of a website \
    and provides a short summary, ignoring text that might be navigation related. \
"


def user_prompt_for(website):
    user_prompt = website.text
    user_prompt += f"You are looking at a website titled {website.title}"
    user_prompt += "The contents of this website is as follows; \
        please provide a short summary of this website in markdown.\
        If it includes news or annoucements, then summerize these too \n\n"
    return user_prompt

def is_url(string):
    url_pattern = re.compile(
        r'^(https?://)?'                     
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'     
        r'(/[\w-]*)*'                         
        r'(\?.*)?'                            
        r'(#.*)?$'                          
    )
    return bool(url_pattern.match(string))

def summarize(text, history):
    if ( is_url(text) == False):
        return "URL only"
    website = Website(text)
    full_prompt = f"System: {system_prompt} User: {user_prompt_for(website)}"
    response = model.generate_content(full_prompt)
    return response.text

demo = gr.ChatInterface(
    fn=summarize,  # The function to summarize the website content
    title="Web Summarizer",  # Title of the interface
    description="Summarize the contents of a website",  # Description of the interface
    theme="soft",  # The theme of the interface
)




demo.launch()