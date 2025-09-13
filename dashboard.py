import streamlit as st
import pandas as pd
import json
from pathlib import Path
import os

# Load data
DATA_FILE = Path("sih_ps_output/sih_ps_all.json")
SHORTLIST_FILE = Path("shortlist.json")

@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        st.error("Data file not found. Please run the scraper first.")
        return pd.DataFrame()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def save_shortlist(shortlist):
    with open(SHORTLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(shortlist, f, indent=2)

def load_shortlist():
    if SHORTLIST_FILE.exists():
        with open(SHORTLIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def main():
    port = int(os.environ.get("PORT", 8501))
    st.set_page_config(page_title="SIH Dashboard", layout="wide", page_icon="📊")
    # For deployment, set server options
    st.set_option('server.port', port)
    st.set_option('server.headless', True)
    st.set_option('server.runOnSave', False)
    
    # Custom CSS for professional look
    st.markdown("""
    <style>
    .main-header {text-align: center; color: #2E86AB; font-size: 2.5em; font-weight: bold;}
    .sub-header {color: #A23B72; font-size: 1.5em;}
    .card {background-color: #F4F4F4; padding: 10px; border-radius: 10px; margin: 10px 0;}
    .stButton>button {background-color: #2E86AB; color: white; border-radius: 5px;}
    .stTextInput>div>div>input {border-radius: 5px;}
    .stSelectbox>div>div>select {border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">SIH 2025 Problem Statements Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Browse, Search, Filter & Shortlist for Smart India Hackathon</div>', unsafe_allow_html=True)

    df = load_data()
    if df.empty:
        return

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Browse", "⭐ Shortlist", "📈 Analytics"])

    with tab1:
        st.header("Browse Problem Statements")
        
        # Sidebar for filters
        with st.sidebar:
            st.header("🔍 Filters")
            search_term = st.text_input("Search (title/description)", "")
            categories = sorted(df['category'].dropna().unique())
            selected_category = st.selectbox("Category", ["All"] + categories)
            organizations = sorted(df['organization'].dropna().unique())
            selected_org = st.selectbox("Organization", ["All"] + organizations)
            themes = sorted(df['theme'].dropna().unique())
            selected_theme = st.selectbox("Theme", ["All"] + themes)
            if st.button("Reset Filters"):
                st.rerun()

        # Apply filters
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df['title'].str.contains(search_term, case=False, na=False) | 
                                      filtered_df['description'].str.contains(search_term, case=False, na=False)]
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        if selected_org != "All":
            filtered_df = filtered_df[filtered_df['organization'] == selected_org]
        if selected_theme != "All":
            filtered_df = filtered_df[filtered_df['theme'] == selected_theme]

        st.write(f"**{len(filtered_df)}** problem statements match your filters.")

        # Pagination
        items_per_page = 10
        total_pages = max(1, (len(filtered_df) // items_per_page) + 1)
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_page:
            page = st.slider("Page", 1, total_pages, st.session_state.get('current_page', 1), key="page_slider")
            st.session_state['current_page'] = page
            st.write(f"Page {page} of {total_pages}")
        with col_prev:
            if st.button("⬅️ Previous", disabled=(page == 1)):
                st.session_state['current_page'] = page - 1
                st.rerun()
        with col_next:
            if st.button("Next ➡️", disabled=(page == total_pages)):
                st.session_state['current_page'] = page + 1
                st.rerun()

        start = (page - 1) * items_per_page
        end = start + items_per_page
        page_df = filtered_df.iloc[start:end]

        # Display
        shortlist_ids = st.session_state.get('shortlist', [])
        for _, row in page_df.iterrows():
            with st.container():
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 4, 1])
                col1.markdown(f"**ID:** {row['ps_id']}")
                col2.markdown(f"**{row['title']}**")
                if col3.checkbox("Add to Shortlist", key=f"short_{row['ps_id']}", value=row['ps_id'] in shortlist_ids):
                    if row['ps_id'] not in shortlist_ids:
                        shortlist_ids.append(row['ps_id'])
                else:
                    if row['ps_id'] in shortlist_ids:
                        shortlist_ids.remove(row['ps_id'])
                st.session_state['shortlist'] = shortlist_ids
                
                with st.expander("View Full Details"):
                    col_left, col_right = st.columns(2)
                    with col_left:
                        st.markdown(f"**🏢 Organization:** {row['organization'] or 'N/A'}")
                        st.markdown(f"**📂 Category:** {row['category'] or 'N/A'}")
                        st.markdown(f"**🎯 Theme:** {row['theme'] or 'N/A'}")
                        if row['department']:
                            st.markdown(f"**🏛️ Department:** {row['department']}")
                        if row['youtube_link']:
                            st.markdown(f"**📺 YouTube:** [Link]({row['youtube_link']})")
                        if row['dataset_link']:
                            st.markdown(f"**📊 Dataset:** [Link]({row['dataset_link']})")
                        if row['contact_info']:
                            st.markdown(f"**📞 Contact:** {row['contact_info']}")
                    with col_right:
                        st.markdown("**📝 Description:**")
                        st.write(row['description'] or 'N/A')
                        if row['background']:
                            st.markdown("**🔍 Background:**")
                            st.write(row['background'])
                        if row['expected_solution']:
                            st.markdown("**💡 Expected Solution:**")
                            st.write(row['expected_solution'])
                st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.header("Your Shortlist")
        shortlist_data = load_shortlist()
        if shortlist_data:
            shortlist_df = pd.DataFrame(shortlist_data)
            st.dataframe(shortlist_df[['ps_id', 'title', 'organization', 'category']])
            col1, col2 = st.columns(2)
            if col1.button("Save Shortlist"):
                save_shortlist(shortlist_data)
                st.success("Shortlist saved!")
            if col2.button("Export as CSV"):
                csv = shortlist_df.to_csv(index=False)
                st.download_button("Download CSV", csv, "shortlist.csv", "text/csv")
        else:
            st.info("No items in shortlist yet. Go to Browse tab to add some!")

    with tab3:
        st.header("Analytics")
        st.subheader("Category Distribution")
        cat_counts = df['category'].value_counts()
        st.bar_chart(cat_counts)
        st.subheader("Theme Distribution")
        theme_counts = df['theme'].value_counts()
        st.bar_chart(theme_counts)

if __name__ == "__main__":
    main()
