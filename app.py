import streamlit as st

from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.schema.output_parser import StrOutputParser

st.set_page_config(page_title="ITC Financial Analysis ChatBot", layout="centered")

# API key
API_key = "Your Gemini API KEY"
    
st.markdown("""
<h1 style='text-align: center; color: white; font-size: 42px;'>
📊 ITC Financials with AI
</h1>
""", unsafe_allow_html=True)


# Memory buffer for chat history
memory_buffer = {"chat_history": []}

# Minimalistic and background-matching style for the New Chat button
new_chat_button = """
<style>
    .stButton>button {
        background-color: rgba(255, 255, 255, 0.2);  /* Semi-transparent white */
        color: white;
        font-size: 16px;
        border: None;
        border-radius: 20px;
        padding: 12px 24px;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
        width: 100%;
        display: black;
    }
    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.4);  /* Lighter on hover */
        transform: scale(1.05);  /* Subtle scaling effect */
    }
    .stButton>button:active {
        transform: scale(0.98);  /* Slight shrink on click */
    }
</style>
"""
st.markdown(new_chat_button, unsafe_allow_html=True)


# End chat button
if st.button("New Chat"):
    memory_buffer["chat_history"] = []

# import zipfile

# Load Chroma vector DB from zip
# with zipfile.ZipFile(r"C:\Users\hi\Desktop\Neuzen AI\chroma_db_backup.zip", 'r') as zip_ref:
#     zip_ref.extractall('chroma_db')


# Embeddings and vector store
embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
vectorstore = Chroma(persist_directory='YOUR CHROMA_DB DIRECTORY', embedding_function=embedding)
mmr_retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3, "lambda_mult": 1})

# Helper functions
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_docs_and_context(question):
    docs = mmr_retriever.get_relevant_documents(question)
    return {"question": question, "docs": docs, "context": format_docs(docs)}

# Chain parts
parallel_chain = RunnableLambda(lambda x: {
    "question": x["input"],
    **get_docs_and_context(x["input"])
})

chat_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
     You are a domain-specific AI financial analyst focused on company-level performance evaluation.

     Your task is to analyze and respond to user financial queries *strictly based on the provided transcript data*: {context}.

     Rules:
     1. ONLY extract facts, figures, and insights that are explicitly available in the transcript.
     2. If data is *missing or partially available*, clearly state: "The required data is not available in the current transcript." Then provide a generic but relevant explanation based on standard financial principles.
     3. Maintain numerical accuracy and avoid interpretation beyond data boundaries.
     4. Prioritize answers relevant to *ITC Ltd.*, but keep response format adaptable to other firms and fiscal years.
     5. Clearly present year-wise or metric-wise insights using bullet points or structured formats if applicable.

     Your goals:
     - Ensure 100% fidelity to source transcript.
     - Do not assume or hallucinate missing numbers.
     - Use clear, reproducible reasoning steps (e.g., show which line items support your conclusion).
     - Output should be modular enough to scale across other companies and time periods.

     Respond only to this question from the user.
     """),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}")
])

llm = ChatGoogleGenerativeAI(api_key=API_key, model="gemini-2.0-flash-exp", temperature=1)
parser = StrOutputParser()

# Chat memory logic
def get_history_from_buffer(_):
    return memory_buffer['chat_history']

runnable_get_history_from_buffer = RunnableLambda(get_history_from_buffer)

main_chain = (
    parallel_chain |
    RunnableLambda(lambda x: {
        "llm_input": {"input": x["question"], "context": x["context"]},
        "docs": x["docs"]
    }) |
    RunnableLambda(lambda x: {
        "result": (chat_prompt | llm | parser).invoke(x["llm_input"]),
        "source_documents": x["docs"]
    })
)

chain = RunnablePassthrough.assign(chat_history=runnable_get_history_from_buffer) | main_chain

# Display previous chat messages
for msg in memory_buffer["chat_history"]:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Chat input
user_input = st.chat_input("Ask a question about ITC's financials...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add user input to memory
    memory_buffer["chat_history"].append(HumanMessage(content=user_input))

    # Call the chain
    output = chain.invoke({"input": user_input})
    ai_response = output["result"]

    # Add AI response to memory
    memory_buffer["chat_history"].append(AIMessage(content=ai_response))

    # Show AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)

        # Show sources
        if output.get("source_documents"):
            st.markdown("#### Source Documents", unsafe_allow_html=True)
            for i, doc in enumerate(output["source_documents"], 1):
                source_name = doc.metadata.get("source", f"Document {i}")
                st.markdown(f"*{i}. {source_name}*")
