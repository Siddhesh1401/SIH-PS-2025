import streamlit as st
import pandas as pd
import json
import os
import requests
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="SIH Problem Statements Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        color: #A23B72;
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F4F4F4;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #2E86AB;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #2E86AB;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1a5f7a;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 2px solid #e0e0e0;
    }
    .stSelectbox>div>div>select {
        border-radius: 5px;
        border: 2px solid #e0e0e0;
    }
    .problem-title {
        color: #2E86AB;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .problem-meta {
        color: #666;
        font-size: 0.9em;
        margin-bottom: 0.5rem;
    }
    .sidebar-header {
        color: #2E86AB;
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        # For Streamlit Cloud, prioritize GitHub URLs over local files
        data_sources = [
            # GitHub raw URLs (prioritize these for Streamlit Cloud)
            "https://raw.githubusercontent.com/Siddhesh1401/SIH-PS-2025/main/sih_ps_all.json",
            "https://raw.githubusercontent.com/Siddhesh1401/SIH-PS-2025/master/sih_ps_all.json",
            # Local file (fallback for local development)
            Path("sih_ps_all.json"),
        ]

        for i, source in enumerate(data_sources):
            try:
                st.info(f"🔄 Trying to load data from source {i+1}...")

                if isinstance(source, Path):
                    # Local file
                    if source.exists():
                        with open(source, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        st.success(f"✅ Loaded data from local file ({len(data)} problems)")
                        return pd.DataFrame(data)
                else:
                    # URL - try to load from GitHub
                    import requests
                    response = requests.get(source, timeout=15)
                    st.write(f"URL: {source}")
                    st.write(f"Status Code: {response.status_code}")

                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ Loaded data from GitHub ({len(data)} problems)")
                        return pd.DataFrame(data)
                    else:
                        st.warning(f"❌ HTTP {response.status_code} from {source}")

            except Exception as e:
                st.error(f"❌ Failed to load from source {i+1}: {str(e)}")
                continue

        # If all sources fail, show sample data
        st.error("❌ Could not load data from any source. Using sample data.")
        sample_data = [
            {
                "title": "Smart Community Health Monitoring System",
                "category": "Healthcare",
                "organization": "Ministry of Health",
                "description": "Develop a system for monitoring community health using IoT sensors and AI analytics for early disease detection and prevention.",
                "ps_id": "25001"
            },
            {
                "title": "AI-Powered Crop Disease Detection",
                "category": "Agriculture",
                "organization": "Ministry of Agriculture",
                "description": "Create an AI system to detect crop diseases using image recognition and provide treatment recommendations to farmers.",
                "ps_id": "25002"
            },
            {
                "title": "Smart Traffic Management System",
                "category": "Transportation",
                "organization": "Ministry of Road Transport",
                "description": "Implement an intelligent traffic management system using computer vision and machine learning to reduce congestion.",
                "ps_id": "25003"
            }
        ]
        return pd.DataFrame(sample_data)
    except Exception as e:
        st.error(f"❌ Critical error in data loading: {str(e)}")
        return pd.DataFrame()

# Main app
def main():
    st.markdown('<div class="main-header">🚀 SIH 2025 Problem Statements Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Browse, Search, Filter & Shortlist for Smart India Hackathon</div>', unsafe_allow_html=True)

    # Load data
    df = load_data()

    if df.empty:
        st.error("❌ No data available. The application is currently showing sample data.")
        st.info("💡 **To use real SIH data:**")
        st.code("""
# Run locally to generate data:
python sih_scraper.py

# Then upload the sih_ps_output/ folder to your hosting platform
# or use a cloud storage solution like AWS S3, Google Cloud Storage
        """)
        return

    # Show data info
    if len(df) <= 5:
        st.info(f"📊 Currently showing {len(df)} sample problem statements. Upload real data to see all 135+ problems.")
    else:
        st.success(f"📊 Loaded {len(df)} problem statements successfully!")

    # Sidebar
    st.sidebar.markdown('<div class="sidebar-header">🔍 Navigation</div>', unsafe_allow_html=True)
    page = st.sidebar.radio("", ["📋 Browse", "🔍 Search", "⭐ Shortlist", "📊 Analytics"], label_visibility="collapsed")

    if page == "Browse":
        show_browse_page(df)
    elif page == "Search":
        show_search_page(df)
    elif page == "Shortlist":
        show_shortlist_page(df)
    elif page == "Analytics":
        show_analytics_page(df)

def show_browse_page(df):
    st.header("📋 Browse Problem Statements")

    # Filters in sidebar
    with st.sidebar:
        st.markdown("### 🔍 Filters")
        categories = ["All"] + sorted(df['category'].unique().tolist()) if 'category' in df.columns else ["All"]
        selected_category = st.selectbox("Filter by Category", categories)

        organizations = ["All"] + sorted(df['organization'].unique().tolist()) if 'organization' in df.columns else ["All"]
        selected_org = st.selectbox("Filter by Organization", organizations)

        # Add theme filter if available
        if 'theme' in df.columns:
            themes = ["All"] + sorted(df['theme'].unique().tolist())
            selected_theme = st.selectbox("Filter by Theme", themes)
        else:
            selected_theme = "All"

    # Filter data
    filtered_df = df.copy()
    if selected_category != "All" and 'category' in df.columns:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    if selected_org != "All" and 'organization' in df.columns:
        filtered_df = filtered_df[filtered_df['organization'] == selected_org]
    if selected_theme != "All" and 'theme' in df.columns:
        filtered_df = filtered_df[filtered_df['theme'] == selected_theme]

    # Results count
    st.write(f"**{len(filtered_df)}** problem statements match your filters.")

    # Pagination
    items_per_page = 10
    total_pages = max(1, (len(filtered_df) // items_per_page) + 1)

    if total_pages > 1:
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
    else:
        page = 1

    # Display problems
    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_df = filtered_df.iloc[start:end]

    for idx, row in page_df.iterrows():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            # Header with ID and title
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                ps_id = row.get('ps_id', f'#{idx+1}')
                st.markdown(f"**ID:** {ps_id}")
            with col2:
                st.markdown(f'<div class="problem-title">{row.get("title", f"Problem {idx+1}")}</div>', unsafe_allow_html=True)
            with col3:
                if st.button("⭐ Shortlist", key=f"shortlist_{idx}"):
                    st.success("Added to shortlist!")

            # Meta information
            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown(f"**🏢 Organization:** {row.get('organization', 'N/A')}")
                st.markdown(f"**📂 Category:** {row.get('category', 'N/A')}")
                if 'theme' in row and row['theme']:
                    st.markdown(f"**🎯 Theme:** {row['theme']}")
                if 'department' in row and row['department']:
                    st.markdown(f"**🏛️ Department:** {row['department']}")

            with col_right:
                if 'youtube_link' in row and row['youtube_link']:
                    st.markdown(f"**📺 YouTube:** [Link]({row['youtube_link']})")
                if 'dataset_link' in row and row['dataset_link']:
                    st.markdown(f"**📊 Dataset:** [Link]({row['dataset_link']})")
                if 'contact_info' in row and row['contact_info']:
                    st.markdown(f"**📞 Contact:** {row['contact_info']}")

            # Description in expander
            with st.expander("📝 View Full Description"):
                st.write(row.get('description', 'No description available'))
                if 'background' in row and row['background']:
                    st.markdown("**🔍 Background:**")
                    st.write(row['background'])
                if 'expected_solution' in row and row['expected_solution']:
                    st.markdown("**💡 Expected Solution:**")
                    st.write(row['expected_solution'])

            st.markdown('</div>', unsafe_allow_html=True)

def show_search_page(df):
    st.header("🔍 Search Problem Statements")

    # Search input with better styling
    search_term = st.text_input("Enter search term", placeholder="Search in titles, descriptions, categories...")

    if search_term:
        # Search in relevant columns
        search_cols = ['title', 'description', 'category', 'organization']
        if 'theme' in df.columns:
            search_cols.append('theme')

        mask = pd.Series(False, index=df.index)

        for col in search_cols:
            if col in df.columns:
                mask = mask | df[col].astype(str).str.lower().str.contains(search_term.lower(), na=False)

        results = df[mask]

        if len(results) > 0:
            st.success(f"Found {len(results)} matching problem statements")

            # Show top results with pagination
            items_per_page = 10
            total_pages = max(1, (len(results) // items_per_page) + 1)

            if total_pages > 1:
                page = st.slider("Page", 1, total_pages, 1, key="search_page")
                start = (page - 1) * items_per_page
                end = start + items_per_page
                page_results = results.iloc[start:end]
                st.write(f"Showing results {start+1}-{min(end, len(results))} of {len(results)}")
            else:
                page_results = results

            # Display results in cards
            for idx, row in page_results.iterrows():
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f'<div class="problem-title">{row.get("title", f"Problem {idx+1}")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="problem-meta">🏢 {row.get("organization", "N/A")} • 📂 {row.get("category", "N/A")}</div>', unsafe_allow_html=True)
                    with col2:
                        if st.button("⭐ Shortlist", key=f"search_shortlist_{idx}"):
                            if 'shortlist' not in st.session_state:
                                st.session_state.shortlist = []
                            if idx not in st.session_state.shortlist:
                                st.session_state.shortlist.append(idx)
                                st.success("Added to shortlist!")

                    # Description preview
                    if 'description' in row:
                        desc_preview = row['description'][:200] + "..." if len(str(row['description'])) > 200 else str(row['description'])
                        st.write(desc_preview)

                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No problem statements found matching your search term.")
            st.info("💡 Try using different keywords or check your spelling.")
    else:
        st.info("🔍 Enter a search term above to find relevant problem statements")
        st.markdown("**Search Tips:**")
        st.markdown("- Search in titles, descriptions, categories, and organizations")
        st.markdown("- Use partial words or phrases")
        st.markdown("- Search is case-insensitive")

def show_shortlist_page(df):
    st.header("⭐ My Shortlist")

    # Initialize shortlist in session state if not exists
    if 'shortlist' not in st.session_state:
        st.session_state.shortlist = []

    shortlist_ids = st.session_state.shortlist

    if shortlist_ids:
        # Filter dataframe to show only shortlisted items
        shortlist_df = df[df.index.isin(shortlist_ids)] if len(shortlist_ids) > 0 else pd.DataFrame()

        if not shortlist_df.empty:
            st.success(f"You have {len(shortlist_df)} items in your shortlist")

            # Display shortlist as a nice table
            display_df = shortlist_df[['title', 'category', 'organization']].copy()
            display_df.index = range(1, len(display_df) + 1)
            st.dataframe(display_df, use_container_width=True)

            # Export options
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Save Shortlist"):
                    # Save to JSON file
                    shortlist_data = shortlist_df.to_dict('records')
                    with open('shortlist.json', 'w', encoding='utf-8') as f:
                        json.dump(shortlist_data, f, indent=2, ensure_ascii=False)
                    st.success("Shortlist saved to shortlist.json!")

            with col2:
                if st.button("📄 Export as CSV"):
                    csv_data = shortlist_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name="sih_shortlist.csv",
                        mime="text/csv"
                    )

            with col3:
                if st.button("🗑️ Clear Shortlist"):
                    st.session_state.shortlist = []
                    st.rerun()

            # Detailed view of shortlisted items
            st.subheader("📋 Detailed View")
            for idx, row in shortlist_df.iterrows():
                with st.expander(f"🔹 {row.get('title', f'Problem {idx+1}')}"):
                    col_left, col_right = st.columns(2)
                    with col_left:
                        st.write(f"**🏢 Organization:** {row.get('organization', 'N/A')}")
                        st.write(f"**📂 Category:** {row.get('category', 'N/A')}")
                        if 'theme' in row and row['theme']:
                            st.write(f"**🎯 Theme:** {row['theme']}")
                    with col_right:
                        st.write("**📝 Description:**")
                        st.write(row.get('description', 'No description available')[:300] + "...")
        else:
            st.info("Your shortlist contains items that are no longer in the current dataset.")
    else:
        st.info("⭐ No items in your shortlist yet!")
        st.markdown("Go to the **Browse** tab to add problem statements to your shortlist.")

def show_analytics_page(df):
    st.header("📊 Analytics Dashboard")

    # Metrics cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Problems", len(df))
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        categories = len(df['category'].unique()) if 'category' in df.columns else 0
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Categories", categories)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        organizations = len(df['organization'].unique()) if 'organization' in df.columns else 0
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Organizations", organizations)
        st.markdown('</div>', unsafe_allow_html=True)

    # Category distribution
    if 'category' in df.columns:
        st.subheader("📈 Category Distribution")
        category_counts = df['category'].value_counts().head(15)
        st.bar_chart(category_counts)

        # Category breakdown table
        st.subheader("📋 Category Breakdown")
        category_df = df['category'].value_counts().reset_index()
        category_df.columns = ['Category', 'Count']
        st.dataframe(category_df, use_container_width=True)

    # Organization distribution
    if 'organization' in df.columns:
        st.subheader("🏢 Organization Distribution")
        org_counts = df['organization'].value_counts().head(15)
        st.bar_chart(org_counts)

    # Theme distribution (if available)
    if 'theme' in df.columns:
        st.subheader("🎯 Theme Distribution")
        theme_counts = df['theme'].value_counts().head(15)
        st.bar_chart(theme_counts)

if __name__ == "__main__":
    main()