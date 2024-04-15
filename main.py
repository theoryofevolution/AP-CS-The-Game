import streamlit as st
import streamlit.components.v1 as components
import json
import random
from datetime import datetime
st.set_page_config('AP CS: The Game', layout="wide", initial_sidebar_state="collapsed")
def load_questions():
    with open('question_bank.json', 'r') as file:
        data = json.load(file)
    return data

def get_random_questions(questions, num=5):
    valid_questions = [q for q in questions if q["question_path"]]
    selected_questions = random.sample(valid_questions, k=min(num, len(valid_questions)))
    return selected_questions

if 'selected_questions' not in st.session_state or st.button("Reload Questions"):
    all_questions = load_questions()
    st.session_state.selected_questions = get_random_questions(all_questions)
    st.session_state.correct_answers = {q['question_path']: q['question_answer'] for q in st.session_state.selected_questions}
    st.session_state.quiz_started = False
    st.session_state.start_time = None


st.markdown("<h1 style='text-align: center; '>AP CS: The Game</h1>", unsafe_allow_html=True)

if st.text_input("Enter a username to start challenge (This will be your username on the leaderboard)"):
    st.write("""The challenge consists of 5 random questions picked from the database. You have unlimited time, so feel free to spend as much time as you want on each question. But do know, the person who gets the most questions right in the least amount of time gets the top place on the leaderboard. Your goal is to complete these questions as fast as you can. Take a piece of paper to begin Click the button to begin the challenge.""")

    if st.button("Begin Challenge"):
        st.session_state.quiz_started = True
        st.session_state.start_time = datetime.now()
    if st.session_state.quiz_started:
        with st.form(key='questions_form'):
            user_answers = {}
            for i, question in enumerate(st.session_state.selected_questions, start=1):
                st.write(f"Question {i}")
                st.image(question['question_path'], width=500)
                user_answers[question['question_path']] = st.radio(f"Options for Question {i}", ["A", "B", "C", "D", "E"], key=f'q{i}')

            submitted = st.form_submit_button("Submit")
            if submitted:
                end_time = datetime.now()
                duration = end_time - st.session_state.start_time
                score = sum(1 for path, answer in user_answers.items() if answer == st.session_state.correct_answers[path])
                st.session_state.quiz_started = False  # Optionally reset the quiz state
                st.success(f"You have submitted the challenge! Your score: {score}/{len(user_answers)}. Total time taken: {duration}")

