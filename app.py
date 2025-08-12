import streamlit as st
import subprocess
import os
import json

# Predefined lists for search filters
JOB_ROLES = [
    "Software Engineer", "Senior Software Engineer", "Lead Software Engineer", "Principal Software Engineer",
    "Software Developer", "Full Stack Developer", "Frontend Developer", "Backend Developer", "DevOps Engineer",
    "Data Scientist", "Data Engineer", "Machine Learning Engineer", "AI Engineer", "Data Analyst",
    "Product Manager", "Product Owner", "Program Manager", "Project Manager", "Scrum Master",
    "UX Designer", "UI Designer", "Product Designer", "Graphic Designer", "Visual Designer",
    "Marketing Manager", "Digital Marketing Specialist", "Content Marketing", "SEO Specialist",
    "Sales Representative", "Account Executive", "Business Development", "Sales Manager",
    "HR Manager", "Recruiter", "Talent Acquisition", "HR Business Partner",
    "Finance Manager", "Financial Analyst", "Accountant", "Controller",
    "Operations Manager", "Business Analyst", "Strategy Manager", "Consultant",
    "Customer Success Manager", "Support Engineer", "Technical Support", "Customer Service",
    "QA Engineer", "Test Engineer", "Quality Assurance", "Test Lead",
    "System Administrator", "Network Engineer", "Security Engineer", "Cloud Engineer",
    "Mobile Developer", "iOS Developer", "Android Developer", "React Native Developer",
    "Python Developer", "Java Developer", "JavaScript Developer", "C# Developer",
    "Ruby Developer", "PHP Developer", "Go Developer", "Rust Developer"
]

LOCATIONS = [
    "Agra", "Ahmedabad", "Amritsar", "Aurangabad", "Bangalore", "Bhubaneswar", "Chandigarh", "Chennai",
    "Coimbatore", "Dehradun", "Delhi", "Gurgaon", "Guwahati", "Hyderabad", "Indore", "Jaipur",
    "Jabalpur", "Jodhpur", "Kanpur", "Kochi", "Kolkata", "Lucknow", "Madurai", "Meerut",
    "Mohali", "Mumbai", "Mysore", "Nagpur", "Noida", "Patna", "Pune", "Raipur",
    "Ranchi", "Salem", "Surat", "Thiruvananthapuram", "Udaipur", "Vadodara", "Varanasi", "Visakhapatnam"
]


COMPANIES = [
    "Google", "Microsoft", "Apple", "Amazon", "Meta", "Netflix", "Uber", "Airbnb", "Twitter", "LinkedIn",
    "Salesforce", "Oracle", "IBM", "Intel", "Cisco", "Adobe", "VMware", "NVIDIA", "AMD", "Qualcomm",
    "Palantir", "Snowflake", "Databricks", "MongoDB", "Elastic", "Confluent", "HashiCorp", "GitLab", "GitHub", "Atlassian",
    "Slack", "Zoom", "Dropbox", "Box", "Spotify", "Pinterest", "Snap Inc", "TikTok", "ByteDance", "Tencent",
    "Alibaba", "Baidu", "JD.com", "Meituan", "DiDi", "Grab", "GoJek", "Rappi", "Nubank", "MercadoLibre",
    "Shopify", "Stripe", "Square", "PayPal", "Coinbase", "Robinhood", "Chime", "Affirm", "Klarna", "Afterpay",
    "DoorDash", "Instacart", "Grubhub", "Postmates", "Lyft", "Bolt", "Gett", "Cabify", "99", "Careem",
    "Tesla", "Rivian", "Lucid Motors", "Nio", "XPeng", "Li Auto", "BYD", "Rivian", "Nikola", "Canoo",
    "SpaceX", "Blue Origin", "Virgin Galactic", "Rocket Lab", "Planet Labs", "Maxar", "BlackSky", "Capella Space",
    "OpenAI", "Anthropic", "Cohere", "Hugging Face", "Stability AI", "Midjourney", "Runway", "Replicate", "Scale AI", "Labelbox",
    "Databricks", "Snowflake", "Fivetran", "dbt", "Airbyte", "Prefect", "Dagster", "Apache Airflow", "Kubernetes", "Docker",
    "HashiCorp", "Pulumi", "Terraform", "Ansible", "Chef", "Puppet", "Jenkins", "GitLab CI", "GitHub Actions", "CircleCI",
    "Stripe", "Plaid", "Finicity", "MX", "Yodlee", "TrueLayer", "Tink", "Nordigen", "Salt Edge", "Bud",
    "Shopify", "WooCommerce", "Magento", "BigCommerce", "Squarespace", "Wix", "Webflow", "Framer", "Bubble", "Glide",
    "Notion", "Airtable", "Coda", "Roam Research", "Obsidian", "Logseq", "RemNote", "Tana", "Fibery", "ClickUp",
    "Figma", "Sketch", "Adobe XD", "InVision", "Marvel", "Principle", "Framer", "Protopie", "Axure", "Balsamiq",
    "Slack", "Microsoft Teams", "Discord", "Telegram", "Signal", "WhatsApp", "WeChat", "Line", "Viber", "Threema",
    "Zoom", "Google Meet", "Microsoft Teams", "Skype", "Webex", "BlueJeans", "GoToMeeting", "Join.me", "Whereby", "Loom",
    "Spotify", "Apple Music", "Amazon Music", "YouTube Music", "Tidal", "Deezer", "Pandora", "SoundCloud", "Bandcamp", "Audiomack",
    "Netflix", "Disney+", "Hulu", "Amazon Prime Video", "HBO Max", "Peacock", "Paramount+", "Apple TV+", "Discovery+", "Crunchyroll"
]

