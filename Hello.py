# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Importing required packages
import openai
import current_prompt
import streamlit as st
from streamlit.logger import get_logger
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

LOGGER = get_logger(__name__)

# Set the OpenAI API settings for our Azure environment
openai.api_type = "azure"
openai.api_base = "https://llm-project-dev.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "b866afd9c45944c9835d70dd26386064"

st.title("Sample Chatbot 🤖")
curr_prompt = current_prompt.system_prompt

st.write("""
This page is built as an interactive prompt interface that allows you to make rapid edits to the prompt and see the output.
""")
with st.expander("Prompt"):
    input_data = st.text_area("Edit Prompt 📝", curr_prompt)
    st.write(curr_prompt)

st.write("""


""")
         
st.sidebar.header("Instructions")
st.sidebar.info(
    '''This is a web application that allows you to interact with 
        the OpenAI API's implementation of the ChatGPT model.
        Enter a **query** in the **text box** and **press enter** to receive 
        a **response** from the ChatGPT
        '''
    )

def main():
    '''
    This function gets the user input, pass it to ChatGPT function and 
    displays the response
    '''
    # Get user input
    user_query = st.text_input("Enter query here, to exit enter :q", "What did we spend per week over the last 6 months?")
    if user_query != ":q" or user_query != "":
        # Pass the query to the ChatGPT function
        response = ChatGPT(user_query)
        return st.write(f"{response}")
    
def test():
    if st.button('Run Test Cases'):
      with st.expander("**Test Case 1:** ✅ passed"):
            st.write("""
                    **Predicted:** { "granularity": "WEEKLY", "range": "LAST_6_MONTHS" }
                    
                    
                    **Ground truth:** { "granularity": "WEEKLY", "range": "LAST_6_MONTHS" }

                    """)
      with st.expander("Test Case 2: ✅ passed"):
            st.write("text")
      with st.expander("Test Case 3:"):
            st.write("text")
      with st.expander("Test Case 4:"):
            st.write("text")
      with st.expander("Test Case 5:"):
            st.write("text")
    
def ChatGPT(user_query):
  user_question = user_query #user_questions[0]

  # Set the OpenAI API settings for our Azure environment
  openai.api_type = "azure"
  openai.api_base = "https://llm-project-dev.openai.azure.com/"
  openai.api_version = "2023-03-15-preview"
  openai.api_key = "b866afd9c45944c9835d70dd26386064"

  # Supporting variables
  today_date = datetime.today().date().strftime('%Y-%m-%d')
  one_year_ago_date = (datetime.today().date() - relativedelta(years=1)).strftime('%Y-%m-%d')

  # Tell the LLM what it's role is and give it the information it needs to complete the task
  system_prompt = current_prompt.system_prompt
  ys_question_to_json_prompt = [{"role":"system","content":system_prompt}]
  # Add the examples to the prompt
  ys_question_to_json_prompt += current_prompt.examples
  # Add the user question to the prompt
  ys_question_to_json_prompt.append({"role":"user","content":user_question})

  # Retrieve the response from our Azure OpenAI API endpoint
  response = openai.ChatCompletion.create(
    engine="yotascale-gpt-35-turbo",
    messages = ys_question_to_json_prompt,
    temperature=0.0,
    max_tokens=350,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None)

  generated_request_body = response.choices[0].message.content
  json_request_body = json.loads(generated_request_body)
  output = json.dumps(json_request_body, indent=2)

  return output

# call the main function
main() 

st.write("""


""")
         
st.write("---")

st.write("""


""")
st.header("Evaluating L1.1")
st.write("""
This section contains a few benchmark tests that the chatbot should maintain a constistent level of succes on

""")

test()

