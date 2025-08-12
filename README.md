# 🔍 LinkedIn Profile URL Scraper - Advanced Edition

A powerful LinkedIn profile scraper with advanced search filters, capsule-style inputs, and multiple export formats. Built with Streamlit and Playwright for optimal performance and user experience.

## ✨ Features

### 🎯 Advanced Search Filters
- **Job Roles**: 60+ predefined roles with custom input support
- **Locations**: 100+ global cities and regions
- **Companies**: 150+ major companies across industries
- **Experience Levels**: Entry Level to C-Level filtering
- **Education**: High School to PhD filtering
- **Company Size**: Startup to Enterprise classification
- **Industry**: Technology, Healthcare, Finance, and more
- **Skills**: Custom skill-based filtering

### 🎨 User Interface
- **Capsule-style Inputs**: Easy selection and removal of multiple values
- **Responsive Design**: Wide layout with sidebar configuration
- **Real-time Logs**: Live scraping progress monitoring
- **Search Preview**: Metrics and results overview
- **Configuration Panel**: Advanced settings and export options

### 📊 Export Options
- **CSV Format**: Standard comma-separated values
- **JSON Format**: Structured data with metadata
- **Excel Format**: Spreadsheet with formatting (requires openpyxl)
- **Multiple Files**: Simultaneous export in all formats

### 🔧 Advanced Configuration
- **Custom Delays**: Configurable timing between actions
- **Page Limits**: Up to 100 pages for premium accounts
- **Profile Data**: Optional detailed profile extraction
- **Connection Filters**: Filter by connection degree and count
- **Anti-Detection**: Random delays and human-like behavior

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- LinkedIn Premium account (recommended for advanced features)
- Modern web browser

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Linkedin-Profile-URL-Scrapper
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install
   ```

4. **Verify installation**
   ```bash
   python -c "import streamlit, playwright, pandas; print('All dependencies installed successfully!')"
   ```

## 🎮 Usage

### 1. Launch the Application
```bash
streamlit run app.py
```

### 2. Configure Search Parameters

#### Basic Settings (Sidebar)
- **Pages to Scrape**: 1-100 (premium accounts)
- **Output Filename**: Custom CSV filename
- **Delays**: Min/Max timing between actions
- **Scroll Pause**: Time to wait after scrolling

#### Export Options
- **Include Profile Data**: Extract detailed information
- **Export Format**: CSV, JSON, Excel, or All
- **Advanced Filters**: Enable LinkedIn's built-in filters
- **Connection Degree**: Include connection information

### 3. Set Search Filters

#### Job Roles
- Select from 60+ predefined roles
- Add custom job titles
- Combine multiple roles for broader search

#### Locations
- Choose from 100+ global cities
- Add custom locations
- Search multiple regions simultaneously

#### Companies
- Select from 150+ major companies
- Add custom company names
- Filter by current/previous employers

#### Additional Filters
- **Experience Level**: Entry to C-Level
- **Education**: High School to PhD
- **Company Size**: Startup to Enterprise
- **Industry**: Technology, Healthcare, Finance, etc.
- **Skills**: Comma-separated skill list

### 4. Start Scraping
1. Click "🚀 Start Advanced Scraping"
2. Browser will open automatically
3. **Manually log in to LinkedIn** (security feature)
4. Scraping begins automatically after login verification
5. Monitor progress in real-time logs

### 5. Download Results
- **CSV File**: Standard spreadsheet format
- **JSON File**: Structured data with metadata
- **Excel File**: Formatted spreadsheet (if openpyxl installed)

## 🔒 Security Features

- **Manual Login**: No credential storage in code
- **Session Management**: Secure browser context
- **No Password Logging**: Credentials never logged
- **Premium Account Support**: Enhanced search capabilities

## 📁 Output Formats

### CSV Format
```csv
linkedin_profile,name,headline,location,company,connection_degree
https://linkedin.com/in/johndoe,John Doe,Software Engineer,San Francisco,Google,2nd
```

### JSON Format
```json
{
  "profiles": [
    {
      "linkedin_profile": "https://linkedin.com/in/johndoe",
      "name": "John Doe",
      "headline": "Software Engineer",
      "location": "San Francisco",
      "company": "Google"
    }
  ]
}
```

### Excel Format
- Multiple sheets for different data types
- Formatted headers and data
- Professional presentation ready

## ⚙️ Configuration Options

### Advanced Settings
- **Delay Range**: 1-10 seconds between actions
- **Scroll Pause**: 1-5 seconds after scrolling
- **Page Limits**: 1-100 pages (premium accounts)
- **Filter Application**: Enable/disable LinkedIn filters

### Search Optimization
- **Keyword Combination**: Smart search term building
- **Location Filtering**: Geographic targeting
- **Company Targeting**: Employer-based filtering
- **Experience Matching**: Level-appropriate results

## 🚨 Important Notes

### LinkedIn Premium Benefits
- **Higher Page Limits**: Up to 100 pages vs 50 for free
- **Advanced Filters**: More granular search options
- **Better Results**: Higher quality candidate matches
- **Reduced Restrictions**: Fewer rate limiting issues

### Best Practices
1. **Use Specific Filters**: Avoid overly broad searches
2. **Limit Page Count**: Start with 10-20 pages
3. **Respect Rate Limits**: Use recommended delays
4. **Monitor Logs**: Check for errors or warnings
5. **Test Small**: Verify with small searches first

### Limitations
- **Manual Login Required**: Security feature, not a bug
- **LinkedIn Changes**: UI updates may require selector updates
- **Rate Limiting**: Respect LinkedIn's terms of service
- **Premium Features**: Some filters require premium accounts

## 🐛 Troubleshooting

### Common Issues

#### Login Problems
- Ensure LinkedIn credentials are correct
- Check for 2FA requirements
- Verify account isn't locked

#### No Results Found
- Check search filter combinations
- Verify location spellings
- Reduce filter restrictions

#### Export Errors
- Install openpyxl for Excel export
- Check file permissions
- Verify sufficient disk space

#### Scraping Stops
- Check browser for LinkedIn prompts
- Verify internet connection
- Monitor log files for errors

### Debug Information
- **Log Files**: Check `scraper.log` for detailed information
- **Screenshots**: Login errors saved as `login_error.png`
- **Console Output**: Real-time progress in terminal
- **Streamlit Logs**: Web interface log display

## 🔄 Updates and Maintenance

### Regular Maintenance
- Update Playwright browsers: `playwright install`
- Check LinkedIn UI changes
- Update selector patterns if needed
- Monitor for new anti-bot measures

### Version Compatibility
- **Python**: 3.7+ (3.8+ recommended)
- **Playwright**: Latest stable version
- **Streamlit**: 1.20+ for new features
- **Pandas**: 1.3+ for data processing

## 📞 Support

### Getting Help
1. Check the troubleshooting section
2. Review log files for errors
3. Verify all dependencies are installed
4. Test with minimal search parameters

### Contributing
- Report bugs with detailed logs
- Suggest new filter options
- Improve selector patterns
- Add new export formats

## 📄 License

This project is for educational and legitimate business use only. Users must comply with LinkedIn's Terms of Service and applicable laws.

## ⚠️ Disclaimer

This tool is designed for legitimate recruitment and business development purposes. Users are responsible for:
- Complying with LinkedIn's Terms of Service
- Respecting rate limits and usage guidelines
- Obtaining proper consent for data collection
- Following applicable privacy laws and regulations

---

**Happy Scraping! 🚀** 
