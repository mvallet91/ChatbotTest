from keys import api_keys
import openai
import gradio as gr

openai.api_key = api_keys.keys['openai']

message_history = [
    {"role": "system", "content": 
     """
     You are an educational AI Assistant for higher education. 
     You help students solve a complex problem using analytics and python.
     Do not provide them the full answer to their questions, but guide them and point them in the right direction. 
     Ask for clarifying questions when necessary and try to be concise with your responses.
     """
     },
]


def predict(input):
    global message_history
    message_history.append({"role": "user", "content": input})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613", 
        messages=message_history
    )
    reply = chat.choices[0].message.content
    message_history.append({"role": "assistant", "content": reply})
    response = [(message_history[i]["content"], message_history[i+1]["content"]) 
                for i in range(1, len(message_history)-1, 2)]
    return response
    
    
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Chat with AI").style(container=False)
        txt.submit(predict, txt, chatbot)
        txt.submit(None, None, txt, _js="() => {''}")


demo.launch()

# inputs = gr.inputs.Textbox(lines=7, label="Chat with AI")
# outputs = gr.outputs.Textbox(label="Reply")

# gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs, title="AI Chatbot",
#              description="Ask anything you want",
#              theme="compact").launch(share=True)

# print(inputs, outputs)



# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     chatbot()

