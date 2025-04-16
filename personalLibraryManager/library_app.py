import streamlit as st
import json
import os

# ----------- Constants -----------
LIBRARY_FILE = "library.txt"

# ----------- Load & Save Functions -----------
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

# ----------- Session Setup -----------
if 'library' not in st.session_state:
    st.session_state.library = load_library()

# ----------- Page Title -----------
st.title("📚 Personal Library Manager")

# ----------- Sidebar Menu -----------
menu = st.sidebar.selectbox("📋 Select an Option", [
    "Add a Book",
    "Remove a Book",
    "Search for a Book",
    "Display All Books",
    "Display Statistics"
])

# ----------- Add a Book -----------
if menu == "Add a Book":
    st.header("➕ Add a New Book")
    title = st.text_input("📖 Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, step=1)
    genre = st.text_input("🏷️ Genre")
    read = st.checkbox("✅ Have you read it?")

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
        st.success("🎉 Book added successfully!")

# ----------- Remove a Book -----------
elif menu == "Remove a Book":
    st.header("❌ Remove a Book")
    titles = [book["title"] for book in st.session_state.library]
    selected_title = st.selectbox("Select book to remove", titles)

    if st.button("Remove Book"):
        st.session_state.library = [book for book in st.session_state.library if book["title"] != selected_title]
        save_library(st.session_state.library)
        st.success(f"🗑️ '{selected_title}' removed successfully!")

# ----------- Search for a Book -----------
elif menu == "Search for a Book":
    st.header("🔍 Search for a Book")
    search_term = st.text_input("Enter title or author")

    if search_term:
        results = [
            book for book in st.session_state.library
            if search_term.lower() in book["title"].lower()
            or search_term.lower() in book["author"].lower()
        ]
        if results:
            for book in results:
                st.markdown(f"""
                **📖 Title:** {book['title']}  
                **✍️ Author:** {book['author']}  
                **📅 Year:** {book['year']}  
                **🏷️ Genre:** {book['genre']}  
                **📘 Read:** {"Yes" if book['read'] else "No"}
                ---
                """)
        else:
            st.warning("No matching books found.")

# ----------- Display All Books -----------
elif menu == "Display All Books":
    st.header("📚 All Books in Library")
    if st.session_state.library:
        for book in st.session_state.library:
            st.markdown(f"""
            **📖 Title:** {book['title']}  
            **✍️ Author:** {book['author']}  
            **📅 Year:** {book['year']}  
            **🏷️ Genre:** {book['genre']}  
            **📘 Read:** {"Yes" if book['read'] else "No"}
            ---
            """)
    else:
        st.info("No books in library.")

# ----------- Statistics -----------
elif menu == "Display Statistics":
    st.header("📊 Library Statistics")
    total = len(st.session_state.library)
    read = sum(book["read"] for book in st.session_state.library)

    if total > 0:
        percent_read = (read / total) * 100
        st.write(f"📚 Total books: **{total}**")
        st.write(f"✅ Books read: **{read}** ({percent_read:.2f}%)")
    else:
        st.info("Library is empty.")
