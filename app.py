import streamlit as st
import json
import os


FILE_PATH = "library.json"


def load_library():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    return []


def save_library(library):
    with open(FILE_PATH, "w") as file:
        json.dump(library, file, indent=4)


library = load_library()

# Custom CSS for full UI redesign with updated background color
st.markdown(
    """
    <style>
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1f2937 !important;
        color: #e0e7ff !important;
        font-weight: 600;
        padding-top: 20px;
    }
    .css-1d391kg .css-1v3fvcr {
        color: #e0e7ff !important;
        font-weight: 600;
    }
    /* Sidebar radio buttons */
    .css-1d391kg .stRadio > div > label {
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        display: block;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .css-1d391kg .stRadio > div > label:hover {
        background-color: #374151 !important;
    }
    .css-1d391kg .stRadio > div > label[aria-checked="true"] {
        background-color: #4f46e5 !important;
        color: white !important;
        font-weight: 700;
    }
    /* Main header banner */
    .main-header {
        font-size: 40px;
        font-weight: 700;
        color: white;
        text-align: center;
        padding: 30px 0;
        background: linear-gradient(90deg, #4f46e5, #3b82f6);
        border-radius: 8px;
        margin-bottom: 30px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    /* Main content background */
    .block-container {
        background-color: #374151;
        padding: 30px 50px 50px 50px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        color: #e0e7ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Status badges */
    .status-not-read {
        background-color: #fee2e2;
        color: #b91c1c;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.9em;
        display: inline-block;
    }
    .status-reading {
        background-color: #fef3c7;
        color: #78350f;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.9em;
        display: inline-block;
    }
    .status-completed {
        background-color: #d1fae5;
        color: #065f46;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.9em;
        display: inline-block;
    }
    /* Book card */
    .book-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: box-shadow 0.3s ease;
    }
    .book-card:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    /* Buttons */
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        color: white;
    }
    /* Footer */
    .footer {
        font-size: 12px;
        color: #6b7280;
        text-align: center;
        margin-top: 50px;
        padding-bottom: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">📚 Personal Library Manager</div>', unsafe_allow_html=True)

menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Books", "Library Stats", "View All Books"])

if menu == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1800, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.selectbox("Read Status", ["Not Read", "Reading", "Completed"])

    if st.button("Add Book"):
        if title and author:
            library.append({
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "status": read_status
            })
            save_library(library)
            st.success(f"📖 '{title}' by {author} added to your library!")
        else:
            st.error("Please fill in both the Title and Author fields.")

elif menu == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    book_titles = [book["title"] for book in library]

    if book_titles:
        book_to_remove = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f"❌ '{book_to_remove}' has been removed.")
    else:
        st.warning("No books available to remove.")

elif menu == "Search Books":
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("Enter title, author, or genre")

    if search_query:
        results = [book for book in library if search_query.lower() in (book["title"] + book["author"] + book["genre"]).lower()]

        if results:
            for book in results:
                status_class = ""
                if book['status'] == "Not Read":
                    status_class = "status-not-read"
                elif book['status'] == "Reading":
                    status_class = "status-reading"
                elif book['status'] == "Completed":
                    status_class = "status-completed"
                st.markdown(
                    f"<div class='book-card'><strong>📖 {book['title']}</strong> by {book['author']}<br>"
                    f"<em>{book['genre']}</em> ({book['year']})<br>"
                    f"<span class='{status_class}'>[{book['status']}]</span></div>",
                    unsafe_allow_html=True
                )
        else:
            st.warning("No matching books found.")

elif menu == "Library Stats":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    genres = list(set(book["genre"] for book in library))
    read_count = sum(1 for book in library if book["status"] == "Completed")

    st.write(f"📚 Total Books: **{total_books}**")
    st.write(f"📖 Books Read: **{read_count}**")
    st.write(f"📂 Unique Genres: **{len(genres)}** ({', '.join(genres)})")

elif menu == "View All Books":
    st.subheader("📚 Your Book Collection")

    if library:
        for book in library:
            status_class = ""
            if book['status'] == "Not Read":
                status_class = "status-not-read"
            elif book['status'] == "Reading":
                status_class = "status-reading"
            elif book['status'] == "Completed":
                status_class = "status-completed"
            st.markdown(
                f"<div class='book-card'><strong>📖 {book['title']}</strong> by {book['author']}<br>"
                f"<em>{book['genre']}</em> ({book['year']})<br>"
                f"<span class='{status_class}'>[{book['status']}]</span></div>",
                unsafe_allow_html=True
            )
    else:
        st.warning("No books in your collection.")

st.markdown('<div class="footer">Personal Library Manager &copy; 2024</div>', unsafe_allow_html=True)
