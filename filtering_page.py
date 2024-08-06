import streamlit as st
import pandas as pd

# Streamlit app
st.title("Research Paper Explorer - Filtering")

# Check if the DataFrame exists in session state
if 'df' in st.session_state:
    df = st.session_state['df']

    # Display date filters
    start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2024-12-31"))

    # Filter by dates
    df['created'] = pd.to_datetime(df['created'])
    df['updated'] = pd.to_datetime(df['updated'])
    filtered_df = df[(df['created'] >= pd.to_datetime(start_date)) & (df['created'] <= pd.to_datetime(end_date))]

    # Get unique categories
    unique_categories = set()
    for categories in filtered_df['categories']:
        unique_categories.update(categories.split())

    # Display categories dropdown
    selected_categories = st.multiselect("Select Categories", sorted(unique_categories))

    # Filter by categories
    if selected_categories:
        filtered_df = filtered_df[filtered_df['categories'].apply(lambda x: any(category in x.split() for category in selected_categories))]

    # Display filtered data
    st.write("### Filtered Papers")
    for index, row in filtered_df.iterrows():
        st.write(f"**Title:** {row['title']}")
        st.write(f"**ID:** {row['id']}")
        st.write(f"**created:** {row['created'].date()}")
        st.write(f"**Authors:** {', '.join(eval(row['authors']))}")
        st.write(f"**summary:** {row['summary']}")
        st.write(f"**Link:** {row['url']}")
        st.write("---")

