import gradio as gr
import os
import time
import google.generativeai as genai

google_key = os.os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=google_key)

class Conversation:
    def __init__(self, prompt, num_of_round):
        self.prompt = prompt
        self.num_of_round = num_of_round
        self.messages = ""
        self.messages += self.prompt
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat()
        self.chat.send_message(self.messages)

    def ask(self, question):
        try:
            self.messages = question
            response = self.chat.send_message(self.messages)
        except Exception as e:
            print(e)
            return e

        message = response.text
        #self.messages.append(response.text)

        return message

prompt ="""
**我的角色是“无尽人生，你的江南”超级游戏的主理人，主要任务是：为玩家提供个性化剧本生成，并指引玩家按照剧本完成任务和挑战。

**需要记住的是：我为玩家生成的任何剧本的故事背景，都必须只能是在江南环太湖地区，具体交互的场景限定在平江路、西山岛、拙政园、山塘街、虎丘范围之内。
"""

conv = Conversation(prompt, 10)

def answer(question, history=[]):
    history.append(question)
    response = conv.ask(question)
    history.append(response)
    responses = [(u,b) for u,b in zip(history[::2], history[1::2])]
    return responses, history

with gr.Blocks(css="#chatbot{height:300px} .overflow-y-auto{height:500px}") as demo:
    chatbot = gr.Chatbot(elem_id="chatbot")
    state = gr.State([])

    # with gr.Row():
    #     txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    txt = gr.Textbox()
    txt.submit(answer, [txt, state], [chatbot, state])

demo.launch()