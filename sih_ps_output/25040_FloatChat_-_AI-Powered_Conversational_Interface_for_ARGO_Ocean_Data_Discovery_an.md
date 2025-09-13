# FloatChat - AI-Powered Conversational Interface for ARGO Ocean Data Discovery and Visualization

**Problem Statement ID:** 25040

**Organization:** Ministry of Earth Sciences (MoES)

**Department:** Indian National Centre for Ocean Information Services (INCOIS)

**Category:** Software

**Theme:** Miscellaneous

## Description

Background Oceanographic data is vast, complex, and heterogeneous – ranging from satellite observations to in-situ measurements like CTD casts, Argo floats, and BGC sensors. The Argo program, which deploys autonomous profiling floats across the world’s oceans, generates an extensive dataset in NetCDF format containing temperature, salinity, and other essential ocean variables. Accessing, querying, and visualizing this data requires domain knowledge, technical skills, and familiarity with complex formats and tools. With the rise of AI and Large Language Models (LLMs), especially when combined with modern structured databases and interactive dashboards, it is now feasible to create intuitive, accessible systems that democratize access to ocean data. Description The current problem statement proposes the development of an AI-powered conversational system for ARGO float data that enables users to query, explore, and visualize oceanographic information using natural language. The current system shall: − Ingest ARGO NetCDF files and convert them into structured formats (like SQL/Parquet). − Use a vector database (like FAISS/Chroma) to store metadata and summaries for retrieval. − Leverage Retrieval-Augmented Generation (RAG) pipelines powered by multimodal LLMs (such as GPT, QWEN, LLaMA, or Mistral) to interpret user queries and map them to database queries (SQL). (Use Model Context Protocol (MCP)) − Enable interactive dashboards (via Streamlit or Dash) for visualization of ARGO profiles, such as mapped trajectories, depth-time plots, and profile comparisons, etc. − Provide a chatbot-style interface where users can ask questions like: • Show me salinity profiles near the equator in March 2023 • Compare BGC parameters in the Arabian Sea for the last 6 months • What are the nearest ARGO floats to this location? This tool will bridge the gap between domain experts, decision-makers, and raw data by allowing non-technical users to extract meaningful insights effortlessly.

## Background

Oceanographic data is vast, complex, and heterogeneous – ranging from satellite observations to in-situ measurements like CTD casts, Argo floats, and BGC sensors. The Argo program, which deploys autonomous profiling floats across the world’s oceans, generates an extensive dataset in NetCDF format containing temperature, salinity, and other essential ocean variables. Accessing, querying, and visualizing this data requires domain knowledge, technical skills, and familiarity with complex formats and tools. With the rise of AI and Large Language Models (LLMs), especially when combined with modern structured databases and interactive dashboards, it is now feasible to create intuitive, accessible systems that democratize access to ocean data.

## Expected Solution / Outcomes

− End-to-end pipeline to process ARGO NetCDF data and store it in a relational (PostgreSQL) and vector database (FAISS/Chroma). − Backend LLM system that translates natural language into database queries and generates responses using RAG. − Frontend dashboard with geospatial visualizations (using Plotly, Leaflet, or Cesium) and tabular summaries to ASCII, NetCDF. − Chat interface that understands user intent and guides them through data discovery. − Demonstrate a working Proof-of-Concept (PoC) with Indian Ocean ARGO data and future extensibility to in-situ observations (BGC, glider, buoys, etc.), and satellite datasets. Acronyms NetCDF: Network Common Data Format CTD: Conductivity Temperature and Depth BGC: Bio-Geo-Chemical Floats

