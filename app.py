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
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #1f77b4;
    }
    .problem-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        # For Streamlit Cloud - load from cloud storage
        # Replace this URL with your actual data file URL
        json_url = "https://raw.githubusercontent.com/Siddhesh1401/SIH-PS-2025/main/sih_ps_all.json"

        import requests
        response = requests.get(json_url)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        else:
            # Fallback to sample data
            st.warning("⚠️ Could not load full data from cloud. Showing sample data instead.")
            sample_data = [
                {
                    "title": "Smart Community Health Monitoring System",
                    "category": "Healthcare",
                    "organization": "Ministry of Health",
                    "description": "Develop a system for monitoring community health using IoT sensors and AI analytics."
                },
                {
                    "title": "AI-Powered Crop Disease Detection",
                    "category": "Agriculture",
                    "organization": "Ministry of Agriculture",
                    "description": "Create an AI system to detect crop diseases using image recognition and provide treatment recommendations."
                },
                {
                    "title": "Smart Traffic Management System",
                    "category": "Transportation",
                    "organization": "Ministry of Road Transport",
                    "description": "Implement an intelligent traffic management system using computer vision and machine learning."
                },
                {
                    "title": "Digital Learning Platform for Rural Areas",
                    "category": "Education",
                    "organization": "Ministry of Education",
                    "description": "Build an offline-first digital learning platform for students in rural areas with limited internet connectivity."
                },
                {
                    "title": "Waste Management Optimization",
                    "category": "Environment",
                    "organization": "Ministry of Environment",
                    "description": "Develop a smart waste segregation and management system using IoT sensors and data analytics."
                }
            ]
            return pd.DataFrame(sample_data)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Main app
def main():
    st.markdown('<h1 class="main-header">🚀 SIH Problem Statements Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Smart India Hackathon 2025 - Problem Statement Explorer")

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
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to", ["Browse", "Search", "Shortlist", "Analytics"])

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

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        categories = ["All"] + sorted(df['category'].unique().tolist()) if 'category' in df.columns else ["All"]
        selected_category = st.selectbox("Filter by Category", categories)

    with col2:
        organizations = ["All"] + sorted(df['organization'].unique().tolist()) if 'organization' in df.columns else ["All"]
        selected_org = st.selectbox("Filter by Organization", organizations)

    # Filter data
    filtered_df = df.copy()
    if selected_category != "All" and 'category' in df.columns:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    if selected_org != "All" and 'organization' in df.columns:
        filtered_df = filtered_df[filtered_df['organization'] == selected_org]

    # Display results
    st.write(f"Showing {len(filtered_df)} problem statements")

    for idx, row in filtered_df.iterrows():
        with st.expander(f"🔹 {row.get('title', f'Problem {idx+1}')}"):
            st.write(f"**Category:** {row.get('category', 'N/A')}")
            st.write(f"**Organization:** {row.get('organization', 'N/A')}")
            if 'description' in row:
                st.write(f"**Description:** {row['description'][:200]}...")
            if st.button(f"Add to Shortlist #{idx+1}", key=f"shortlist_{idx}"):
                st.success("Added to shortlist!")

def show_search_page(df):
    st.header("🔍 Search Problem Statements")

    search_term = st.text_input("Enter search term", placeholder="Search in titles, descriptions...")

    if search_term:
        # Search in relevant columns
        search_cols = ['title', 'description', 'category', 'organization']
        mask = pd.Series(False, index=df.index)

        for col in search_cols:
            if col in df.columns:
                mask = mask | df[col].astype(str).str.lower().str.contains(search_term.lower())

        results = df[mask]

        st.write(f"Found {len(results)} matching problem statements")

        for idx, row in results.head(10).iterrows():
            with st.expander(f"🔹 {row.get('title', f'Problem {idx+1}')}"):
                st.write(f"**Category:** {row.get('category', 'N/A')}")
                st.write(f"**Organization:** {row.get('organization', 'N/A')}")
                if 'description' in row:
                    st.write(f"**Description:** {row['description'][:300]}...")
    else:
        st.info("Enter a search term to find relevant problem statements")

def show_shortlist_page(df):
    st.header("⭐ My Shortlist")
    st.info("Shortlist functionality will be implemented here")

def show_analytics_page(df):
    st.header("📊 Analytics Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Problems", len(df))

    with col2:
        categories = len(df['category'].unique()) if 'category' in df.columns else 0
        st.metric("Categories", categories)

    with col3:
        organizations = len(df['organization'].unique()) if 'organization' in df.columns else 0
        st.metric("Organizations", organizations)

    # Category distribution
    if 'category' in df.columns:
        st.subheader("📈 Category Distribution")
        category_counts = df['category'].value_counts().head(10)
        st.bar_chart(category_counts)

if __name__ == "__main__":
    main()