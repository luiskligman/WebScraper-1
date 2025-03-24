import streamlit as st
# Selenium allows us to automate a web browser so we can actually navigate to a webpage
# we can grab all of the content that's on that page then we could do some filtering on it
# which we can then pass on to a LLM (such as ChatGPT)

from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content

from parse import parse_with_ollama

st.title("AI Web Scraper")
url = st.text_input("Enter a website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the website")
    result = scrape_website(url)

    print(result)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

# dom stands for Document Object Model
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)

