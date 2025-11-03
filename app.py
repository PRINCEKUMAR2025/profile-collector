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
    "India", "Agra", "Ahmedabad", "Amritsar", "Aurangabad", "Bangalore", "Bhubaneswar", "Chandigarh", "Chennai",
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
        st.subheader("🛠️ Skills Configuration")
        st.markdown("**Configure skill-based filtering with priority system**")
        
        # Skills section with two columns
        skills_col1, skills_col2 = st.columns(2)
        
        with skills_col1:
            st.markdown("**🎯 Must Have Skills**")
            st.markdown("*Priority 1: Candidates must have these skills*")
            
            # Predefined must-have skills
            must_have_skills_predefined = [
                "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift",
                "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask", "Spring", "Laravel", "Rails",
                "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "GitLab CI", "GitHub Actions",
                "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Kafka", "RabbitMQ", "Apache Spark", "Hadoop",
                "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter",
                "Data Science", "Data Analysis", "Statistics", "R", "SAS", "SPSS", "Tableau", "Power BI", "Looker", "Grafana",
                "DevOps", "CI/CD", "Microservices", "REST API", "GraphQL", "gRPC", "WebSocket", "OAuth", "JWT", "OAuth2",
                "Agile", "Scrum", "Kanban", "JIRA", "Confluence", "Slack", "Microsoft Teams", "Zoom", "Notion", "Asana",
                "Project Management", "Product Management", "Business Analysis", "Requirements Gathering", "Stakeholder Management", "Risk Management",
                "Sales", "Marketing", "Digital Marketing", "SEO", "SEM", "Content Marketing", "Social Media Marketing", "Email Marketing", "Analytics", "Growth Hacking",
                "UI/UX Design", "Figma", "Sketch", "Adobe XD", "InVision", "Prototyping", "Wireframing", "User Research", "A/B Testing", "Design Systems"
            ]
            
            must_have_skills_selected = st.multiselect(
                "Select Must-Have Skills",
                must_have_skills_predefined,
                key="must_have_skills_select",
                help="Choose skills that candidates MUST have"
            )
            
            must_have_skills_custom = st.text_input(
                "Add Custom Must-Have Skills",
                placeholder="e.g., Blockchain, AI, Cloud Computing (comma-separated)",
                key="must_have_skills_custom",
                help="Add custom must-have skills separated by commas"
            )
            
            # Combine predefined and custom must-have skills
            must_have_skills = must_have_skills_selected.copy()
            if must_have_skills_custom and must_have_skills_custom.strip():
                custom_skills = [s.strip() for s in must_have_skills_custom.split(",") if s.strip()]
                must_have_skills.extend(custom_skills)
        
        with skills_col2:
            st.markdown("**🔗 With Skills**")
            st.markdown("*Priority 2: Bonus if candidates also have these skills*")
            
            # Predefined with-skills
            with_skills_predefined = [
                "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift",
                "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask", "Spring", "Laravel", "Rails",
                "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "GitLab CI", "GitHub Actions",
                "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Kafka", "RabbitMQ", "Apache Spark", "Hadoop",
                "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter",
                "Data Science", "Data Analysis", "Statistics", "R", "SAS", "SPSS", "Tableau", "Power BI", "Looker", "Grafana",
                "DevOps", "CI/CD", "Microservices", "REST API", "GraphQL", "gRPC", "WebSocket", "OAuth", "JWT", "OAuth2",
                "Agile", "Scrum", "Kanban", "JIRA", "Confluence", "Slack", "Microsoft Teams", "Zoom", "Notion", "Asana",
                "Project Management", "Product Management", "Business Analysis", "Requirements Gathering", "Stakeholder Management", "Risk Management",
                "Sales", "Marketing", "Digital Marketing", "SEO", "SEM", "Content Marketing", "Social Media Marketing", "Email Marketing", "Analytics", "Growth Hacking",
                "UI/UX Design", "Figma", "Sketch", "Adobe XD", "InVision", "Prototyping", "Wireframing", "User Research", "A/B Testing", "Design Systems"
            ]
            
            with_skills_selected = st.multiselect(
                "Select With-Skills",
                with_skills_predefined,
                key="with_skills_select",
                help="Choose skills that are nice to have"
            )
            
            with_skills_custom = st.text_input(
                "Add Custom With-Skills",
                placeholder="e.g., Blockchain, AI, Cloud Computing (comma-separated)",
                key="with_skills_custom",
                help="Add custom with-skills separated by commas"
            )
            
            # Combine predefined and custom with-skills
            with_skills = with_skills_selected.copy()
            if with_skills_custom and with_skills_custom.strip():
                custom_skills = [s.strip() for s in with_skills_custom.split(",") if s.strip()]
                with_skills.extend(custom_skills)
    
    # Skills combination display
    if must_have_skills or with_skills:
        st.markdown("---")
        st.subheader("🎯 Skills Search Strategy")
        
        col_strategy1, col_strategy2 = st.columns(2)
        
        with col_strategy1:
            if must_have_skills:
                st.markdown("**Must Have Skills:**")
                for skill in must_have_skills:
                    st.markdown(f"• {skill}")
            else:
                st.markdown("**Must Have Skills:** None selected")
        
        with col_strategy2:
            if with_skills:
                st.markdown("**With Skills (Bonus):**")
                for skill in with_skills:
                    st.markdown(f"• {skill}")
            else:
                st.markdown("**With Skills (Bonus):** None selected")
        
        # Search strategy explanation
        if must_have_skills and with_skills:
            st.info("🔍 **Search Strategy**: Will find candidates who have ALL must-have skills, prioritizing those who also have with-skills.")
        elif must_have_skills:
            st.info("🔍 **Search Strategy**: Will find candidates who have ALL must-have skills.")
        elif with_skills:
            st.info("🔍 **Search Strategy**: Will find candidates who have any of the with-skills (less restrictive).")
    
    # Legacy skills field for backward compatibility
    skills = []  # Initialize empty for backward compatibility
    
    # Tier 1 Colleges Filter Section
    st.markdown("---")
    st.header("🎓 Tier 1 Colleges Filter (Premium Feature)")
    st.markdown("**Filter candidates from top institutions in India**")
    
    # Enable/Disable Tier 1 filter
    tier1_colleges_filter = st.checkbox(
        "🔒 Enable Tier 1 Colleges Filter (Only show candidates from listed colleges)",
        value=False,
        help="When enabled, ONLY candidates from selected Tier 1 colleges will be shown"
    )
    
    col_tier1, col_tier2 = st.columns(2)
    
    with col_tier1:
        st.markdown("**🏛️ Select Tier 1 Colleges**")
        
        # Comprehensive list of Tier 1 colleges in India
        tier1_colleges_predefined = [
            # IITs
            "Indian Institute of Technology Delhi", "Indian Institute of Technology Bombay", "Indian Institute of Technology Madras", "Indian Institute of Technology Kanpur", "Indian Institute of Technology Kharagpur",
"Indian Institute of Technology Roorkee", "Indian Institute of Technology Guwahati", "Indian Institute of Technology Hyderabad", "Indian Institute of Technology Indore", "Indian Institute of Technology (BHU) Varanasi",
"Indian Institute of Technology Ropar", "Indian Institute of Technology Patna", "Indian Institute of Technology Gandhinagar", "Indian Institute of Technology Jodhpur", "Indian Institute of Technology Bhubaneswar",
"Indian Institute of Technology Mandi", "Indian Institute of Technology Tirupati", "Indian Institute of Technology Palakkad", "Indian Institute of Technology Jammu", "Indian Institute of Technology Dharwad",
"Indian Institute of Technology Goa", "Indian Institute of Technology Bhilai", "Indian Institute of Technology",

            
            # NITs
            "National Institute of Technology Tiruchirappalli", "National Institute of Technology Surathkal", "National Institute of Technology Warangal", "National Institute of Technology Calicut", "National Institute of Technology Rourkela",
"National Institute of Technology Karnataka", "National Institute of Technology Durgapur", "National Institute of Technology Jamshedpur", "National Institute of Technology Kurukshetra", "National Institute of Technology Allahabad",
"National Institute of Technology Bhopal", "National Institute of Technology Nagpur", "National Institute of Technology Silchar", "National Institute of Technology Hamirpur", "National Institute of Technology Jalandhar",
"National Institute of Technology Raipur", "National Institute of Technology Agartala", "National Institute of Technology Patna", "National Institute of Technology Meghalaya", "National Institute of Technology Manipur",
"National Institute of Technology",

            
            # IIMs
            "IIM Ahmedabad", "IIM Bangalore", "IIM Calcutta", "IIM Lucknow", "IIM Kozhikode",
            "IIM Indore", "IIM Shillong", "IIM Rohtak", "IIM Ranchi", "IIM Raipur",
            "IIM Trichy", "IIM Udaipur", "IIM Kashipur", "IIM Nagpur", "IIM Visakhapatnam",
            "IIM Amritsar", "IIM Bodh Gaya", "IIM Sambalpur", "IIM Sirmaur", "IIM Jammu",
            "Indian Institute of Management",
            
            # BITS
            "BITS Pilani", "BITS Goa", "BITS Hyderabad", "BIRLA Institute",
            
            # IISc and IISERs
            "IISc Bangalore", "Indian Institute of Science",
            "IISER Pune", "IISER Kolkata", "IISER Mohali", "IISER Bhopal", "IISER Thiruvananthapuram",
            
            # Top State Universities
            "Delhi University", "DU", "St. Stephen's College", "Hindu College", "SRCC",
            "Shri Ram College of Commerce", "Lady Shri Ram College", "Miranda House",
            "Delhi Technological University", "DTU", "NSIT", "Netaji Subhas",
            "Jadavpur University", "Presidency University", "Anna University",
            
            # Top Private Universities
            "VIT Vellore", "Vellore Institute of Technology", "IIIT Hyderabad", "IIIT Bangalore",
            "IIIT Delhi", "Manipal Institute of Technology", "Thapar University",
            "PEC Chandigarh", "Punjab Engineering College", "ICT Mumbai",
            "VJTI Mumbai", "Veermata Jijabai", "College of Engineering Pune", "COEP",
            
            # ISB and Management Schools
            "ISB Hyderabad", "Indian School of Business", "XLRI Jamshedpur",
            "FMS Delhi", "JBIMS Mumbai", "MDI Gurgaon", "SP Jain",
            
            # Medical Colleges
            "AIIMS Delhi", "AIIMS", "All India Institute of Medical Sciences",
            "CMC Vellore", "Christian Medical College", "JIPMER",
            
            # Law Schools
            "NLSIU Bangalore", "NALSAR Hyderabad", "NLU Delhi", "NUJS Kolkata"
        ]
        
        tier1_colleges_selected = st.multiselect(
            "Select Tier 1 Colleges",
            tier1_colleges_predefined,
            default=[],
            key="tier1_colleges_select",
            help="Select colleges to filter candidates from these institutions"
        )
    
    with col_tier2:
        st.markdown("**✏️ Add Custom Colleges**")
        st.caption("Add colleges not in the predefined list")
        
        tier1_colleges_custom = st.text_area(
            "Add Custom Tier 1 Colleges",
            placeholder="e.g., IIT Hyderabad, NIT Trichy, BITS Pilani (one per line or comma-separated)",
            key="tier1_colleges_custom",
            help="Add custom college names separated by commas or new lines",
            height=150
        )
        
        # Combine predefined and custom tier 1 colleges
        tier1_colleges = tier1_colleges_selected.copy()
        if tier1_colleges_custom and tier1_colleges_custom.strip():
            # Split by both comma and newline
            custom_colleges = []
            for line in tier1_colleges_custom.split('\n'):
                custom_colleges.extend([c.strip() for c in line.split(',') if c.strip()])
            tier1_colleges.extend(custom_colleges)
    
    # Display selected Tier 1 colleges
    if tier1_colleges:
        st.markdown("---")
        st.subheader("🎯 Selected Tier 1 Colleges")
        
        if tier1_colleges_filter:
            st.success(f"🔒 **Filter ENABLED**: Only showing candidates from {len(tier1_colleges)} selected colleges")
        else:
            st.info(f"ℹ️ **Filter DISABLED**: Will prioritize candidates from {len(tier1_colleges)} colleges (bonus points)")
        
        # Display in columns
        num_cols = 3
        cols = st.columns(num_cols)
        for i, college in enumerate(tier1_colleges):
            with cols[i % num_cols]:
                if tier1_colleges_filter:
                    st.markdown(f"🔒 {college}")
                else:
                    st.markdown(f"⭐ {college}")
        
        # Explanation
        st.caption("💡 **Tip**: Enable the filter checkbox above to ONLY show candidates from these colleges. If disabled, these colleges give bonus relevance points.")
    
    # Search Quality Indicator (moved here after all variables are defined)
    st.markdown("---")
    col_quality1, col_quality2 = st.columns([2, 1])
    
    with col_quality1:
        # Calculate search specificity
        must_have_skills_count = len(must_have_skills) if 'must_have_skills' in locals() else 0
        with_skills_count = len(with_skills) if 'with_skills' in locals() else 0
        total_filters = len(job_roles) + len(locations) + len(companies) + len(experience_levels) + len(education_levels) + len(company_sizes) + len(industries) + must_have_skills_count + with_skills_count
        
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
        - **Must-Have Skills**: 2-5 core skills that are absolutely required
        - **With-Skills**: 3-8 additional skills that are nice to have
        
        **Skills Strategy:**
        - **Must-Have Skills**: Use for essential requirements (e.g., "Python", "React")
        - **With-Skills**: Use for bonus qualifications (e.g., "Machine Learning", "AWS")
        - **Combination**: Must-have "Python" with "Statistics" for data science roles
        
        **Avoid:**
        - Too many filters (may return no results)
        - Very specific company names (use partial names)
        - Overly broad locations (use specific cities)
        - Too many must-have skills (keep it to 2-5 maximum)
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
                "must_have_skills": must_have_skills if 'must_have_skills' in locals() else [],
                "with_skills": with_skills if 'with_skills' in locals() else [],
                "tier1_colleges": tier1_colleges if 'tier1_colleges' in locals() else [],
                "tier1_colleges_filter": tier1_colleges_filter if 'tier1_colleges_filter' in locals() else False,
                "skills": [],  # Legacy field for backward compatibility
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
                    
                    # Show available output files
                    st.markdown("### 📁 Available Files for Download")
                    
                    # Check for output files
                    if os.path.exists(csv_filename):
                        file_size = os.path.getsize(csv_filename)
                        st.info(f"📊 **CSV File Found:** {csv_filename} ({file_size:,} bytes)")
                        with open(csv_filename, "rb") as f:
                            st.download_button(
                                f"📥 Download CSV ({csv_filename})",
                                f.read(),
                                file_name=csv_filename,
                                mime="text/csv",
                                key="download_csv"
                            )
                    else:
                        st.warning(f"⚠️ CSV file not found: {csv_filename}")
                    
                    # Check for JSON output
                    json_filename = csv_filename.replace('.csv', '.json')
                    if os.path.exists(json_filename):
                        file_size = os.path.getsize(json_filename)
                        st.info(f"📄 **JSON File Found:** {json_filename} ({file_size:,} bytes)")
                        with open(json_filename, "rb") as f:
                            st.download_button(
                                f"📥 Download JSON ({json_filename})",
                                f.read(),
                                file_name=json_filename,
                                mime="application/json",
                                key="download_json"
                            )
                    
                    # Check for Excel output
                    excel_filename = csv_filename.replace('.csv', '.xlsx')
                    if os.path.exists(excel_filename):
                        file_size = os.path.getsize(excel_filename)
                        st.info(f"📈 **Excel File Found:** {excel_filename} ({file_size:,} bytes)")
                        with open(excel_filename, "rb") as f:
                            st.download_button(
                                f"📥 Download Excel ({excel_filename})",
                                f.read(),
                                file_name=excel_filename,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="download_excel"
                            )
                else:
                    st.error(f"❌ Scraping failed with error: {result.stderr}")
                    
                    # Show helpful troubleshooting tips
                    st.markdown("### 🔧 Troubleshooting Tips:")
                    st.markdown("""
                    **Common issues and solutions:**
                    
                    1. **Login Required:** Make sure you're logged into LinkedIn in the browser that opens
                    2. **Network Issues:** Check your internet connection
                    3. **LinkedIn Changes:** LinkedIn may have updated their interface - try again later
                    4. **Rate Limiting:** Wait a few minutes before trying again
                    5. **Browser Issues:** Close and restart the Streamlit app if the browser doesn't open
                    
                    **Check the logs below for detailed error information.**
                    """)
                    
            except Exception as e:
                st.error(f"❌ Error executing scraper: {str(e)}")
    
    # Display existing files section
    st.markdown("---")
    st.markdown("### 📁 Previously Created Files")
    
    # Find all CSV, JSON, and Excel files in the directory
    import glob
    
    csv_files = glob.glob("*.csv")
    json_files = glob.glob("*.json")
    excel_files = glob.glob("*.xlsx")
    
    if csv_files or json_files or excel_files:
        st.info("📂 **Files available for download:**")
        
        # Display CSV files
        for csv_file in csv_files:
            try:
                file_size = os.path.getsize(csv_file)
                st.info(f"📊 **CSV:** {csv_file} ({file_size:,} bytes)")
                with open(csv_file, "rb") as f:
                    st.download_button(
                        f"📥 Download {csv_file}",
                        f.read(),
                        file_name=csv_file,
                        mime="text/csv",
                        key=f"existing_csv_{csv_file}"
                    )
            except Exception as e:
                st.error(f"Error reading {csv_file}: {e}")
        
        # Display JSON files
        for json_file in json_files:
            try:
                file_size = os.path.getsize(json_file)
                st.info(f"📄 **JSON:** {json_file} ({file_size:,} bytes)")
                with open(json_file, "rb") as f:
                    st.download_button(
                        f"📥 Download {json_file}",
                        f.read(),
                        file_name=json_file,
                        mime="application/json",
                        key=f"existing_json_{json_file}"
                    )
            except Exception as e:
                st.error(f"Error reading {json_file}: {e}")
        
        # Display Excel files
        for excel_file in excel_files:
            try:
                file_size = os.path.getsize(excel_file)
                st.info(f"📈 **Excel:** {excel_file} ({file_size:,} bytes)")
                with open(excel_file, "rb") as f:
                    st.download_button(
                        f"📥 Download {excel_file}",
                        f.read(),
                        file_name=excel_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"existing_excel_{excel_file}"
                    )
            except Exception as e:
                st.error(f"Error reading {excel_file}: {e}")
    else:
        st.info("📭 No output files found. Run the scraper to generate CSV, JSON, or Excel files.")
    
    # Display logs
    st.markdown("---")
    st.header("📋 Scraper Logs")
    show_logs()

if __name__ == "__main__":
    main()