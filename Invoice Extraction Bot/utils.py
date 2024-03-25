#因為Langchain團隊積極改善工具，我們可以看到每週都有很多變化，
#作為其一部分，下面的導入已被淘汰
#from langchain.llms import OpenAI
#https://replicate.com/
from langchain_openai import OpenAI

from pypdf import PdfReader
#from langchain.llms.openai import OpenAI
import pandas as pd #==> 處理表格內容
import re 
import replicate 
from langchain.prompts import PromptTemplate

#從PDF文件中提取資訊
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



#功能：從文本中提取數據...
def extracted_data(pages_data):

    template = """Please Extract all the following values : invoice no., Description, Quantity, date, 
         Unit price , Amount, Total, email, phone number and address from this data: {pages}

         Expected output: remove any dollar symbols {{'Invoice no.': '1001329','Description': 'Office Chair','Quantity': '2','Date': '5/4/2023','Unit price': '1100.00$','Amount': '2200.00$','Total': '2200.00$','Email': 'Santoshvarma0988@gmail.com','Phone number': '9999999999','Address': 'Mumbai, India'}}
         """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    llm = OpenAI(temperature=.7)
    full_response=llm(prompt_template.format(pages=pages_data))
    

    #以下代碼將在我們希望使用LLAMA 2模型時使用，我們將使用Replicate來托管我們的模型....
    
    #output = replicate.run('replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1', 
                           #input={"prompt":prompt_template.format(pages=pages_data) ,
                                  #"temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})
    
    #full_response = ''
    #for item in output:
        #full_response += item
    

    #print(full_response)
    return full_response


# 迭代用戶上傳的PDF文件列表，一個接一個地處理文件
def create_docs(user_pdf_list):
    
    df = pd.DataFrame({'Invoice no.': pd.Series(dtype='str'),
                   'Description': pd.Series(dtype='str'),
                   'Quantity': pd.Series(dtype='str'),
                   'Date': pd.Series(dtype='str'),
	                'Unit price': pd.Series(dtype='str'),
                   'Amount': pd.Series(dtype='int'),
                   'Total': pd.Series(dtype='str'),
                   'Email': pd.Series(dtype='str'),
	                'Phone number': pd.Series(dtype='str'),
                   'Address': pd.Series(dtype='str')
                    })

    
    
    for filename in user_pdf_list:
        
        print(filename)
        raw_data=get_pdf_text(filename)
        #print(raw_data)
        print("提取了原始數據")

        llm_extracted_data=extracted_data(raw_data)
        #print(llm_extracted_data)
        #print("LLM提取的數據")
        #將項目添加到我們的列表中 - 添加數據及其元數據

        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)

       

        if match:
            extracted_text = match.group(1)
            # 將提取的文本轉換為字典
            data_dict = eval('{' + extracted_text + '}')
            print(data_dict)
        else:
            print("未找到匹配。")
            # 初始化data_dict
            data_dict = {}

        
        df=df._append([data_dict], ignore_index=True)
        print("********************完成***************")
        #df=df.append(save_to_dataframe(llm_extracted_data), ignore_index=True)

    df.head()
    return df
