import gradio as gr
import requests
import json
import time

#nohup vllm serve Qwen/QwQ-32B --max_model_len 35000 --gpu_memory_utilization 0.95 >1.txt &
def format_chat_history(chat_history):
    """将Gradio聊天历史转换为Qwen专用格式"""
    formatted = ""
    for user_msg, assistant_msg in chat_history:
        formatted += f"<|im_start|>user\n{user_msg}<|im_end|>\n"
        formatted += f"<|im_start|>assistant\n{assistant_msg}<|im_end|>\n"
    return formatted


def stream_vllm_generate(prompt, temperature=0.7):
    """流式生成核心函数"""
    url = "http://localhost:8000/v1/completions"
    headers = {'Content-Type': 'application/json'}

    payload = {
        'model': "Qwen/QwQ-32B",
        'prompt': prompt,
        'max_tokens': 30000,
        'temperature': temperature,
        'stream': True,
        'stop': ['<|im_end|>'],
        'echo': False
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)

    if response.status_code != 200:
        raise Exception(f'请求失败: {response.text}')

    for chunk in response.iter_lines(decode_unicode=True):
        if chunk:
            if chunk.startswith('data: '):
                chunk = chunk[6:]

            if chunk.strip() == '[DONE]':
                break

            try:
                data = json.loads(chunk)
                if 'choices' in data:
                    yield data['choices'][0].get('text', '')
                    # 提前终止检查
                    if data['choices'][0].get('finish_reason') == 'stop':
                        break
            except json.JSONDecodeError:
                continue


def generate_response_stream(message, chat_history):
    """适配Gradio的流式生成函数"""
    # 构建符合Qwen格式的prompt
    base_prompt = format_chat_history(chat_history)
    current_prompt = base_prompt + f"<|im_start|>user\n{message}<|im_end|>\n<|im_start|>assistant\n"

    # 流式生成
    assistant_response = ""
    for delta in stream_vllm_generate(current_prompt, temperature=0.6):
        assistant_response += delta
        yield assistant_response


# 创建Gradio界面
chat_interface = gr.ChatInterface(
    fn=generate_response_stream,
    title="Qwen Chatbot (vLLM)",
    description="基于Qwen-32B模型的聊天演示",
    examples=["解释量子计算", "用Python写快速排序"],
    css=".gradio-container {background: #f9f9f9}"
)

if __name__ == "__main__":
    # 配置服务器参数
    server_config = {
        "server_name": "0.0.0.0",
        "server_port": 7861,
        "share": False
    }

    # 启动应用
    print("启动聊天服务器...")
    chat_interface.launch(**server_config)