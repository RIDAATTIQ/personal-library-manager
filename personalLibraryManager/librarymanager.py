import streamlit as st
import json
import os

LIBRARY_FILE = "library.txt"

# Load/Save
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Load session library
if 'library' not in st.session_state:
    st.session_state.library = load_library()

st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox("Select an Option", [
    "Add a Book", "Remove a Book", "Search a Book",
    "Display All Books", "Display Statistics"
])

if menu == "Add a Book":
    st.header("📖 Add a New Book")

    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read it?")

    if st.button("Add Book"):
        new_book = {
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read
        }
        st.session_state.library.append(new_book)
        save_library(st.session_state.library)
        st.success("✅ Book added successfully!")




