import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


with open(r"C:\Users\Lenovo\Desktop\interviewQuestion\mcqgen\Response.json",'r') as file:
    RESPONSE_JSON = "json.load(file)"


st.title("MCQs Creator Application with LangChain")

with st.form("user_inputs"):

    upload_file=st.file_uploader("Upload a pdf or text file")

    mcq_count=st.number_input("Number of MCQs", min_value=3, max_value=50)

    subject=st.text_input("Insert Subject",max_chars=20)

    tone=st.text_input("Complexity level of Question",max_chars=20,placeholder="Simple")

    button=st.form_submit_button("Create MCQs")

    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(upload_file)

                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }

                    )

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response,dict):

                    quiz=response.get("quiz",None)
                    if quiz is not None:
                        st.write("Output is:", quiz)
                        #st.write("# Quiz Data")

                        #for question_data in quiz.get("questions", []):
                            #st.write("## Question:", question_data["question"])
                            #st.write("**Options:**")
                            #for option in question_data["options"]:
                                #st.write("-", option)
                            #st.write("**Answer:**", question_data["answer"])

                else:
                    st.write(response)
















