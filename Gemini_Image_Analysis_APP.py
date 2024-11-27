import gradio as gr
import google.generativeai as genai
import textwrap

genai.configure(api_key="Google_api_key")

model = genai.GenerativeModel('models/gemini-1.5-flash')

def format_text(text):
    text = text.replace('•', '  ')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def analyze_image(image):
    response = model.generate_content(["""Analyze the image and write in text about image.""", image], stream=True)
    response.resolve()
    return format_text(response.text)

interface = gr.Interface(
    fn=analyze_image,
    inputs=gr.Image(type="pil"),
    outputs=gr.Markdown(),  
    title="IngrediChef",
    description="Upload an Image of ingredients"
)

interface.launch("share=True")