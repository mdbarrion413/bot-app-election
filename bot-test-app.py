import streamlit as st

dictionary = {'Classification': ['Linear', 'Tree'], 'Regression': ['Logistic', 'Random']}


st.title("PBS 56th Annual Membership Meeting")

selected_section = st.sidebar.selectbox("Choose section:", sorted(dictionary.keys()))
selected_page = st.sidebar.radio("Choose page:", sorted(dictionary[selected_section]))

if st.button("Run model"):
    st.write(f"Running {selected_section}:{selected_page}")


