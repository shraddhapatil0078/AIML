import streamlit as st

from few_shots import FewShotPosts
from postgenerator import generate_post


def main():
    st.title("LinkedIn Post Generator")
    col1, col2, col3 = st.columns(3)
    obj = FewShotPosts()  # Create an instance
    tags = obj.get_tags()  # Call method on instance
    with col1:
        selected_tag = st.selectbox('Title', options=tags)
    with col2:
        selected_length = st.selectbox("Length", options=["Short", "Medium", "Long"])
    with col3:
        selected_lang = st.selectbox("langauge", options=["English"])

    if st.button("Generate"):
        post = generate_post(selected_length, selected_lang, selected_tag)
        st.write(post)

if __name__ == "__main__":
    main()