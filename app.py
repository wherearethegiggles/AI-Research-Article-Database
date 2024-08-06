import streamlit as st
import pandas as pd
import arxivscraper.arxivscraper as ax

# Streamlit app
st.title("Research Paper Explorer")

# Check if the data has been scraped before
if 'df' not in st.session_state:
    # Date inputs for scraping
    date_from = st.date_input("Scrape Date From", value=pd.to_datetime("2024-05-26"))
    date_until = st.date_input("Scrape Date Until", value=pd.to_datetime("2024-05-28"))

    # Category selection
    categories = st.multiselect("Select Categories", options=['cs.AI', 'cs.LG', 'cs.CV', 'cs.CL'], default=['cs.AI'])
    
    # Filter inputs
    filters = st.text_input("Enter Filters (comma separated)", value="LLM,language model,Chatbot")
    filter_list = [f.strip() for f in filters.split(",")]

    # Scrape button
    if st.button("Scrape"):
        with st.spinner("Scraping data..."):
            scraper = ax.Scraper(category='cs', date_from=date_from.strftime('%Y-%m-%d'), date_until=date_until.strftime('%Y-%m-%d'), t=10, filters={'categories': categories, 'abstract': filter_list})
            output = scraper.scrape()
            cols = ('id', 'title', 'categories', 'abstract', 'created', 'updated', 'authors', 'url')
            df = pd.DataFrame(output, columns=cols)
            st.session_state['df'] = df
            st.success("Scraping complete! Please click 'Process' to continue.")

# Check if the DataFrame exists in session state
if 'df' in st.session_state:
    df = st.session_state['df']

    # Process button
    if 'processed' not in st.session_state:
        if st.button("Process"):
            st.session_state['processed'] = True
            st.success("Processing complete!")

    if 'processed' in st.session_state:
        # Display date filters
        start_date = st.date_input("Filter Start Date", value=pd.to_datetime("2020-01-01"))
        end_date = st.date_input("Filter End Date", value=pd.to_datetime("2024-12-31"))

        # Filter by dates
        df['created'] = pd.to_datetime(df['created'])
        df['updated'] = pd.to_datetime(df['updated'])
        filtered_df = df[(df['created'] >= pd.to_datetime(start_date)) & (df['created'] <= pd.to_datetime(end_date))]

        # Filter by keywords in Title
        title_filter = st.text_input("Keywords in Title:", value="")

        if title_filter:
            filtered_df = filtered_df[filtered_df['title'].str.contains(title_filter, case=False, na=False)]

        # Get unique categories
        unique_categories = set()
        for categories in filtered_df['categories']:
            unique_categories.update(categories.split())

        # Display categories dropdown
        selected_categories = st.multiselect("Select Categories", sorted(unique_categories))

        # Filter by categories
        if selected_categories:
            filtered_df = filtered_df[filtered_df['categories'].apply(lambda x: any(category in x.split() for category in selected_categories))]

        # Export filtered data to CSV
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name='filtered_data.csv',
            mime='text/csv'
        )

        # Display filtered data
        st.write("### Filtered Papers")
        for index, row in filtered_df.iterrows():
            title = row['title']
            st.write(f"**Title:** {title}")
            st.write(f"**ID:** {row['id']}")
            st.write(f"**Updated:** {row['updated'].date()}")
            st.write(f"**Abstract:** {row['abstract']}")
            st.write(f"**Link:** {row['url']}")
            st.write("---")
