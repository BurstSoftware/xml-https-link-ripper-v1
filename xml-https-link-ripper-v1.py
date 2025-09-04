import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd

# Streamlit app title
st.title("XML URL Extractor")

# Text area for user to paste XML data
xml_input = st.text_area("Paste your XML dataset here:", height=200)

# Function to parse XML and extract URL
def parse_xml(xml_data):
    try:
        # Parse the XML string
        root = ET.fromstring(xml_data)
        # Find the <loc> tag
        for url in root.findall(".//loc"):
            return url.text
        return None
    except ET.ParseError:
        st.error("Invalid XML format. Please check your input.")
        return None

# Process the input when the user submits
if st.button("Extract URL"):
    if xml_input:
        extracted_url = parse_xml(xml_input)
        if extracted_url:
            # Create a DataFrame with the extracted URL and browse-categories page
            data = {
                "Page Type": ["Main URL", "Browse Categories"],
                "URL": [
                    f'<a href="{extracted_url}" target="_blank">{extracted_url}</a>',
                    f'<a href="{extracted_url}browse-categories/" target="_blank">{extracted_url}browse-categories/</a>'
                ]
            }
            df = pd.DataFrame(data)
            
            # Display the table with clickable links
            st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.warning("No URL found in the provided XML.")
    else:
        st.warning("Please paste an XML dataset to process.")

# Optional: Display raw XML input for reference
if xml_input:
    st.subheader("Raw XML Input")
    st.code(xml_input, language="xml")
