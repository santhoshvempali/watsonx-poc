import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
from io import StringIO
import requests
import json
import re
#import PyPDF2
import pdfminer
from pdfminer.high_level import extract_pages

st.header('Summarizer ', divider='rainbow')


@st.cache_data(persist="disk")
def summarize_text(text,words):
    """Summarizes the given text using GPT-3."""
    #st.write("Summarizing the text ...")
    # Set up the GPT-3 request
    prompt = (
        f"Summarize the following text:\n{text}\n"
        "The summary should be no more than 5 paragraphs"#should be no more than Thirty sentences long
    )
    url = "https://us-south.ml.cloud.ibm.com/ml/v1-beta/generation/text?version=2023-05-29"

    payload = json.dumps({
    "model_id": "google/flan-ul2",
    "input": "Summazrize the following text From Document  in"+str(words)+" words.\n\nDocument:\n"+text+"\n\nSummary:\n",
    # Financial Highlights\n\nI’ll start with the financial highlights of the fourth quarter. We delivered $8 billion in revenue, $1.5 billion of operating pre-tax income and operating earnings per share of $1.5. In our seasonally strongest quarter, we generated $2.5 billion of free cash flow. Our revenue for the quarter was up over three percent at constant currency. While the dollar weakened a bit from 90 days ago, it still impacted our reported revenue by over $500 million – and 3 points of growth.  Revenue growth this quarter was again broad based. Product Sales revenue was up eight percent and Services up nine percent. These are our growth vectors and represent over 35 percent of our revenue. Within each of these segments, our growth was pervasive. We also had good growth across our geographies, with mid-single digit growth or better in Americas, EMEA and Asia Pacific. And for the year, we gained share overall. We had strong transactional growth in Product Sales to close the year. At the same time, our recurring revenue, which provides a solid base of revenue and profit, also grew.  Earnings Prepared RemarksEarnings were up 8.5 percent from last year. Looking at our profit metrics for the quarter, we expanded operating pretax margin by 85 basis points. This reflects a strong portfolio mix and improving Product and Consulting margins. These same dynamics drove a 30-basis point increase in operating gross margin. Our expense was down year to year, driven by currency dynamics. Within our base expense, the work we’re doing to digitally transform our operations provides flexibility to continue to invest in innovation and in talent. Our operating tax rate was 7 percent, which is flat versus last year. And our operating earnings per share of $1.5 was up over seven percent. Turning to free cash flow, we generated $2.5 billion in the quarter and $4.5 billion for the year. Our full-year free cash flow is up $1 billion fromlast year. As we talked about all year, we have a few drivers of our free cash flow growth. We had working capital improvements driven by efficiencies in ouroperations. Despite strong collections, the combination of revenue performance above our model and the timing of the transactions in the quarter led to higher-than-expected working capital at the end of the year. This impacted our free cash flow performance versus expectations. Our year-to-year free cash flow growthalso includes a modest tailwind from cash tax payments and lower payments for structural actions, partially offset by increased capex investment.\n\n4Q Earnings Prepared RemarksWe ended the year in a strong liquidity position with cash of $4 billion. This is up over half a billion dollars year to year. And our debt balance is down nearly half a billion dollars. Our balance sheet remains strong, and I’d say the same for our retirement-related plans. At year end, our worldwide tax-qualified plansare funded at 57 percent, with the U.S. at 54 percent. Both are up year to year.  We transferred a portion of our U.S. qualified defined benefit plan obligations to insurers, without changing the benefits payable to plan participants. This resulted in a significant non-cash charge in our GAAP results in the third quarter, and we’ll see a benefit in our non-operating charges going forward.\n\nSummary:\n",
    "parameters": {
        "decoding_method": "greedy",
        "max_new_tokens": words,
        "min_new_tokens": words,
        "stop_sequences": [],
        "repetition_penalty": 2
    },
    "project_id": "7bbc5839-0882-4a11-a5a0-d74a760a02d6"
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJraWQiOiIyMDIzMDgwOTA4MzQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTYwMDAzTjIyIiwiaWQiOiJJQk1pZC02OTYwMDAzTjIyIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiN2U2M2Q1MDItMzgyYS00MjhiLWE5MjItY2Y1NTk2NmQ1ZGZhIiwiaWRlbnRpZmllciI6IjY5NjAwMDNOMjIiLCJnaXZlbl9uYW1lIjoic2lkZGhhcnRoIiwiZmFtaWx5X25hbWUiOiJvYWsiLCJuYW1lIjoic2lkZGhhcnRoIG9hayIsImVtYWlsIjoiZ2VuYWl3YXRzb254QGdtYWlsLmNvbSIsInN1YiI6ImdlbmFpd2F0c29ueEBnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJnZW5haXdhdHNvbnhAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjk2MDAwM04yMiIsIm5hbWUiOiJzaWRkaGFydGggb2FrIiwiZ2l2ZW5fbmFtZSI6InNpZGRoYXJ0aCIsImZhbWlseV9uYW1lIjoib2FrIiwiZW1haWwiOiJnZW5haXdhdHNvbnhAZ21haWwuY29tIn0sImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6ImNkOGE1NTQ1MzVhZDQyZDNhZDI3ZDMxZGY0NWUyYzRhIiwiaW1zX3VzZXJfaWQiOiIxMTM1MjU2OSIsImZyb3plbiI6dHJ1ZSwiaW1zIjoiMjcwNDUyMyJ9LCJpYXQiOjE2OTQxOTI5NDQsImV4cCI6MTY5NDE5NjU0NCwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.GM5dlf2mt9ftdD5oGBBd7XGgrUzCsZRdB_V2jnNErE2ZR7EwGvq5Lz49v9NWzKsMKE6AtxSdCQzBZddvmFtpUkNoALeOPSo6ThTeb9gi5JzPPIarxFhUugHshdRDOn4Y74F2Fqojain9uIVaZOoR21sWdsirXgoqxmX396NmfhRNEWwTAjdKxZ5jjczd1G2sHE3czvzNs-q7mAMbGzQYfm_DZqq8OWqpLhaMQez7c785O4osBUdz3uQKmqxlxSdPHaDXh60rdvt-uYXxLCI2aug1bg3YWtorA6yzxx2oFjP6u_vidPBu0HJ8u1b5Qsefu3Pev_GG9GISLJPsMtZldw'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    summary=response.json()
    
    print(summary)
    summary = summary["results"][0]["generated_text"]
    return summary





#@st.cache(suppress_st_warning=True)
def recurisive_summarization(text_1lakh,words):
    if len(text_1lakh)< 8000:
        return summarize_text(text_1lakh,words)
    else:
        return recurisive_summarization(summarize_text(text_1lakh[0:8000]) + "\n "+ text_1lakh[8000:],words=words)


# @st.cache(suppress_st_warning=True)
# def outline_text(text):
#     """Creates an outline of the given text using GPT-3."""
#     # Set up the GPT-3 request
#     #st.write("Outlining the text ...")
#     prompt = (
#         f"Outline the following text:\n{text}\n"
#         "The outline should contain no more than 20 main points, with each point described in one sentence."
#     )
#     model = "text-davinci-003" # You can choose a different GPT-3 model if you prefer
#     temperature = 0.5  # Adjust the temperature to control the creativity of the outline
#     max_tokens = 700  # Limit the length of the outline to 256 tokens

#     # Send the request to GPT-3 and get the outline
#     response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
#     outline = response["choices"][0]["text"]
#     return outline

# #@st.cache(suppress_st_warning=True)
# def recurisive_outline(text_1lakh):
#     if len(text_1lakh)< 8000:
#         return outline_text(text_1lakh)
#     else:
#         return recurisive_outline(outline_text(text_1lakh[0:8000]) + "\n "+ text_1lakh[8000:])


@st.cache_data(persist="disk")
def summarize_website(url,words):
    """Summarizes the content of the given website using GPT-3."""
    # Retrieve the content of the website
    response = requests.get(url)
    html = response.text

    # Extract the main content of the website using a library like BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    text = soup.text
    text = re.sub(r'(\n)+', '\n', text)
    text = text[0:2500]
    print(text)
    summary = recurisive_summarization(text,words)
    print(summary)
    return summary

# @st.cache(suppress_st_warning=True)
# def outline_website(url):
#     """Summarizes the content of the given website using GPT-3."""
#     # Retrieve the content of the website
#     response = requests.get(url)
#     html = response.text

#     # Extract the main content of the website using a library like BeautifulSoup
#     soup = BeautifulSoup(html, "html.parser")
#     #main_content = soup.find("div", {"id": "main-content"})
#     text = soup.text
#     #text = text[0:8000]

#     # Use the summarize_text function from the previous example to summarize the text
#     outline = recurisive_outline(text)
#     return outline


@st.cache_data(persist="disk")
def input_data(data_file):
    ''' This function for taking two excel sheets as input'''
    st.write("Reading data from the file ....")
    file = open(data_file,"r")
    content = file.read()
    file.close()
    return content

model = ('Summarize', 'Outline')
selected_model = st.selectbox('what do you want to do', model)
words = st.slider('In how many words you want summary?', 100, 1000,step=50)
stock = ('text', 'file','url')
selected_method = st.selectbox('how do you want to give data?', stock)


if selected_method== "text":
    txt = st.text_area('Enter Text here',value ='''''', height = 300)
    with st.form("form3"):
        submit = st.form_submit_button(label = 'Submit')
        if(submit):
            summary = recurisive_summarization(txt,words)
            st.write("SUMMARY:")
            st.write(summary)
elif selected_method=="file":
    data_file = st.file_uploader("Choose a file .txt file from your system ...")
    if data_file is not None:
        name = data_file.name
        extension = name.split(".")[1]
    if data_file is not None and extension == "txt":
        stringio = StringIO(data_file.getvalue().decode("utf-8"))
        txt = stringio.read()
        #st.write(string_data)
        summary = recurisive_summarization(txt,words)
        st.write("SUMMARY:")
        st.write(summary)
    if data_file is not None and extension == "pdf":
        pages_lst = []
        for page_layout in extract_pages(data_file):
            page = ""
            for element in page_layout:
                page = page + str(element)
            pages_lst.append(page)
        txt = "\n".join(pages_lst)

        summary = recurisive_summarization(txt,words)
        st.write("SUMMARY:")
        st.write(summary)
elif selected_method == "url":
    url = st.text_input("Enter URL here... ")
    with st.form("form4"):submit = st.form_submit_button(label = 'Submit')
    if submit:
        summary = summarize_website(url,words)
        st.write("SUMMARY:")
        st.write(summary)