def create_capsule_input(label, options, key, placeholder="Select or type...", help_text=""):
    """Create a capsule-style input for multiple values"""
    st.subheader(label)
    
    # Text input for custom values
    custom_input = st.text_input(
        f"Add custom {label.lower()}",
        key=f"custom_{key}",
        placeholder=f"Type custom {label.lower()} and press Enter",
        help=help_text
    )
    
    # Multi-select for predefined options
    selected_options = st.multiselect(
        f"Select from common {label.lower()}s",
        options,
        key=f"select_{key}",
        help=f"Choose from popular {label.lower()}s or add custom ones above"
    )
    
    # Display selected values as capsules
    all_values = selected_options.copy()
    
    # Add custom input if provided
    if custom_input and custom_input.strip():
        all_values.append(custom_input.strip())
    
    # Display capsules
    if all_values:
        st.write("**Selected values:**")
        cols = st.columns(4)
        for i, value in enumerate(all_values):
            col_idx = i % 4
            with cols[col_idx]:
                if st.button(f"❌ {value}", key=f"remove_{key}_{i}"):
                    all_values.remove(value)
                    st.rerun()
    
    return all_values

def show_logs():
    if os.path.exists("scraper.log"):
        with open("scraper.log", encoding='utf-8') as f:
            st.text(f.read())
    else:
        st.warning("No log file found.")

