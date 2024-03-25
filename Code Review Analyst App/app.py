#下面的導入已被Langchain在其改進策略中最近提到的導入所替代 :)
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

from langchain.schema import HumanMessage, SystemMessage
from io import StringIO
import streamlit as st
from dotenv import load_dotenv
import time
import base64


#這個函數通常在Python中被用來從.env檔案加載環境變量到應用的環境中。
load_dotenv()

st.title("來對你的Python代碼進行代碼審查吧")
st.header("請在這裡上傳你的.py檔案:")


# 使用Streamlit將文本內容作為檔案下載的函數
def text_downloader(raw_text):
    # 為檔案名稱生成一個時間戳以確保唯一性
    timestr = time.strftime("%Y%m%d-%H%M%S")
    
    # 將原始文本以base64格式進行編碼以供檔案下載
    b64 = base64.b64encode(raw_text.encode()).decode()
    
    # 創建一個帶有時間戳的新檔案名
    new_filename = "code_review_analysis_file_{}_.txt".format(timestr)
    
    st.markdown("#### 下載檔案 ✅###")
    
    # 創建一個帶有編碼內容和檔案名供下載的HTML連結
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">點擊這裡!!</a>'
    
    # 使用Streamlit markdown顯示HTML連結
    st.markdown(href, unsafe_allow_html=True)

# 捕獲.py檔案數據
data = st.file_uploader("上傳Python檔案",type=".py")

if data:

    # 創建一個StringIO物件，並用'data'的解碼內容初始化它
    stringio = StringIO(data.getvalue().decode('utf-8'))

    # 讀取StringIO物件的內容，並將其存儲在變量'read_data'中
    fetched_data = stringio.read()

    # 可選，解除注釋以下行以將讀取的數據寫入streamlit應用
    st.write(fetched_data)

    # 使用指定的模型名稱"gpt-3.5-turbo"和溫度0.9初始化ChatOpenAI實例。
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

    # 創建一個SystemMessage實例，帶有指定的內容，提供有關助手角色的資訊。
    systemMessage = SystemMessage(content="你是一個代碼審查助手。提供詳細建議以改進給定的Python代碼，並逐行提及現有代碼並適當縮進")

    # 創建一個HumanMessage實例，內容從某些數據源讀取。
    humanMessage = HumanMessage(content=fetched_data)

    # 調用ChatOpenAI實例的chat方法，傳遞包含系統和人類消息的消息列表。
    # 最近langchain建議使用invoke函數 :)
    finalResponse = chat.invoke([systemMessage, humanMessage])

    
    #顯示審查評論
    st.markdown(finalResponse.content)


    text_downloader(finalResponse.content)