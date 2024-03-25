import whisper
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper
import os
from dotenv import load_dotenv
# 從https://platform.openai.com/ 獲取
os.environ["OPENAI_API_KEY"] = "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"

# 從https://nla.zapier.com/docs/authentication/ & https://actions.zapier.com/credentials/ 登入後獲取：
os.environ["ZAPIER_NLA_API_KEY"] = "sk-ak-f0sQolIk14LUBqFaOmNqKJpXXb"


def email_summary(file):


    # 大型語言模型
    llm = OpenAI(temperature=0)

    # 初始化zapier
    zapier = ZapierNLAWrapper()
    toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)

    # 這裡使用的代理是"zero-shot-react-description"代理。
    # Zero-shot意味著代理僅基於當前操作功能——它沒有記憶。
    # 它使用ReAct框架決定基於工具的描述使用哪個工具。
    agent = initialize_agent(toolkit.get_tools(), llm, agent="zero-shot-react-description", verbose=True)


    # 指定模型，在這裡是BASE
    model = whisper.load_model("base")

   

    # 轉錄音頻文件
    result = model.transcribe(file)
    print(result["text"])

    # 使用zapier發送電子郵件
    agent.run("Send an Email to kilong31442@gmail.com via gmail summarizing the following text provided below : "+result["text"])
