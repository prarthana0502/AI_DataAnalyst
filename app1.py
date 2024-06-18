import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from apikey import gemini_key

# Mock class to represent the Gemini API
class Gemini:
    def __init__(self, model, temperature=0):
        self.model = model
        self.temperature = temperature
    
   
# Set up Gemini API key
os.environ['GEMINI_API_KEY'] = gemini_key
load_dotenv(find_dotenv())

# Define the model ID for the Gemini model
model_id = "gemini-3.5-turbo-instruct"  # Hypothetical model ID

# Initialize Gemini with the new model ID
llm = Gemini(model=model_id, temperature=0)

st.title('AI Assistant for Data Science')
st.write("Hello, I am your AI Assistant and I am here to help you with data analysis")

with st.sidebar:
    st.write('''Your Data Science Adventure Begins with a CSV File.''')
    st.caption("That's why I'd love for you to upload a CSV file. Once we have your data in hand, we'll dive into understanding it. Then, we'll work together to shape your business challenge into a solution. I'll introduce you to the coolest machine learning models.")

    st.divider()
    st.caption("<p style='text-align:center'> made by RV students</p>", unsafe_allow_html=True)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def clicked():
    st.session_state.clicked = True

st.button("Let's get started", on_click=clicked)
if st.session_state.clicked:
    st.header('Exploratory Data Analysis Part')
    st.subheader('Solution')
    file_csv = st.file_uploader("Upload your file here!!!", type="csv")
    
    if file_csv is not None:
        file_csv.seek(0)
        df = pd.read_csv(file_csv, low_memory=False)
        
        @st.cache_data
        def steps_eda():
            return llm.generate_text('What are the steps of EDA')
        
        @st.cache_data
        def function_agent():
            st.write("**Data Overview**")
            st.write("The first rows of your dataset look like this:")
            st.write(df.head())
            st.write("*Data Cleaning*")
            columns_df = llm.generate_text("What are the meanings of the columns?")
            st.write(columns_df)
            missing_values = llm.generate_text("How many missing values are there?")
            st.write(missing_values)
            duplicates = llm.generate_text("Are there any duplicate values?")
            st.write(duplicates)
            st.write("*Data Summarization*")
            st.write(df.describe())
            correlation_analysis = llm.generate_text("Calculate correlations between variables")
            st.write(correlation_analysis)
            outliers = llm.generate_text("Identify outliers in the data")
            st.write(outliers)
            new_features = llm.generate_text("What new features would be interesting?")
            st.write(new_features)
            return
        
        @st.cache_data
        def function_question_variable(user_question_variable):
            st.line_chart(df[user_question_variable])
            summary_statistics = llm.generate_text(f"Give me a summary of the statistics of {user_question_variable}")
            st.write(summary_statistics)
            normality = llm.generate_text(f"Check for normality in {user_question_variable}")
            st.write(normality)
            outliers = llm.generate_text(f"Assess the presence of outliers in {user_question_variable}")
            st.write(outliers)
            trends = llm.generate_text(f"Analyze trends and seasonality in {user_question_variable}")
            st.write(trends)
            missing_values = llm.generate_text(f"Determine the missing values in {user_question_variable}")
            st.write(missing_values)
            return

        @st.cache_data
        def function_question_dataframe(user_question_dataframe):
            dataframe_info = llm.generate_text(user_question_dataframe)
            st.write(dataframe_info)
            return
 
        # Main 
        st.header('Exploratory Data Analysis')
        st.subheader('General Information about the Dataset')
        with st.sidebar:
            with st.expander('What are the steps of EDA'):
                steps = steps_eda()
                if steps:
                    st.write(steps)  

        function_agent()

        st.subheader("Variable of Study")
        user_question_variable = st.text_input("What variable are you interested in?")
        if user_question_variable:
            function_question_variable(user_question_variable)

        st.subheader('Further Study')
        user_question_dataframe = st.text_input("Is there anything else you would like to know about the dataframe?")
        if user_question_dataframe and user_question_dataframe.lower() not in ('', 'no'):
            function_question_dataframe(user_question_dataframe)
        elif user_question_dataframe.lower() in ('no'):
            st.write('')
