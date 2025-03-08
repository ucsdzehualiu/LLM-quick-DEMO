import gradio as gr
import ollama


def generate_response_stream(message, chat_history):
    """
    使用 Ollama 模型生成流式响应。

    参数:
        message (str): 用户当前输入的消息。
        chat_history (list): 历史聊天记录，每项为 (用户消息, 助手回复) 的元组。

    生成:
        str: 流式更新的助手回复。
    """
    # 将聊天历史转换为 Ollama 所需格式
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
            "temperature": 0.6,
            "max_tokens": 30000
        }
    )

    # 流式处理响应并逐步返回内容
    assistant_response = ""
    for chunk in response:
        content = chunk['message']['content']
        assistant_response += content
        yield assistant_response


# 定义 Gradio 聊天界面
chat_interface = gr.ChatInterface(
    fn=generate_response_stream,
    title="Chatbot DEMO",
    description="CHAT BOT",
    examples=["你好，介绍一下你自己。", "Python 是什么？"],
)


if __name__ == "__main__":
    # 检查模型是否存在，否则下载
    try:
        ollama.show('qwq')
    except ollama.ResponseError:
        print("正在下载模型...")
        ollama.pull('qwq')

    # 启动 Gradio 应用
    chat_interface.launch(server_name="0.0.0.0", server_port=7861)
