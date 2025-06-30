
import streamlit as st
import pandas as pd

data = pd.read_csv('questions_answers.csv')
qa_dict = dict(zip(data['Questions'].str.lower(), data['Answers']))

def preprocess_question(question):
    question = question.lower().strip()
    question = question.replace('?', '').replace("'", "").replace('"', '')
    question = question.replace('what', '').replace('how', '').replace('can', '')
    question = question.replace('does', '').replace('kepler', '').replace('college', '')
    return ' '.join(question.split())

def find_best_match(user_question, questions):
    user_question = preprocess_question(user_question)
    if user_question in questions:
        return user_question
    for q in questions:
        if user_question in q or q in user_question:
            return q
    user_words = set(user_question.split())
    max_overlap = 0
    best_match = None
    for q in questions:
        q_words = set(q.split())
        overlap = len(user_words.intersection(q_words))
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = q
    return best_match if max_overlap >= 2 else None

st.title("Kepler College Chatbot")
question = st.text_input("Ask me anything about Kepler College")
if question:
    user_question_processed = preprocess_question(question)
    questions = list(qa_dict.keys())
    answer = "I'm sorry, I don't have information about that." 
    if user_question_processed in questions:
        answer = qa_dict[user_question_processed]
    else:
        best_match = find_best_match(user_question_processed, questions)
        if best_match:
            answer = qa_dict[best_match]
    st.write(answer)
