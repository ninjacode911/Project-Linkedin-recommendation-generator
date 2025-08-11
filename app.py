from openai import OpenAI, RateLimitError
import streamlit as st
import time
import os
# Add at the top of the file after imports:
# Add at the top of the file after imports:
from typing import Dict, Optional
# Page configuration
st.set_page_config(
    page_title="LinkedIn Recommendation Generator",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import LinkedIn-style font */
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
    
    /* Main container styling */
    .main-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f4f8 100%);
        min-height: 100vh;
    }
    
    /* Header styling */
    .header-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .linkedin-logo {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #0077B5 0%, #005885 100%);
        border-radius: 15px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,119,181,0.3);
    }
    
    .main-title {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #0077B5;
        margin: 0;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.2rem;
        color: #666;
        margin: 0;
        font-weight: 400;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #0077B5;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e8f4f8;
    }
    
    /* Sub-section headers styling */
    .sub-section-header {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #0077B5;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid rgba(0, 119, 181, 0.2);
    }
    
    /* Custom star rating styling */
    .star-rating {
        display: flex;
        gap: 8px;
        align-items: center;
        margin: 10px 0;
        padding: 15px;
        background: #f8f9ff;
        border-radius: 12px;
        border: 1px solid #e8f4f8;
    }
    
    .star-question {
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 500;
        color: #0077B5; /* Changed from white to blue for visibility */
        font-size: 1rem;
        flex: 1;
        margin-right: 20px;
    }
    
    /* Result container */
    .result-container {
        background: linear-gradient(135deg, #0077B5 0%, #005885 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,119,181,0.3);
        margin-top: 2rem;
    }
    
    .result-title {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .recommendation-text {
        background: rgba(255,255,255,0.15);
        padding: 2rem;
        border-radius: 15px;
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Style for the code block that appears on copy */
    .stCodeBlock {
        border-radius: 15px !important;
        border: 1px solid #e8f4f8 !important;
    }
    .stCodeBlock pre {
        min-height: 200px; /* Increase the default height */
        max-height: 400px;
        overflow-y: auto !important;
        white-space: pre-wrap !important; /* Allow text to wrap */
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0077B5 0%, #005885 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,119,181,0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,119,181,0.4);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: #f8f9ff;
        border: 1px solid #e8f4f8;
        border-radius: 12px;
        font-family: 'Source Sans Pro', sans-serif;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background: #f8f9ff;
        border: 1px solid #e8f4f8;
        border-radius: 12px;
        font-family: 'Source Sans Pro', sans-serif;
        padding: 12px 16px;
    }
    
    /* Progress bar */
    .progress-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom metric styling */
    .metric-container {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f4f8 100%);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
        border: 1px solid #e8f4f8;
    }
    
    /* Form field uniform sizing and styling */
    .stTextInput > div {
        width: 100% !important;
    }
    
    .stSelectbox > div {
        width: 100% !important;
    }
    
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #333 !important;
        min-height: 48px !important;
        border: 1px solid #e8f4f8 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stSelectbox > div > div {
        background-color: white !important;
        color: #333 !important;
        min-height: 48px !important;
        border: 1px solid #e8f4f8 !important;
        border-radius: 8px !important;
    }
    /* Add consistent spacing between star ratings */
    .star-rating-container {
        margin-bottom: 1rem;
    }
    /* Container for form fields */
    .form-field-container {
        padding: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def create_star_rating(label, key, help_text=None):
    """Create a custom 5-star rating component"""
    # Use a container to apply consistent bottom margin via CSS
    with st.container():
        st.markdown('<div class="star-rating-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown(f'<div class="star-question">{label}</div>', unsafe_allow_html=True)
            if help_text:
                st.caption(help_text)
        
        with col2:
            # The select_slider is inside the columns
            pass

        rating = st.select_slider(
            "",
            options=[1, 2, 3, 4, 5],
            value=3,
            key=key,
            label_visibility="collapsed"
        )
    
    # Create visual stars
    stars = "".join(["⭐" if i < rating else "☆" for i in range(5)])
    st.markdown(f"<div style='font-size: 1.5rem; text-align: center; margin-top: -35px;'>{stars}</div>", unsafe_allow_html=True)

    return rating

    """Generate recommendation using OpenRouter API with input summary"""
    
    # Organize ratings into categories for analysis
    performance_areas = {
        "Technical Competence": {
            "Domain Knowledge": ratings['domain'],
            "Problem Solving": ratings['problem_solving'],
            "Initiative": ratings['initiative']
        },
        "Professional Skills": {
            "Adaptability": ratings['adaptability'],
            "Communication": ratings['communication']
        },
        "Interpersonal Impact": {
            "Team Collaboration": ratings['teamwork'],
            "Support & Guidance": ratings['support']
        },
        "Overall Performance": {
            "Reliability": ratings['reliability'],
            "Overall Contribution": ratings['overall'],
            "Growth Potential": ratings['potential']
        }
    }
    
    # Calculate category averages
    category_scores = {}
    for category, metrics in performance_areas.items():
        category_scores[category] = sum(metrics.values()) / len(metrics)
    
    # Identify top strengths (ratings of 4 or 5)
    strengths = [k for k, v in ratings.items() if v >= 4]
    
    # Build a text block for the analysis part of the prompt
    analysis_text = ""
    for category, score in category_scores.items():
        analysis_text += f"\n- {category}: {score:.1f}/5"

    # Create a single, comprehensive prompt for a more efficient, single API call
    recommendation_prompt = f"""
    You are an expert in writing professional LinkedIn recommendations.
    Your task is to generate a recommendation for {employee_name}.

    - Employee: {employee_name}
    - Role: {employee_type}
    - My Relationship to them: {relationship}
    - Duration we worked together: {time_worked}
    - Performance Summary by Category:{analysis_text}
    - Employee's LinkedIn Profile (for context, do not mention the URL in the output): {linkedin_url or 'Not provided'}
    - Key Strengths (rated 4 or 5): {', '.join(strengths) if strengths else 'None specified'}

    
    Instructions for the recommendation:
    1. Start by clearly stating the working relationship ({relationship}) and the duration ({time_worked}).
    2. Highlight their role as a {employee_type} and their key responsibilities.
    3. Instead of just listing their strengths, weave them into a brief narrative or specific example that illustrates their positive impact. For instance, how their 'Problem Solving' skills unblocked a project or how their 'Team Collaboration' improved team morale.
    4. Conclude with a strong, forward-looking statement about their potential.
    5. Use vivid, descriptive language to make the recommendation feel more personal and human.
    """

    try:
        client = OpenAI(
        # Generate the final recommendation in a single call
        final_response = client.chat.completions.create(
            api_key=os.environ.get('OPENROUTER_API_KEY')
                {"role": "system", "content": "You are an expert in writing professional, warm, and authentic LinkedIn recommendations."},
                {"role": "user", "content": recommendation_prompt}
            ],
            max_tokens=255,
            temperature=0.75
        )
        return final_response.choices[0].message.content.strip()
    except RateLimitError:
        st.error("API rate limit or quota exceeded. Please check your OpenRouter account and billing details.")
        return None
    except Exception as e:
        st.error(f"An error occurred while generating the recommendation: {str(e)}")
        return None

def render_header():
    """Renders the main header of the application."""
    st.markdown("""
    <div class="header-container">
        <div class="linkedin-logo">
            <svg width="35" height="35" viewBox="0 0 24 24" fill="white">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
        </div>
        <h1 class="main-title">LinkedIn Recommendation Generator</h1>
        <p class="subtitle">Build impactful recommendations for LinkedIn - Made By github.com/ninjacode911</p>
    </div>
    """, unsafe_allow_html=True)

def render_input_form() -> Dict:
    """Renders the input form and returns a dictionary of user inputs."""
    st.markdown('<h3 class="section-header">📋 Basic Information</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        employee_name = st.text_input(
            "Employee Name",
            key="employee_name",
            placeholder="e.g., John Smith"
        )
        relationship = st.selectbox(
            "Your relationship with this person",
            ["", "Direct Manager", "Senior Manager", "Team Lead", "Colleague", "Project Manager", "Department Head", "HR Manager"],
            key="relationship"
        )
    
    with col2:
        employee_type = st.selectbox(
            "Employee Role/Department",
            ["", "Software Developer", "AI Engineer", "Marketing Specialist", "Sales Representative", 
             "Project Manager", "Data Analyst", "UI/UX Designer", "Customer Support", "Business Analyst", 
             "Product Manager", "DevOps Engineer", "Content Creator", "HR Specialist", "Other"],
            key="employee_type"
        )
        time_worked = st.selectbox(
            "How long have you worked together?",
            ["", "Less than 6 months", "6 months - 1 year", "1-2 years", "2-3 years", "3-5 years", "More than 5 years"],
            key="time_worked"
        )

    # LinkedIn Profile URL input
    linkedin_url = st.text_input(
        "Enter LinkedIn Profile URL",
        key="linkedin_url",
        placeholder="e.g., https://www.linkedin.com/in/username"
    )
    
    st.markdown('<h3 class="section-header">⭐ Performance Evaluation</h3>', unsafe_allow_html=True)
    st.markdown("*Rate each aspect on a scale of 1-5 stars*")
    
    ratings = {}
    st.markdown("<div class='sub-section-header'>Core Competencies</div>", unsafe_allow_html=True)
    ratings['domain'] = create_star_rating(
        "How would you rate the employee's knowledge and expertise in their specific field or role?", 
        "domain"
    )
    ratings['problem_solving'] = create_star_rating(
        "How effectively does the employee address challenges and find solutions?", 
        "problem_solving"
    )
    ratings['initiative'] = create_star_rating(
        "How proactive is the employee in taking initiative and contributing to company objectives?", 
        "initiative"
    )

    st.markdown("<div class='sub-section-header'>Professional Skills</div>", unsafe_allow_html=True)
    ratings['adaptability'] = create_star_rating(
        "How well does the employee handle change or take on new responsibilities?", 
        "adaptability"
    )
    ratings['communication'] = create_star_rating(
        "How clearly and professionally does the employee communicate ideas or information?", 
        "communication"
    )

    st.markdown("<div class='sub-section-header'>Interpersonal Skills</div>", unsafe_allow_html=True)
    ratings['teamwork'] = create_star_rating(
        "How well does the employee work with colleagues or teams to achieve goals?", 
        "teamwork"
    )
    ratings['support'] = create_star_rating(
        "How well does the employee support or guide others in the work environment?", 
        "support"
    )

    st.markdown("<div class='sub-section-header'>Performance & Potential</div>", unsafe_allow_html=True)
    ratings['reliability'] = create_star_rating(
        "How consistently does the employee demonstrate dedication and reliability?", 
        "reliability"
    )
    ratings['overall'] = create_star_rating(
        "How would you rate the employee's overall contribution to their role and the team?", 
        "overall"
    )
    ratings['potential'] = create_star_rating(
        "How would you rate the employee's potential for further growth or advancement within the organization?", 
        "potential"
    )
    
    return {
        "employee_name": employee_name,
        "relationship": relationship,
        "employee_type": employee_type,
        "time_worked": time_worked,
        "linkedin_url": linkedin_url,
        "ratings": ratings
    }

def render_results_section(ratings: Dict[str, int]):
    """Renders the recommendation, action buttons, and analytics."""
    if st.session_state.recommendation_generated:
        st.markdown(f"""
        <div class="result-container">
            <h3 class="result-title">📝 Your LinkedIn Recommendation</h3>
            <div class="recommendation-text">
                {st.session_state.generated_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            # This provides a clear way for users to copy the text.
            if st.button("📋 Show Text for Copying"):
                st.code(st.session_state.generated_text, language="text")
                st.info("You can now manually copy the text above.")
        
        with col2:
            # This provides a clear way for users to copy the text.
            if st.button("� Show Text for Copying"):
                st.code(st.session_state.generated_text, language="text")
                st.info("You can now manually copy the text above.")
        if st.session_state.saved_linkedin_url:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0077B5 0%, #005885 100%); color: white; padding: 8px; border-radius: 5px; margin: 1rem 0; text-align: center; font-family: 'Source Sans Pro', sans-serif; font-size: 1rem;">
                st.session_state.recommendation_generated = False
            """, unsafe_allow_html=True)
        
        # Instructions
        st.markdown("""
        <div class="result-container">
            <h4 style="color: white; margin-bottom: 1rem;">📖 How to Post on LinkedIn</h4>
            <ol style="font-family: 'Source Sans Pro', sans-serif; line-height: 1.6;">
                <li>Copy the recommendation text above</li>
                <li>Click on the person's LinkedIn profile</li>
                <li>Click "More" → "Recommend"</li>
                <li>Paste the generated recommendation</li>
                <li>Review and send!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        # Analytics section
        st.markdown('<h4 style="color: #0077B5;">📊 Rating Summary</h4>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        avg_rating = sum(ratings.values()) / len(ratings)
        highest_rating = max(ratings.values())
        lowest_rating = min(ratings.values())
        
        with col1:
            st.metric("Average Rating", f"{avg_rating:.1f}/5", f"{avg_rating/5*100:.0f}%")
        with col2:
            st.metric("Highest Rating", f"{highest_rating}/5")
        with col3:
            st.metric("Lowest Rating", f"{lowest_rating}/5")
        with col4:
            st.metric("Word Count", len(st.session_state.generated_text.split()))

def main():
    """Main function to run the Streamlit application."""
    # Robustly check for API key from environment variables (Hugging Face secrets)
    # or from a local secrets.toml file for local development.
    api_key = os.environ.get('OPENROUTER_API_KEY')
    
    if not api_key:
        try:
            # This check is for local development with a .streamlit/secrets.toml file.
            if 'OPENROUTER_API_KEY' in st.secrets:
                api_key = st.secrets['OPENROUTER_API_KEY']
                os.environ['OPENROUTER_API_KEY'] = api_key
        except FileNotFoundError:
            # This is expected on Hugging Face if you only use repository secrets.
            # We pass silently and rely on the final check below.
            pass

    # Final check to ensure the API key was found by either method.
    if not api_key:
        st.error("🔑 OpenRouter API key not found. Please add it to your Hugging Face Space secrets in the 'Settings' tab.")
        st.stop()
    render_header()

    # Initialize session state
    if 'recommendation_generated' not in st.session_state:
        st.session_state.recommendation_generated = False
    if 'generated_text' not in st.session_state:
        st.session_state.generated_text = ""
    if 'saved_linkedin_url' not in st.session_state:
        st.session_state.saved_linkedin_url = ""

    form_data = render_input_form()
    
    # Generate recommendation button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate LinkedIn Recommendation", type="primary"):
            # Validate required fields
            required_fields = ["employee_name", "employee_type", "relationship", "time_worked"]
            if not all(form_data[field] for field in required_fields):
                st.error("Please fill in all required fields in the 'Basic Information' section.")
            else:
                with st.spinner("🤖 Analyzing performance data and crafting your recommendation..."):
                    progress_bar = st.progress(0, text="Analyzing...")
                    time.sleep(0.5)
                    progress_bar.progress(50, text="Generating text...")
                    
                    recommendation = generate_recommendation(**form_data)
                    
                    progress_bar.progress(100, text="Done!")
                    time.sleep(0.5)
                    progress_bar.empty()
                
                if recommendation:
                    st.session_state.recommendation_generated = True
                    st.session_state.generated_text = recommendation
                    st.session_state.saved_linkedin_url = form_data["linkedin_url"]
                    st.success("✅ Recommendation generated successfully!")
                    st.rerun() # Rerun to display the results section cleanly

    # Display results in a separate container
    render_results_section(form_data["ratings"])

if __name__ == "__main__":
    main()
