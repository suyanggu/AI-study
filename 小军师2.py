import openai
import docx
import configparser


# 从ini文件中读取api_key
openai.api_key = "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"

doc = docx.Document("/Users/long/Desktop/小军师-效能测试数据.docx")
text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

# Function to send a message to the OpenAI chatbot model and return its response
# 发送消息给OpenAI的聊天机器人模型，并返回它的回复
def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    # 使用OpenAI的ChatCompletion API来获取聊天机器人的回复
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        # 这个模型是网页版OpenAI chatbot的模型
        # The conversation history up to this point, as a list of dictionaries
        # 将目前为止的对话历史记录，作为字典的列表
        messages=message_log,
        # The maximum number of tokens (words or subwords) in the generated response
        # 最大的生成回复的token数 最大4095（单词或子单词）
        max_tokens=500,
        # The stopping sequence for the generated response, if any (not used here)
        # 停止生成回复的序列，如果有的话（这里没有使用）
        stop=None,
        # The "creativity" of the generated response (higher temperature = more creative)
        # 生成回复的“创造性”（参数越高，创造性越强）
        temperature=0.9,
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    # 从聊天机器人的回复中，找到第一个有文本的回复（有些回复可能没有文本）
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    # 如果没有找到有文本的回复，返回第一个回复的内容（可能为空）
    return response.choices[0].message.content


# Main function that runs the chatbot
def main():
    # Initialize the conversation history with a message from the chatbot
    # 用聊天机器人的消息来初始化对话历史记录
    message_log = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    # Set a flag to keep track of whether this is the first request in the conversation
    # 设置一个标志来跟踪这是否是对话中的第一个请求
    first_request = True

    # Start a loop that runs until the user types "quit"
    # 开始一个循环，直到用户输入“quit”为止
    while True:
        if first_request:
            # If this is the first request, get the user's input and add it to the conversation history
            # 如果这是第一个请求，获取用户的输入，并将其添加到对话历史记录中
            prompt = f"请结合下面的文本内容，根据你自己的经验知识，总结文本内容表现出的管理现状情况，并给出初步的管理建议。（管理现状和初步建议要换行区分，分别表达；管理现状和初步建议中用序号分开进行要点表达，但要点要尽量抽象概括，不要只是复述数据）不要再把数据复述一遍，直接给出概括性的结论。\
    文本内容是：{text}\""
            message_log.append({"role": "user", "content": prompt})

            # Add a message from the chatbot to the conversation history
            # 添加来自聊天机器人的消息到对话历史记录中
            message_log.append(
                {"role": "assistant", "content": "You are a helpful assistant."})

            # Send the conversation history to the chatbot and get its response
            # 发送对话历史记录给聊天机器人，并获取它的回复
            response = send_message(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            # 添加聊天机器人的回复到对话历史记录中，并将其打印到控制台
            message_log.append({"role": "assistant", "content": response})
            print(f"AI assistant: {response}")

            # Set the flag to False so that this branch is not executed again
            # 设置标志为False，以便不再执行此分支
            first_request = False
        else:
            # If this is not the first request, get the user's input and add it to the conversation history
            # 如果这不是第一个请求，获取用户的输入，并将其添加到对话历史记录中
            user_input = input("You: ")

            # If the user types "quit", end the loop and print a goodbye message
            # 如果用户输入“quit”，结束循环并打印再见消息
            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            message_log.append({"role": "user", "content": user_input})

            # Send the conversation history to the chatbot and get its response
            # 发送对话历史记录给聊天机器人，并获取它的回复
            response = send_message(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            # 添加聊天机器人的回复到对话历史记录中，并将其打印到控制台
            message_log.append({"role": "assistant", "content": response})
            print(f"AI assistant: {response}")


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()


