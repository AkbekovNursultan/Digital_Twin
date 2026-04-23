"""
Layer 2 — Model: Career Prediction via Cosine Similarity
Digital Twin Career Engine — Nursultan Akbekov

Input:  skill_vector.json  (your personal skills from NotebookLM)
Input:  jobs_dataset.csv   (the Kaggle dataset)
Output: prediction_output.json  (top 3 jobs + missing skills)
"""

import json
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── 1. Load your personal skill vector ────────────────────────────────────────
skill_vector = {
    "hard_skills": [
        "Java Core", "Spring Boot", "Spring Security", "Spring Data JPA",
        "Hibernate", "REST API", "PostgreSQL", "MySQL", "Maven",
        "JUnit", "Mockito", "Git", "Jira", "Thymeleaf",
        "HTML", "CSS", "Vue.js", "OOP", "C#", "Generative AI",
        "Mobile Application Development", "VR Design"
    ],
    "soft_skills": [
        "Teamwork", "Collaboration", "Problem Solving", "Analytical Thinking",
        "Time Management", "Deadline Orientation", "Technical Communication",
        "Non-technical Communication", "Adaptability", "Fast Learning",
        "Critical Thinking", "System Thinking", "Attention to Detail",
        "Independence", "Self-direction", "Competitive Mindset"
    ],
    "education": {
        "degree": "Bachelor",
        "major": "Software Engineering",
        "gpa": "3.59",
        "relevant_courses": [
            "Programming Languages I & II", "Database Systems", "OOP",
            "Back-end Development", "Front-end", "Software Engineering",
            "Design & Analysis of Algorithms", "Mobile Application Development",
            "Robotics", "VR Design", "Generative AI", "C#",
            "Software Architecture & Design Patterns", "Competitive Programming"
        ]
    }
}

# Combine all skills into one string (your "skill document")
user_skills_text = " ".join(
    skill_vector["hard_skills"] + skill_vector["soft_skills"]
).lower()

print("✅ Skill vector loaded.")
print(f"   Hard skills : {len(skill_vector['hard_skills'])}")
print(f"   Soft skills : {len(skill_vector['soft_skills'])}")
print()

# ── 2. Load and clean the job dataset ─────────────────────────────────────────
df = pd.read_csv("jobs_dataset.csv")

# Keep only rows with a title and skills column
df = df.dropna(subset=["Title", "Skills"])

# Combine Title + Skills + Keywords into one text per job
def build_job_text(row):
    parts = [str(row.get("Title", "")),
             str(row.get("Skills", "")),
             str(row.get("Keywords", ""))]
    return " ".join(parts).lower()

df["job_text"] = df.apply(build_job_text, axis=1)

print(f"✅ Dataset loaded: {len(df)} job listings.")
print()

# ── 3. TF-IDF Vectorisation ───────────────────────────────────────────────────
all_texts = df["job_text"].tolist() + [user_skills_text]

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),   # unigrams + bigrams
    max_features=5000
)
tfidf_matrix = vectorizer.fit_transform(all_texts)

# Your vector is always the last row
user_vector = tfidf_matrix[-1]
job_vectors = tfidf_matrix[:-1]

# ── 4. Cosine similarity ──────────────────────────────────────────────────────
similarities = cosine_similarity(user_vector, job_vectors).flatten()
df["similarity_score"] = similarities

# Sort by score, drop duplicates by Title, take top 3
top_jobs = (
    df.sort_values("similarity_score", ascending=False)
      .drop_duplicates(subset=["Title"])
      .head(3)
)

print("🎯 Top 3 predicted job matches:")
print()

# ── 5. Calculate missing skills per job ──────────────────────────────────────
def get_missing_skills(job_skills_raw: str, user_skills: list) -> list:
    """Return skills in the job that the user doesn't have."""
    # Normalise job skills — split on ; or ,
    job_skills = [
        s.strip().lower()
        for s in re.split(r"[;,]", str(job_skills_raw))
        if s.strip()
    ]
    user_lower = [s.lower() for s in user_skills]

    missing = []
    for skill in job_skills:
        # Partial match check: skill is 'missing' if no user skill contains it
        matched = any(skill in u or u in skill for u in user_lower)
        if not matched and skill not in missing:
            missing.append(skill.title())
    return missing

all_user_skills = skill_vector["hard_skills"] + skill_vector["soft_skills"]
results = []

for _, row in top_jobs.iterrows():
    missing = get_missing_skills(row["Skills"], all_user_skills)
    # Cap to top 8 most important missing skills
    missing_top = missing[:8]

    job_result = {
        "job_id": row.get("JobID", "N/A"),
        "title": row["Title"],
        "experience_level": row.get("ExperienceLevel", "N/A"),
        "similarity_score": round(float(row["similarity_score"]), 4),
        "missing_skills": missing_top
    }
    results.append(job_result)
    print(f"  #{len(results)}  {row['Title']}")
    print(f"      Level      : {row.get('ExperienceLevel', 'N/A')}")
    print(f"      Score      : {round(row['similarity_score'] * 100, 1)}%")
    print(f"      Missing    : {', '.join(missing_top) if missing_top else 'None — you match fully!'}")
    print()

# ── 6. Write output JSON ──────────────────────────────────────────────────────
output = {
    "profile": {
        "name": "Nursultan Akbekov",
        "degree": skill_vector["education"]["degree"],
        "major": skill_vector["education"]["major"],
        "gpa": skill_vector["education"]["gpa"],
        "total_hard_skills": len(skill_vector["hard_skills"]),
        "total_soft_skills": len(skill_vector["soft_skills"])
    },
    "top_predicted_jobs": results
}

with open("prediction_output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ Results saved to prediction_output.json")
print()
print("=== FULL OUTPUT ===")
print(json.dumps(output, indent=2, ensure_ascii=False))