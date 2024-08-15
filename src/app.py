import streamlit as st

from common.utils import initialize_db_connection, build_few_shots_prompt, generate_sql_query, run_query, \
    get_vertexai_llm, chain_query

def main():
    # Configure settings of the page
    st.set_page_config(page_title="Chat with SQL Databases", page_icon="🧊", layout="wide")

    # Add a header
    st.header("Chat with SQL Databases using Gemini-Pro💬🤖")

    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Widget to provide questions
    user_question = st.text_input("Ask a question from the Database")

    if st.button("Gemini-Pro"):
        with st.spinner("Thinking..."):

            # DB connection
            db = initialize_db_connection()

            # Generate few shots prompt
            few_shots_prompt = build_few_shots_prompt(db)

            # Generate SQL query
            sql_query = generate_sql_query(prompt=few_shots_prompt, user_question=user_question)

            # Execute SQL query
            query_results = run_query(db=db, sql_query=sql_query)

            # LLM
            llm = get_vertexai_llm()

            # Final answer
            answer = chain_query(llm=llm, sql_response=query_results)

            # Update chat history
            st.session_state.chat_history.append({"question": user_question, "sql_query": sql_query, "answer": answer})

            st.write(f"**SQL Query:** `{sql_query}`")
            st.write(answer)

            st.success("Done")

    # Display chat history
    st.subheader("Chat History")
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['question']}")
        st.write(f"**SQL Query:** `{chat['sql_query']}`")
        st.write(f"**Gemini-Pro:** {chat['answer']}")

if __name__ == "__main__":
    main()
