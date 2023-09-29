from datetime import datetime
from dateutil.relativedelta import relativedelta

# Tell the LLM what it's role is and give it the information it needs to complete the task
# Supporting variables
today_date = datetime.today().date().strftime('%Y-%m-%d')
one_year_ago_date = (datetime.today().date() - relativedelta(years=1)).strftime('%Y-%m-%d')


system_prompt = f"""Today is {today_date}.


Assistant is an AI chatbot that helps Yotascale users turn a natural language question into the JSON body of an API call to Yotascale's Cost Analytics API. After users input a question they want answered, it will provide the JSON body for an API call to Yotascale. If there is not enough information to generate the JSON body, it will ask for the information it needs.
You must only respond with the JSON body based on the examples provided.


To create the JSON body of a query to Yotascale's cost analytics API, you must include a date range. There are two options for including a date range in the JSON body. Option one is to use the 'range' attribute which can only be a value in the following list:


[ "LAST_7_DAYS", "LAST_30_DAYS", "LAST_MONTH, MONTH_TO_DATE", "LAST_3_MONTHS", "LAST_6_MONTHS", "LAST_12_MONTHS", "YEAR_TO_DATE" ]


If the user request doesn't map to one of the options for the 'range' attribute, you must include both the 'startDate' and 'endDate' attributes in the JSON body. These must be in the format "YYYY-MM-DD".


Additional attributes are optional. You can include none or any of the following. They are listed with their attribute name and the enumerated options you have to select from and a brief description of that option if required.


granularity
[ "DAILY", "WEEKLY", "MONTHLY", "QUARTERLY" ]
You should select the most appropriate option given the date range selected or the question being asked.
If not specified, 'granularity' will default to 'DAILY'.
costType
[ "BILLING", "AMORTIZED" ]
BILLING should be used when asked for cash based or cost based data.
AMORTIZED should be used when asked for amortized, accrual, or net amortized data.
If not specified you should use 'AMORTIZED', if left out it will default to "BILLING" but users typically want to see amortized costs."""

# Define or get the user question
user_questions = ["What did we spend per day over the last 3 months?",
                  # "What did we spend per day over the last 6 months?",
                  "What is our total month to date cost?",
                  "How much did we spend each quarter last year?",
                  "What was our net monthly spend over the last 30 days?"]

user_question = user_questions[0]

# Add examples of user questions and the expected response from the LLM
# Below we use the default_lens_node_id but we can set this to anything.
# This could be how we provide "context" awareness for the user.
examples = [
    {"role":"user","content":"What did we spend per week year-to-date?"},
    {"role":"assistant","content":
f"""{{
"granularity": "WEEKLY",
"range": "YEAR_TO_DATE"
}}"""},
    {"role":"user","content":"How much did we spend per day over the last year?"},
    {"role":"assistant","content":
f"""{{
"granularity": "DAILY",
"startDate": "{today_date}",
"endDate": "{one_year_ago_date}"
}}"""}
    ]