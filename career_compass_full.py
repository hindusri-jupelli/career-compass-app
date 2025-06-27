import streamlit as st
import requests

# --------------- API CONFIG ---------------- #
RAPIDAPI_KEY = "bec5f09fmsh15acdd3ff8c7fd0p15abd5jsnf7f492b60b06"
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}
UDEMY_HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "udemy-search-results.p.rapidapi.com"
}

# --------------- INTEREST TO CAREER MAP ---------------- #
career_map = {
    "Coding": ["Software Developer", "AI Engineer", "Data Analyst"],
    "Design": ["UI/UX Designer", "Graphic Designer"],
    "Biology": ["Biotech Researcher", "Healthcare Analyst"],
    "Finance": ["Financial Analyst", "Accountant"],
    "Writing": ["Content Writer", "Technical Writer"],
    "Public Speaking": ["HR Manager", "PR Specialist"]
}

# --------------- MOCK SALARY DATA ---------------- #
salary_map = {
    "Software Developer": "$75,000 - $120,000",
    "AI Engineer": "$95,000 - $150,000",
    "Data Analyst": "$60,000 - $90,000",
    "UI/UX Designer": "$65,000 - $100,000",
    "Graphic Designer": "$50,000 - $80,000",
    "Biotech Researcher": "$70,000 - $110,000",
    "Healthcare Analyst": "$65,000 - $90,000",
    "Financial Analyst": "$70,000 - $95,000",
    "Accountant": "$60,000 - $85,000",
    "Content Writer": "$45,000 - $70,000",
    "Technical Writer": "$55,000 - $85,000",
    "HR Manager": "$60,000 - $100,000",
    "PR Specialist": "$50,000 - $90,000"
}

# --------------- FUNCTIONS ---------------- #
def fetch_jobs(title, location, remote_only=False):
    query = f"{title} in {location}" if location != "Any" else title
    url = f"https://jsearch.p.rapidapi.com/search?query={query}&num_pages=1"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        jobs = response.json()["data"]
        if remote_only:
            return [job for job in jobs if job.get("job_is_remote")]
        return jobs
    else:
        return []

def fetch_courses(topic):
    url = f"https://udemy-search-results.p.rapidapi.com/search/{topic}"
    response = requests.get(url, headers=UDEMY_HEADERS)
    if response.status_code == 200:
        return response.json().get("results", [])[:3]  # top 3 courses
    return []

# --------------- STREAMLIT UI ---------------- #
st.title("Career Compass – Full Smart Edition")
st.markdown("Get real-time **career insights**, **salary ranges**, and **courses** based on your interests.")

# Input
selected_interests = st.multiselect("🎯 Select Your Interests:", list(career_map.keys()))
country = st.selectbox("🌍 Filter Jobs by Country:", ["Any", "India", "USA", "UK", "Canada", "Germany"])
remote_only = st.checkbox("💻 Remote Jobs Only")

# Generate results
if st.button("🔍 Explore Careers"):
    if not selected_interests:
        st.warning("Please select at least one interest.")
    else:
        careers = set()
        for interest in selected_interests:
            careers.update(career_map[interest])
        
        for career in sorted(careers):
            with st.expander(f"🔎 {career}"):
                col1, col2 = st.columns([1, 2])
                
                # Mock salary info
                with col1:
                    st.subheader("💰 Salary Estimate")
                    st.write(salary_map.get(career, "Data not available"))
                
                # Fetch and show jobs
                with col2:
                    st.subheader("📌 Job Listings")
                    jobs = fetch_jobs(career, country, remote_only)
                    if jobs:
                        for job in jobs[:2]:  # Show 2 jobs
                            st.markdown(f"**{job['job_title']}** at *{job['employer_name']}*")
                            st.markdown(f"📍 {job.get('job_city', 'Location')}, {job.get('job_country', '')}")
                            st.markdown(f"[Apply Here]({job['job_apply_link']})")
                            st.markdown("---")
                    else:
                        st.info("No jobs found for the selected filters.")

                # Course recommendations
                st.subheader("🎓 Recommended Courses")
                courses = fetch_courses(career)
                if courses:
                    for course in courses:
                        st.markdown(f"**{course['title']}**")
                        st.markdown(f"[View Course]({course['url']})")
                else:
                    st.info("No courses found for this career.")

# View all mapping
with st.expander("📘 View Interest ➜ Career Mapping"):
    for k, v in career_map.items():
        st.write(f"**{k}** ➜ {', '.join(v)}")
