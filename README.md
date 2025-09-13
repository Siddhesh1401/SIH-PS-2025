# SIH Problem Statements Dashboard

A comprehensive web application for browsing, searching, and filtering Smart India Hackathon (SIH) problem statements. This project scrapes SIH problem statements and provides an interactive dashboard for easy exploration and shortlisting.

## 🚀 Features

### 📊 Interactive Dashboard
- **Browse**: View all problem statements in a paginated table
- **Search**: Real-time search across titles, descriptions, and categories
- **Filter**: Filter by category, organization, and other criteria
- **Shortlist**: Save favorite problem statements for later reference
- **Analytics**: View statistics and insights about the problem statements

### 🔍 Advanced Search & Filtering
- Text search across all fields
- Category-based filtering
- Organization-based filtering
- Pagination for better performance
- Sortable columns

### 📱 Responsive Design
- Mobile-friendly interface
- Professional UI with modern styling
- Dark/light theme support
- Expandable details for each problem statement

### 📈 Analytics Dashboard
- Total problem statements count
- Category distribution
- Organization statistics
- Search trends and insights

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas
- **Web Scraping**: BeautifulSoup4, Requests
- **Deployment**: Vercel
- **Version Control**: Git

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🚀 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Siddhesh1401/SIH-PS-2025.git
   cd SIH-PS-2025
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the scraper (optional - data already included)**
   ```bash
   python sih_scraper.py
   ```

5. **Run the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

6. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
SIH-PS-2025/
├── dashboard.py              # Main Streamlit application
├── sih_scraper.py           # Web scraper for SIH problem statements
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel deployment configuration
├── Procfile                # Heroku deployment configuration
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
└── sih_ps_output/          # Scraped data directory
    ├── sih_ps_all.json     # All problem statements (JSON)
    ├── sih_ps_all.csv      # All problem statements (CSV)
    └── *.md                # Individual problem statement files
```

## 🎯 Usage

### For Participants
1. **Browse Problem Statements**: Use the main dashboard to explore all available problems
2. **Search**: Use the search bar to find specific topics or technologies
3. **Filter**: Apply filters to narrow down by category or organization
4. **Shortlist**: Save interesting problems to your shortlist for later review
5. **View Details**: Click on any problem statement to see full details

### For Organizers
- View comprehensive analytics about problem statement distribution
- Monitor search trends and popular categories
- Export data for further analysis

## 🌐 Deployment

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Vercel will automatically detect Streamlit and deploy
3. Your app will be live at `https://your-app.vercel.app`

### Local Deployment
Follow the installation steps above for local development.

## 📊 Data Source

Problem statements are scraped from the official Smart India Hackathon website. The scraper collects:
- Problem statement titles
- Detailed descriptions
- Categories and domains
- Organization information
- Submission guidelines
- Contact information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Smart India Hackathon for providing the platform
- All participating organizations for their problem statements
- Open source community for the amazing tools

## 📞 Support

If you have any questions or need help:
- Open an issue on GitHub
- Contact the maintainers
- Check the documentation

---

**Made with ❤️ for Smart India Hackathon 2025**