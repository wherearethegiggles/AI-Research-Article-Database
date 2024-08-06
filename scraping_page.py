import streamlit as st
import pandas as pd
import arxivscraper.arxivscraper as ax

# Streamlit app
st.title("Research Paper Explorer")

# Date inputs for scraping
date_from = st.date_input("Scrape Date From", value=pd.to_datetime("2024-05-26"))
date_until = st.date_input("Scrape Date Until", value=pd.to_datetime("2024-05-28"))

# Scrape button
if st.button("Scrap"):
    with st.spinner("Scraping data..."):
        scraper = ax.Scraper(category='cs', date_from=date_from.strftime('%Y-%m-%d'), date_until=date_until.strftime('%Y-%m-%d'), t=10, filters={'categories': ['cs.AI'], 'abstract': ['language model']})
        output = scraper.scrape()
        cols = ('id', 'title', 'categories', 'abstract', 'created', 'updated', 'authors', 'url')
        df = pd.DataFrame(output, columns=cols)
        st.session_state['df'] = df
        st.success("Scraping complete! Please click 'Process' to continue.")

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

    import ast

    # Display filtered data
    st.write("### Filtered Papers")
    for index, row in filtered_df.iterrows():
        st.write(f"**Title:** {row['title']}")
        st.write(f"**ID:** {row['id']}")
        st.write(f"**created:** {row['created'].date()}")
        
        # Convert authors string representation of a list to a list
        authors = ast.literal_eval(row['authors'])
        st.write(f"**Authors:** {', '.join(authors)}")  # Join authors list without using eval()
        
        st.write(f"**Abstract:** {row['abstract']}")  # Corrected column name
        st.write(f"**Link:** {row['url']}")
        st.write("---")
