import streamlit as st
import pandas as pd
from io import BytesIO

def separate_data_by_keywords(df, column_name, selected_keywords):
    keyword_containers = {keyword: [] for keyword in selected_keywords}
    for index, row in df.iterrows():
        text = row[column_name]
        for keyword in selected_keywords:
            if keyword.lower() in text.lower():
                keyword_containers[keyword].append(row)
    return keyword_containers

def main():
    st.title("Data Separation Based on Keywords")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        st.sidebar.title("Options")
        selected_column = st.sidebar.selectbox("Select the Column to Match with Keywords", df.columns)
        custom_keywords = st.sidebar.text_area("Enter Custom Keywords (comma-separated)")

        if custom_keywords:
            selected_keywords = [keyword.strip() for keyword in custom_keywords.split(",")]
        else:
            selected_keywords = []

        keyword_containers = separate_data_by_keywords(df, selected_column, selected_keywords)

        st.write("### Results:")
        for keyword, container in keyword_containers.items():
            st.write(f"Items with keyword '{keyword}':")
            keyword_df = pd.DataFrame(container)
            count = len(keyword_df)
            st.write(f"Count: {count}")
            st.write(keyword_df)
            st.write("---")

            # Generate and offer file download for each keyword
            if not keyword_df.empty:
                output_buffer = BytesIO()
                output_writer = pd.ExcelWriter(output_buffer, engine="openpyxl")
                keyword_df.to_excel(output_writer, index=False)
                output_writer.close()  # Close the writer before saving to the buffer
                output_buffer.seek(0)
                st.download_button(
                    label=f"Download {keyword} Data",
                    data=output_buffer,
                    file_name=f"{keyword}_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

if __name__ == "__main__":
    main()
