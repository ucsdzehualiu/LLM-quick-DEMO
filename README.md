# LLM_DEMO
 A chatbot demo powered by Ollama with streaming capabilities. The current model is `qwq`.
# Ollama-Based Chatbot DEMO
## 中文说明：
这是一个基于 Gradio 和 Ollama 的聊天机器人示例。通过 Ollama 模型（如 `qwq`）提供流式响应，支持与用户进行自然对话。

## 功能特点
- **流式生成**：逐字返回模型的回复内容，提升交互体验。
- **历史记录保留**：自动处理并存储聊天上下文，确保对话连贯性。
- **自定义配置**：可通过参数调整温度值（temperature）、最大输出长度（max_tokens）等。

## 安装要求
```bash
pip install gradio ollama
```
## 运行步骤
确保已安装并运行 Ollama 服务。
执行以下命令启动应用：
```
python app.py
```
访问 http://localhost:7861 使用聊天界面。
注意事项
若首次使用模型 qwq，系统会自动下载（可能需要较长时间）。
可通过修改代码中的 model='qwq' 更换其他 Ollama 支持的模型。
流式响应速度取决于网络和模型复杂度，请保持稳定连接。
### English Description:
This is a chatbot demo powered by Gradio and Ollama. It leverages the Ollama model (e.g., qwq) to generate streaming responses for natural conversations.

Features
Streaming Response: Gradually outputs the model's reply for smooth interaction.
Chat History Management: Automatically retains context for coherent dialogues.
Customizable Parameters: Adjust temperature, max tokens, and other settings via code parameters.
Requirements

pip install gradio ollama
Usage Steps
Ensure Ollama service is installed and running.
Run the application:


python app.py
3. Access the chat interface at http://localhost:7861.

Notes
The model qwq will be automatically downloaded if not found (may take time).
Replace model='qwq' in code to use other Ollama models.
Streaming performance depends on network and model complexity. Stable connectivity is recommended.


