import docx
import openai

# 设置 OpenAI API 密钥
openai.api_key = "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"

# 读取 Word 文档内容
doc = docx.Document("/Users/long/Desktop/小军师-效能测试数据.docx")
text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

# print(text)

def get_completion(prompt, model="gpt-3.5-turbo"):
    '''
    prompt: 对应的提示
    model: 调用的模型，默认为 gpt-3.5-turbo(ChatGPT)，有内测资格的用户可以选择 gpt-4
    '''
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0, 
        frequency_penalty=0,
        presence_penalty=0,# 模型输出的温度系数，控制输出的随机程度
    )
    # 调用 OpenAI 的 Completion 接口
    return response.choices[0].message["content"]

# 设置默认问题
default_prompt = f"请结合下面的文本内容，根据你自己的经验知识，总结文本内容表现出的管理现状情况，并给出初步的管理建议。（管理现状和初步建议要换行区分，分别表达；管理现状和初步建议中用序号分开进行要点表达，但要点要尽量抽象概括，不要只是复述数据）不要再把数据复述一遍，直接给出概括性的结论。\
    文本内容是：{text}\
    """

# 首次运行程序时使用默认问题
prompt = default_prompt
response = get_completion(prompt)
report = f"一、根据目前提供的指标对现状进行分析，给出初步建议：\n   {response}\n\n二、行业经验表明，"

# 打印分析结果
print(report)

while True:
    # 提示输入问题
    question = input("请输入你的问题：")
    
    # 如果是默认问题，则使用默认 prompt 值
    if question == default_prompt:
        prompt = default_prompt
    else:
        # 否则使用另外一个 prompt 值
        prompt = f"\n问题是：{question}\n"
    
    # 调用接口获取回答
    response = get_completion(prompt)
    
    # 打印回答
    print(response)
