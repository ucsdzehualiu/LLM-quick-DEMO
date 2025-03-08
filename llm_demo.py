import gradio as gr
import ollama

# 定义流式生成函数
def generate_response_stream(message, chat_history):
    # 将聊天历史转换为 Ollama 需要的格式
    messages = []
    for user_msg, assistant_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": message})

    # 创建流式生成请求
    response = ollama.chat(
        model='qwq',  # Ollama 模型名称
        messages=messages,
        stream=True,
        options={
            "temperature": 0.7,
            "max_tokens": 30000
        }
    )

    # 流式处理响应
    assistant_response = ""
    for chunk in response:
        content = chunk['message']['content']
        assistant_response += content
        yield assistant_response

# 创建 Gradio ChatInterface
chat_interface = gr.ChatInterface(
    fn=generate_response_stream,
    title="Qwen Chatbot with Streaming (Ollama)",
    description="A chatbot using Qwen model via Ollama with streaming generation.",
    examples=["你好，介绍一下你自己。", "Python 是什么？"],
)

# 启动应用前确保模型已存在
try:
    ollama.show('qwq')
except ollama.ResponseError:
    print("正在下载模型...")
    ollama.pull('qwq')

# 启动 Gradio 应用
chat_interface.launch(server_name="0.0.0.0", server_port=7861)