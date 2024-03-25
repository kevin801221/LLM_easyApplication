import streamlit as st
from langchain.prompts import PromptTemplate
# Recently the below import has been replaced by later one
# from langchain.llms import CTransformers
from langchain_community.llms import CTransformers

#Function to get the response back
def getLLMResponse(form_input,email_sender,email_recipient,email_style):
    # 使用OpenAI並設定溫度為0.9，模型為"text-davinci-003"

    # 為Llama-2-7B-Chat的包裝器，運行Llama 2於CPU上

    # 量化是通過將權重從16位浮點數轉換成8位整數來降低模型精度，
    # 使其能夠在資源有限的設備上有效部署，減少模型大小，同時保持性能。

    # C Transformers支持各種開源模型，
    # 其中包括像是Llama、GPT4All-J、MPT和Falcon等受歡迎的模型。


    # C Transformers是一個Python庫，它為使用GGML庫用C/C++實現的變換器模型提供了綁定


    llm = CTransformers(model='D:/readingtask_GPT/Langchain/llama2/models/llama-2-7b-chat.ggmlv3.q8_0.bin',     #https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main
                    model_type='llama',
                    config={'max_new_tokens': 256,
                            'temperature': 0.01})
    
    
    #Template for building the PROMPT
    template = """
    Write a email with {style} style and includes topic :{email_topic}.\n\nSender: {sender}\nRecipient: {recipient}
    \n\nEmail Text:
    
    """

    #Creating the final PROMPT
    prompt = PromptTemplate(
        input_variables=["style","email_topic","sender","recipient"],
        template=template,)

  
    #Generating the response using LLM
    #langchain has recommended to use 'invoke' function for the below please :)
    response=llm.invoke(prompt.format(email_topic=form_input,sender=email_sender,recipient=email_recipient,style=email_style))
    print(response)

    return response

#################### streamlit前端設定 #################################

st.set_page_config( page_title="Generate Emails",
                    page_icon='📧',
                    layout='centered',
                    initial_sidebar_state='collapsed')

st.header("Generate Emails 📧")

form_input = st.text_area('Enter the email topic', height=275)

#Creating columns for the UI - To receive inputs from user
col1, col2, col3 = st.columns([10, 10, 5])
with col1:
    email_sender = st.text_input('寄信者')
with col2:
    email_recipient = st.text_input('接收者')
with col3:
    email_style = st.selectbox('寫作風格',
                                    ('Formal', 'Appreciating', 'Not Satisfied', 'Neutral'),
                                       index=0)


submit = st.button("產生!!")

#When 'Generate' button is clicked, execute the below code
if submit:
    st.write(getLLMResponse(form_input,email_sender,email_recipient,email_style))
