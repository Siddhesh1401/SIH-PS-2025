import streamlit as st
import pandas as pd
import json
from pathlib import Path

# Load data
DATA_FILE = Path("sih_ps_output/sih_ps_all.json")
SHORTLIST_FILE = Path("shortlist.json")

@st.cache_data
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def save_shortlist(shortlist):
    with open(SHORTLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(shortlist, f, indent=2)

def main():
    st.title("SIH Problem Statements Dashboard")

    df = load_data()

    # Search
    search_term = st.text_input("Search by title or description", "")
    if search_term:
        df = df[df['title'].str.contains(search_term, case=False, na=False) | 
                df['description'].str.contains(search_term, case=False, na=False)]

    # Filters
    categories = df['category'].dropna().unique()
    selected_category = st.selectbox("Filter by Category", ["All"] + list(categories))
    if selected_category != "All":
        df = df[df['category'] == selected_category]

    organizations = df['organization'].dropna().unique()
    selected_org = st.selectbox("Filter by Organization", ["All"] + list(organizations))
    if selected_org != "All":
        df = df[df['organization'] == selected_org]

    themes = df['theme'].dropna().unique()
    selected_theme = st.selectbox("Filter by Theme", ["All"] + list(themes))
    if selected_theme != "All":
        df = df[df['theme'] == selected_theme]

    # Display
    st.write(f"Showing {len(df)} problem statements")
    st.dataframe(df[['ps_id', 'title', 'organization', 'category', 'theme', 'description']].head(50))

    # Shortlist
    selected_ids = st.multiselect("Select PS IDs to shortlist", df['ps_id'].tolist())
    if st.button("Save Shortlist"):
        shortlist_data = df[df['ps_id'].isin(selected_ids)].to_dict('records')
        save_shortlist(shortlist_data)
        st.success(f"Saved {len(shortlist_data)} items to shortlist.json")

if __name__ == "__main__":
    main()
    