import streamlit as st
import pickle
import numpy as np
import time

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="AI Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

# ----------------------------
# Load Files
# ----------------------------
popular_df = pickle.load(open("popular.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
books_data = pickle.load(open("books_data.pkl", "rb"))

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#0F2027,#203A43,#2C5364);
background-attachment:fixed;
}

h1{
color:white;
text-align:center;
font-size:48px;
font-weight:bold;
}

h3{
color:#FFD700;
text-align:center;
}

p{
color:white;
}

.stButton>button{
width:100%;
background:linear-gradient(90deg,#ff512f,#dd2476);
color:white;
border-radius:15px;
height:55px;
font-size:20px;
font-weight:bold;
border:none;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.05);
box-shadow:0px 0px 20px #ff4b4b;
}

div[data-baseweb="select"]{
background:white;
border-radius:10px;
}

img{
border-radius:15px;
box-shadow:0px 0px 15px black;
}

.footer{
text-align:center;
color:white;
padding:20px;
font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("📚 Project Information")

st.sidebar.info("""
### AI Book Recommendation System

This project recommends books using

✅ Collaborative Filtering

✅ Cosine Similarity

Built with:

• Python

• Pandas

• Scikit-Learn

• Streamlit
""")

st.sidebar.success("Made with ❤️ by Swati Chaturvedi")

# ----------------------------
# Header
# ----------------------------

st.markdown("<h1>📚 AI Book Recommendation System</h1>",unsafe_allow_html=True)

st.markdown(
"<h3>Find Your Next Favorite Book in Seconds</h3>",
unsafe_allow_html=True
)

st.write("")
st.write("")

# ============================================
# Recommendation Function
# ============================================

def recommend(book_name):

    index = np.where(books.index == book_name)[0][0]

    similar_items = sorted(
        list(enumerate(similarity[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    data = []

    for i in similar_items:

        temp = books_data[
            books_data["Book-Title"] == books.index[i[0]]
        ]

        item = []

        item.extend(
            temp.drop_duplicates("Book-Title")["Book-Title"].values
        )

        item.extend(
            temp.drop_duplicates("Book-Title")["Book-Author"].values
        )

        item.extend(
            temp.drop_duplicates("Book-Title")["Image-URL-M"].values
        )

        data.append(item)

    return data


# ============================================
# Book Selection
# ============================================

st.markdown("## 📖 Choose Your Favorite Book")

selected_book = st.selectbox(

    "Search Book",

    books.index.values

)

st.write("")

# ============================================
# Recommendation Button
# ============================================

if st.button("🚀 Recommend Books"):

    with st.spinner("🔍 Finding Similar Books..."):

        time.sleep(2)

        recommended_books = recommend(selected_book)

    st.success("✅ Recommendation Completed")

    st.write("")
    st.markdown("## 📚 Recommended Books")

    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [col1, col2, col3, col4, col5]

    for col, book in zip(columns, recommended_books):

        with col:

            st.image(book[2], use_container_width=True)

            st.markdown(
                f"""
                <div style="
                background:#ffffff15;
                padding:15px;
                border-radius:15px;
                text-align:center;
                height:170px;
                ">
                <h5 style="color:white;">
                {book[0]}
                </h5>

                <p style="color:#FFD700;">
                ✍ {book[1]}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )
            
            # ============================================
# Popular Books Section
# ============================================

st.write("")
st.write("")
st.markdown("---")
st.markdown(
    "<h2 style='text-align:center;color:#FFD700;'>🔥 Top 10 Popular Books</h2>",
    unsafe_allow_html=True
)

cols = st.columns(5)

for i in range(10):

    with cols[i % 5]:

        st.image(
            popular_df.iloc[i]["Image-URL-M"],
            use_container_width=True
        )

        st.markdown(
            f"""
            <div style="
            background:rgba(255,255,255,0.10);
            padding:12px;
            border-radius:15px;
            margin-bottom:20px;
            box-shadow:0 0 10px rgba(255,255,255,0.2);
            ">

            <h5 style="color:white;">
            {popular_df.iloc[i]['Book-Title']}
            </h5>

            <p style="color:#FFD700;">
            👤 {popular_df.iloc[i]['Book-Author']}
            </p>

            <p style="color:#00FFAA;">
            ⭐ Rating :
            {round(popular_df.iloc[i]['Avg-Rating'],2)}
            </p>

            <p style="color:#87CEFA;">
            📚 Votes :
            {popular_df.iloc[i]['Num-Ratings']}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================
# Project Statistics
# ============================================

st.write("")
st.markdown("---")

st.markdown(
    "<h2 style='text-align:center;color:#FFD700;'>📊 Project Statistics</h2>",
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "📚 Books",
        len(books.index)
    )

with c2:
    st.metric(
        "⭐ Popular Books",
        len(popular_df)
    )

with c3:
    st.metric(
        "🤖 Recommendations",
        "5 Books"
    )


# ============================================
# Footer
# ============================================

st.write("")
st.markdown("---")

st.markdown("""
<div class="footer">

<h3 style="color:white;">
❤️ Developed by <span style="color:#FFD700;">
Swati Chaturvedi
</span>
</h3>

<p>
BCA (IBM) Student | AI & Data Analytics Enthusiast
</p>

<p>
📚 AI Book Recommendation System | Streamlit Project
</p>

</div>
""", unsafe_allow_html=True)