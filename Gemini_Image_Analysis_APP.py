import gradio as gr
import google.generativeai as genai
import textwrap
import PIL.Image


genai.configure(api_key="Gemini_API_Key") # API Key
model = genai.GenerativeModel('models/gemini-1.5-flash')

def format_text(text):
    text = text.replace('•', '  ')
    return textwrap.indent(text, '> ', predicate=lambda _: True)



def initialize_chat_history():
    return []

def add_message_to_history(history, role, message):
    history.append({"role": role, "parts": [message]})
    return history

def generate_response(image, prompt, chat_history):
    try:

        if not chat_history:
            chat_history = initialize_chat_history()
        
        chat_history = add_message_to_history(chat_history, "user", prompt)
        
 
        if image:
            response = model.generate_content([prompt, image], stream=True)
        else:
            response = model.generate_content(prompt, stream=True)
        
        response.resolve()
        
        chat_history = add_message_to_history(chat_history, "model", response.text)
        
        formatted_response = format_text(response.text)
        
        return formatted_response, chat_history
    
    except Exception as e:
        return f"An error occurred: {str(e)}", chat_history

def clear_chat():
    return [], None




with gr.Blocks() as interface:
    chat_history_state = gr.State([])
    

    gr.Markdown("# AI Math ChatBot: Conversational Mathematical Assistant")
    gr.Markdown("Upload an image of ingredients and chat about recipe ideas!")
    
    with gr.Row():
        with gr.Column():

            image_input = gr.Image(type="pil", label="Upload an Image of Math Problem or Question")
            prompt_input = gr.Textbox(label="Enter your Prompt", placeholder="Ask about any Math Problem.")
            

            with gr.Row():
                submit_btn = gr.Button("Generate Response")
                clear_btn = gr.Button("Clear Chat")
        
        with gr.Column():
            output = gr.Markdown(label="Response")
            
            chat_history_display = gr.Markdown(label="Chat History")
    
    submit_btn.click(
        fn=generate_response, 
        inputs=[image_input, prompt_input, chat_history_state],
        outputs=[output, chat_history_state]
    )
    

    clear_btn.click(
        fn=clear_chat,
        outputs=[chat_history_display, image_input]
    )


interface.launch(share=True)