def main():
    st.set_page_config(
        page_title="LinkedIn Advanced Scraper", 
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 LinkedIn Profile URL Scraper - Advanced")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Basic settings
        st.subheader("Basic Settings")
        pages = st.slider("Number of pages to scrape", 1, 100, 10, help="Maximum 100 pages for premium accounts")
        csv_filename = st.text_input("CSV filename", "candidates.csv", help="Output CSV filename")
        
        # Advanced settings
        st.subheader("Advanced Settings")
        delay_min = st.slider("Min delay between actions (seconds)", 1, 5, 2)
        delay_max = st.slider("Max delay between actions (seconds)", 3, 10, 5)
        scroll_pause = st.slider("Scroll pause (seconds)", 1, 5, 2)
        
        # Export options
        st.subheader("Export Options")
        include_profile_data = st.checkbox("Include profile data", value=False, help="Extract additional profile information")
        export_format = st.selectbox("Export format", ["CSV", "JSON", "Excel"])
        
        # Filter settings
        st.subheader("Filter Settings")
        use_advanced_filters = st.checkbox("Use advanced LinkedIn filters", value=True)
        include_connections = st.checkbox("Include connection degree", value=False)
        min_connections = st.number_input("Minimum connections", min_value=0, value=0, help="Filter by minimum connection count")
        
        # Debug options
        st.subheader("Debug Options")
        debug_mode = st.checkbox("Enable debug mode", value=False, help="Take screenshots and provide detailed logging")
        test_search = st.checkbox("Test search first", value=True, help="Test search before full scraping")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🔐 LinkedIn Credentials")
        email = st.text_input("LinkedIn Email", key="email")
        password = st.text_input("LinkedIn Password", type="password", key="password")
        
        if st.button("🔑 Test Connection", type="primary"):
            if email and password:
                st.success("Credentials entered. Connection will be tested during scraping.")
            else:
                st.error("Please enter both email and password.")
    
    with col2:
        st.header("📊 Search Results Preview")
        if 'search_results' in st.session_state:
            st.metric("Total Profiles Found", len(st.session_state.search_results))
            st.metric("Pages Scraped", st.session_state.get('pages_scraped', 0))
        else:
            st.info("No search results yet. Start a search to see metrics.")
    
    # Search filters section
    st.markdown("---")
    st.header("🎯 Search Filters")
    
    # Job Roles
    job_roles = create_capsule_input(
        "Job Roles", 
        JOB_ROLES, 
        "job_roles",
        help_text="Add multiple job roles to search for. You can combine different levels and specializations."
    )
    
    # Locations
    locations = create_capsule_input(
        "Locations", 
        LOCATIONS, 
        "locations",
        help_text="Add multiple locations to search in. You can search globally or focus on specific regions."
    )
    
    # Companies
    companies = create_capsule_input(
        "Companies", 
        COMPANIES, 
        "companies",
        help_text="Add companies to filter candidates who work or worked at these organizations."
    )
    
    # Additional filters
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.subheader("💼 Experience Level")
        experience_levels = st.multiselect(
            "Experience Level",
            ["Entry Level", "Associate", "Mid-Level", "Senior", "Lead", "Principal", "Director", "VP", "C-Level"],
            default=["Mid-Level", "Senior"],
            help="Select experience levels to filter candidates"
        )
    
    with col4:
        st.subheader("🎓 Education")
        education_levels = st.multiselect(
            "Education Level",
            ["High School", "Associate's", "Bachelor's", "Master's", "PhD", "MBA", "Other"],
            default=["Bachelor's", "Master's"],
            help="Filter by education level"
        )
    
    with col5:
        st.subheader("🏢 Company Size")
        company_sizes = st.multiselect(
            "Company Size",
            ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10001+", "Startup", "Enterprise"],
            default=["Startup", "Enterprise"],
            help="Filter by company size"
        )
    
    # Industry and skills
    col6, col7 = st.columns(2)
    
    with col6:
        st.subheader("🏭 Industry")
        industries = st.multiselect(
            "Industry",
            ["Technology", "Healthcare", "Finance", "Education", "Manufacturing", "Retail", "Consulting", "Media", "Real Estate", "Transportation"],
            help="Filter by industry"
        )
    
    with col7:
        st.subheader("🛠️ Skills")
        skills = st.text_input(
            "Required Skills",
            placeholder="e.g., Python, React, AWS (comma-separated)",
            help="Enter skills separated by commas"
        )
    
    # Search Quality Indicator (moved here after all variables are defined)
    st.markdown("---")
    col_quality1, col_quality2 = st.columns([2, 1])
    
    with col_quality1:
        # Calculate search specificity
        skills_count = len([s.strip() for s in skills.split(',')]) if skills and skills.strip() else 0
        total_filters = len(job_roles) + len(locations) + len(companies) + len(experience_levels) + len(education_levels) + len(company_sizes) + len(industries) + skills_count
        
        if total_filters == 0:
            search_quality = "❌ No filters selected"
            quality_color = "red"
            quality_message = "Add filters to get targeted results"
        elif total_filters <= 3:
            search_quality = "🟡 Basic targeting"
            quality_color = "orange"
            quality_message = "Good start! Add more filters for better results"
        elif total_filters <= 6:
            search_quality = "🟢 Well targeted"
            quality_color = "green"
            quality_message = "Excellent targeting! This should give quality results"
        else:
            search_quality = "🔴 Overly specific"
            quality_color = "red"
            quality_message = "Too many filters may return no results"
    
    with col_quality2:
        st.metric("Search Quality", search_quality)
        st.caption(quality_message)
    
    # Search Optimization Tips
    with st.expander("💡 Search Optimization Tips"):
        st.markdown("""
        **For Best Results:**
        - **Job Roles**: 1-3 specific roles (e.g., "AI Engineer", "Machine Learning Engineer")
        - **Locations**: 1-2 cities or regions
        - **Companies**: 1-2 target companies
        - **Experience**: 2-3 levels (e.g., "Mid-Level", "Senior")
        - **Industry**: 1-2 industries maximum
        
        **Avoid:**
        - Too many filters (may return no results)
        - Very specific company names (use partial names)
        - Overly broad locations (use specific cities)
        """)
    
    # Search button and execution
    st.markdown("---")
    
    if st.button("🚀 Start Advanced Scraping", type="primary", use_container_width=True):
        if not (email and password):
            st.error("Please enter your LinkedIn credentials.")
        elif not (job_roles or locations):
            st.error("Please select at least one job role or location.")
        else:
            # Prepare search parameters
            search_params = {
                "email": email,
                "password": password,
                "job_roles": job_roles,
                "locations": locations,
                "companies": companies,
                "experience_levels": experience_levels,
                "education_levels": education_levels,
                "company_sizes": company_sizes,
                "industries": industries,
                "skills": [s.strip() for s in skills.split(",")] if skills else [],
                "pages": pages,
                "csv_filename": csv_filename,
                "delay_min": delay_min,
                "delay_max": delay_max,
                "scroll_pause": scroll_pause,
                "include_profile_data": include_profile_data,
                "export_format": export_format,
                "use_advanced_filters": use_advanced_filters,
                "include_connections": include_connections,
                "min_connections": min_connections,
                "debug_mode": debug_mode,
                "test_search": test_search
            }
            
            # Save parameters to file for scraper
            with open("search_params.json", "w") as f:
                json.dump(search_params, f)
            
            st.info("🚀 Starting advanced LinkedIn scraping...")
            st.info("A browser will open shortly. Please log in to LinkedIn manually.")
            st.info("Scraping will begin automatically after login verification.")
            
            # Execute scraper with all parameters
            try:
                result = subprocess.run(
                    ["python", "scraper.py"],
                    capture_output=True, text=True
                )
                
                if result.returncode == 0:
                    st.success("✅ Scraping completed successfully!")
                    
                    # Check for output files
                    if os.path.exists(csv_filename):
                        with open(csv_filename, "rb") as f:
                            st.download_button(
                                f"📥 Download {csv_filename}",
                                f,
                                file_name=csv_filename,
                                mime="text/csv"
                            )
                    
                    # Check for JSON output
                    json_filename = csv_filename.replace('.csv', '.json')
                    if os.path.exists(json_filename):
                        with open(json_filename, "rb") as f:
                            st.download_button(
                                f"📥 Download {json_filename}",
                                f,
                                file_name=json_filename,
                                mime="application/json"
                            )
                    
                    # Check for Excel output
                    excel_filename = csv_filename.replace('.csv', '.xlsx')
                    if os.path.exists(excel_filename):
                        with open(excel_filename, "rb") as f:
                            st.download_button(
                                f"📥 Download {excel_filename}",
                                f,
                                file_name=excel_filename,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                else:
                    st.error(f"❌ Scraping failed with error: {result.stderr}")
                    
            except Exception as e:
                st.error(f"❌ Error executing scraper: {str(e)}")
    
    # Display logs
    st.markdown("---")
    st.header("📋 Scraper Logs")
    show_logs()

if __name__ == "__main__":
    main()