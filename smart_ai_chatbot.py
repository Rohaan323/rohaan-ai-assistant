import gradio as gr
from groq import Groq

# ✅ Groq Llama 3 setup
client = Groq(api_key="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")

# ✅ Memory & logic
memory = {}
MAX_HISTORY = 5

def save_memory(mem):
    pass

# ✅ Main AI logic
def chat_with_ai(message, chat_history):
    try:
        msg_lower = message.lower()

        if "my name is" in msg_lower:
            name = msg_lower.split("my name is")[-1].strip(" :.")
            memory["name"] = name
            save_memory(memory)
            reply = f"Nice to meet you, {name}!"
            return chat_history + [[message, reply]]

        if "what is my name" in msg_lower:
            name = memory.get("name", "not saved yet")
            reply = f"Your name is {name}."
            return chat_history + [[message, reply]]

        if any(phrase in msg_lower for phrase in [
            "who made you", "who is your creator", "who built you",
            "who developed you", "who programmed you", "who designed you", "who coded you"
        ]):
            reply = "I was made by Rohaan Zohaib, my creator."
            return chat_history + [[message, reply]]

        if any(phrase in msg_lower for phrase in [
            "who are you",
            "who r u",
            "what are you",
            "tell me about yourself",
            "describe yourself",
            "what do you do",
            "what is your purpose",
            "what's your job",
            "what do you exist for",
            "why do you exist"
        ]):
            reply = "I am Rohaan's AI Assistant — always ready to help you anytime, day or night!"
            return chat_history + [[message, reply]]

        if "what is your name" in msg_lower:
            reply = "My name is Rohaan's AI Assistant."
            return chat_history + [[message, reply]]

        messages = []
        for user, bot in chat_history[-MAX_HISTORY:] if chat_history else []:
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": bot})
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )

        reply = response.choices[0].message.content
        return chat_history + [[message, reply]]

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        return chat_history + [[message, error_msg]]

# ✅ Black gaming theme with custom CSS
custom_css = """
body { background-color: #000000; color: #00FFEF; }
.gradio-container { background-color: #000000; }
h1, p { color: #00FFEF; }
button { background-color: #111111; color: #00FFEF; border: 1px solid #00FFEF; }
input { background-color: #111111; color: #00FFEF; }
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown(
        """
        <div style='text-align:center;'>
        <h1>🎮 Rohaan's AI Assistant 🤖</h1>
        <p>Type your message — your cyber assistant is ready!</p>
        </div>
        """
    )

    chatbot = gr.Chatbot(label="💬 Rohaan's AI Assistant", height=500)
    msg = gr.Textbox(label="🎮 Type your message...", placeholder="Ready to chat? Type here...")
    clear = gr.Button("🗑️ Clear Chat")

    def respond(message, history):
        return chat_with_ai(message, history)

    msg.submit(respond, [msg, chatbot], chatbot)
    clear.click(lambda: None, None, chatbot)

    gr.Markdown(
        "<hr><p style='text-align:center;'>🔥 Made by Rohaan Zohaib — Rohaan's AI Assistant Black Edition 🔥</p>"
    )

# ✅ Best practice for deployment
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8080)
