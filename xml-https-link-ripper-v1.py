import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd

# Streamlit app title
st.title("XML URL Extractor")

# Text area for user to paste XML data
xml_input = st.text_area("Paste your XML dataset here:", height=200)

# Function to parse XML and extract all URLs
def parse_xml(xml_data):
    try:
        # Parse the XML string
        root = ET.fromstring(xml_data)
        # Find all <loc> tags and extract their text
        urls = [url.text for url in root.findall(".//loc") if url.text]
        return urls
    except ET.ParseError:
        st.error("Invalid XML format. Please check your input.")
        return []

# Process the input when the user submits
if st.button("Extract URLs"):
    if xml_input:
        extracted_urls = parse_xml(xml_input)
        if extracted_urls:
            # Create a DataFrame with all extracted URLs
            data = {
                "Page URL": [f'<a href="{url}" target="_blank">{url}</a>' for url in extracted_urls]
            }
            df = pd.DataFrame(data)
            
            # Display the table with clickable links
            st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.warning("No URLs found in the provided XML.")
    else:
        st.warning("Please paste an XML dataset to process.")

# Optional: Display raw XML input for reference
if xml_input:
    st.subheader("Raw XML Input")
    st.code(xml_input, language="xml")
