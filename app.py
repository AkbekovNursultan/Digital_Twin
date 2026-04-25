"""
Layer 4 — Application: Digital Twin Career Dashboard
Nursultan Akbekov — Software Engineering, Ala-Too International University
Run with: streamlit run app.py
"""

import os
import json
import streamlit as st
import plotly.graph_objects as go
import anthropic

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Digital Twin — Nursultan Akbekov",
    page_icon="🤖",
    layout="wide"
)

# ── Data ──────────────────────────────────────────────────────────────────────
PROFILE = {
    "name": "Nursultan Akbekov",
    "title": "Java Backend Developer",
    "university": "Ala-Too International University",
    "major": "Software Engineering",
    "gpa": "3.59",
    "year": "2nd Year (2023–2027)"
}

HARD_SKILLS = {
    "Java Core": 90,
    "Spring Boot": 85,
    "REST API": 88,
    "PostgreSQL": 80,
    "Spring Security": 78,
    "Hibernate/JPA": 80,
    "JUnit/Mockito": 75,
    "Git": 85,
    "Vue.js": 55,
    "HTML/CSS": 60,
    "C#": 40,
    "Generative AI": 50,
}

SOFT_SKILLS = {
    "Problem Solving": 88,
    "Teamwork": 82,
    "Fast Learning": 90,
    "Analytical Thinking": 85,
    "Attention to Detail": 83,
    "Technical Communication": 75,
    "Time Management": 78,
    "Critical Thinking": 84,
    "Adaptability": 86,
    "Self-direction": 80,
}

PREDICTION = {
    "top_job": "Java Developer (Experienced)",
    "score": "25.8%",
    "missing_skills": ["Advanced Java", "AWS", "Docker", "Kubernetes", "Agile"],
    "current_skills": list(HARD_SKILLS.keys())
}

SEMESTER_DATA = {
    "top_skill": "Spring Boot + Spring Security",
    "top_course": "Back-end Development (100/100 ✨)",
    "most_productive_day": "Tuesday",
    "internship": "O! Mobile Operator Labs 6.0",
    "project": "Client Registration System (CRM)",
    "gpa": "3.59",
    "semesters_completed": 6,
    "total_credits": 154,
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="background:#1e293b; color:white; width:80px; height:80px; 
        border-radius:50%; display:flex; align-items:center; justify-content:center; 
        font-size:2em; font-weight:bold; margin-bottom:10px; border:2px solid #3b82f6;">
        NA
        </div>
    """, unsafe_allow_html=True)
    st.title("🤖 Digital Twin")
    st.markdown(f"**{PROFILE['name']}**")
    st.markdown(f"*{PROFILE['title']}*")
    st.markdown(f"🎓 {PROFILE['university']}")
    st.markdown(f"📊 GPA: **{PROFILE['gpa']}**")
    st.divider()
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "",
        ["⚖️ Balance Wheel", "🗺️ RPG Tech Tree",
         "💬 Live Coach", "🎁 Semester Wrapped"],
        label_visibility="collapsed"
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — BALANCE WHEEL
# ══════════════════════════════════════════════════════════════════════════════
if page == "⚖️ Balance Wheel":
    st.title("⚖️ Skill Balance Wheel")
    st.markdown("Visual comparison of your **Hard Technical Skills** vs **Soft Skills**")
    st.divider()

    col1, col2 = st.columns(2)

    # Hard Skills Radar
    with col1:
        st.subheader("🔧 Hard / Technical Skills")
        hard_names = list(HARD_SKILLS.keys())
        hard_vals  = list(HARD_SKILLS.values())
        hard_vals_closed = hard_vals + [hard_vals[0]]
        hard_names_closed = hard_names + [hard_names[0]]

        fig_hard = go.Figure(go.Scatterpolar(
            r=hard_vals_closed,
            theta=hard_names_closed,
            fill="toself",
            fillcolor="rgba(0, 120, 255, 0.25)",
            line=dict(color="royalblue", width=2),
            name="Hard Skills"
        ))
        fig_hard.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=420,
            margin=dict(t=40, b=40)
        )
        st.plotly_chart(fig_hard, use_container_width=True)

    # Soft Skills Radar
    with col2:
        st.subheader("🧠 Soft Skills")
        soft_names = list(SOFT_SKILLS.keys())
        soft_vals  = list(SOFT_SKILLS.values())
        soft_vals_closed = soft_vals + [soft_vals[0]]
        soft_names_closed = soft_names + [soft_names[0]]

        fig_soft = go.Figure(go.Scatterpolar(
            r=soft_vals_closed,
            theta=soft_names_closed,
            fill="toself",
            fillcolor="rgba(0, 200, 120, 0.25)",
            line=dict(color="mediumseagreen", width=2),
            name="Soft Skills"
        ))
        fig_soft.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=420,
            margin=dict(t=40, b=40)
        )
        st.plotly_chart(fig_soft, use_container_width=True)

    # Summary metrics
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hard Skills", f"{len(HARD_SKILLS)}", "skills tracked")
    c2.metric("Avg Hard Score", f"{round(sum(HARD_SKILLS.values())/len(HARD_SKILLS))}%")
    c3.metric("Soft Skills", f"{len(SOFT_SKILLS)}", "skills tracked")
    c4.metric("Avg Soft Score", f"{round(sum(SOFT_SKILLS.values())/len(SOFT_SKILLS))}%")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — RPG TECH TREE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ RPG Tech Tree":
    st.title("🗺️ RPG Career Tech Tree")
    st.markdown("Your skill unlock map to **Java Developer (Experienced)**")
    st.divider()

    # Build node data
    nodes = [
        # Current unlocked skills (green)
        dict(id="Java Core",       x=1, y=5, color="#22c55e", status="✅ Unlocked"),
        dict(id="OOP",             x=2, y=6, color="#22c55e", status="✅ Unlocked"),
        dict(id="Spring Boot",     x=2, y=5, color="#22c55e", status="✅ Unlocked"),
        dict(id="REST API",        x=3, y=5, color="#22c55e", status="✅ Unlocked"),
        dict(id="Spring Security", x=3, y=6, color="#22c55e", status="✅ Unlocked"),
        dict(id="Hibernate/JPA",   x=3, y=4, color="#22c55e", status="✅ Unlocked"),
        dict(id="PostgreSQL",      x=4, y=4, color="#22c55e", status="✅ Unlocked"),
        dict(id="JUnit/Mockito",   x=4, y=6, color="#22c55e", status="✅ Unlocked"),
        dict(id="Git",             x=1, y=3, color="#22c55e", status="✅ Unlocked"),
        dict(id="Vue.js",          x=2, y=3, color="#22c55e", status="✅ Unlocked"),
        # Missing skills (orange)
        dict(id="Advanced Java",   x=5, y=5, color="#f97316", status="🔒 Missing"),
        dict(id="Docker",          x=5, y=3, color="#f97316", status="🔒 Missing"),
        dict(id="AWS",             x=6, y=4, color="#f97316", status="🔒 Missing"),
        dict(id="Kubernetes",      x=6, y=3, color="#f97316", status="🔒 Missing"),
        dict(id="Agile/Scrum",     x=5, y=7, color="#f97316", status="🔒 Missing"),
        # Dream job (gold)
        dict(id="☆ Java Dev\n(Experienced)", x=8, y=5, color="#eab308", status="🏆 Dream Job"),
    ]

    edges = [
        ("Java Core", "Spring Boot"),
        ("Java Core", "OOP"),
        ("OOP", "Spring Boot"),
        ("Spring Boot", "REST API"),
        ("Spring Boot", "Spring Security"),
        ("Spring Boot", "Hibernate/JPA"),
        ("Hibernate/JPA", "PostgreSQL"),
        ("REST API", "Advanced Java"),
        ("Spring Security", "Advanced Java"),
        ("Git", "Vue.js"),
        ("Git", "Docker"),
        ("Docker", "AWS"),
        ("Docker", "Kubernetes"),
        ("Advanced Java", "☆ Java Dev\n(Experienced)"),
        ("AWS", "☆ Java Dev\n(Experienced)"),
        ("Kubernetes", "☆ Java Dev\n(Experienced)"),
        ("Agile/Scrum", "☆ Java Dev\n(Experienced)"),
        ("JUnit/Mockito", "Advanced Java"),
    ]

    # Draw edges
    edge_x, edge_y = [], []
    node_dict = {n["id"]: n for n in nodes}
    for src, dst in edges:
        if src in node_dict and dst in node_dict:
            edge_x += [node_dict[src]["x"], node_dict[dst]["x"], None]
            edge_y += [node_dict[src]["y"], node_dict[dst]["y"], None]

    fig_tree = go.Figure()

    fig_tree.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(color="#475569", width=1.5),
        hoverinfo="none"
    ))

    for n in nodes:
        fig_tree.add_trace(go.Scatter(
            x=[n["x"]], y=[n["y"]],
            mode="markers+text",
            marker=dict(size=38, color=n["color"],
                        line=dict(color="white", width=2)),
            text=[n["id"]],
            textposition="bottom center",
            textfont=dict(size=10, color="white"),
            hovertemplate=f"<b>{n['id']}</b><br>{n['status']}<extra></extra>",
            showlegend=False
        ))

    fig_tree.update_layout(
        height=520,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_tree, use_container_width=True)

    # Legend
    lc1, lc2, lc3 = st.columns(3)
    lc1.success("✅ Unlocked — skills you already have")
    lc2.warning("🔒 Missing — skills to unlock next")
    lc3.info("🏆 Dream Job — your ML-predicted target role")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — LIVE COACH CHATBOT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💬 Live Coach":
    st.title("💬 Live Career Coach")
    st.markdown("Chat with your **Digital Twin** — powered by Claude AI")
    st.divider()

    # Roast toggle
    roast_mode = st.toggle("🔥 Roast My Stack Mode", value=False)

    if roast_mode:
        st.error("🔥 **ROAST MODE ACTIVATED** — Aggressive tech lead incoming...")
        system_prompt = """You are an extremely aggressive, brutally honest senior tech lead 
        with 15 years of Java experience. You are reviewing Nursultan Akbekov's tech stack 
        and career progress. You must:
        - Roast his stack humorously but constructively
        - Mock the fact he only has Vue.js for frontend ("why not React, are you allergic?")
        - Point out that missing Docker/Kubernetes in 2025 is basically career suicide
        - Be harsh about the missing AWS skills
        - Joke about his GPA being 3.59 ("almost a 4.0, what happened?")
        - End every response with one genuine piece of advice
        - Keep it funny, sharp, and under 150 words
        Profile: Java Backend Developer, Spring Boot, REST API, PostgreSQL, 
        GPA 3.59, missing: Advanced Java, Docker, AWS, Kubernetes"""
    else:
        system_prompt = """You are a warm, encouraging career coach and Digital Twin 
        for Nursultan Akbekov, a Java Backend Developer from Kyrgyzstan studying 
        Software Engineering at Ala-Too International University (GPA 3.59).
        His skills: Java Core, Spring Boot, Spring Security, Hibernate/JPA, 
        REST API, PostgreSQL, MySQL, JUnit, Mockito, Git, Vue.js, C#, Generative AI.
        His predicted career path: Java Developer (Experienced).
        Missing skills to reach that goal: Advanced Java, Docker, AWS, Kubernetes, Agile.
        Give specific, actionable career advice. Be concise (under 150 words).
        Always reference his actual skills and goals."""

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    if prompt := st.chat_input("Ask your Digital Twin anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..." if not roast_mode else "Loading insults..."):
                try:
                    api_key = os.getenv("ANTHROPIC_API_KEY", "")
                    if not api_key:
                        st.error("ANTHROPIC_API_KEY not found. Add it to your .env file.")
                    else:
                        client = anthropic.Anthropic(api_key=api_key)
                        response = client.messages.create(
                            model="claude-3-5-sonnet-20240620",
                            max_tokens=300,
                            system=system_prompt,
                            messages=[
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.messages
                            ]
                        )
                        reply = response.content[0].text
                        st.markdown(reply)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": reply}
                        )
                except Exception as e:
                    st.error(f"API error: {e}")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — SEMESTER WRAPPED
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎁 Semester Wrapped":
    st.title("🎁 Semester Wrapped 2024–2025")
    st.markdown("Your **year in review** — shareable on LinkedIn")
    st.divider()

    # Card CSS
    st.markdown("""
    <style>
    .wrapped-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 50%, #1a1a2e 100%);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        border: 1px solid #3b82f6;
        box-shadow: 0 0 30px rgba(59,130,246,0.3);
    }
    .wrapped-title {
        font-size: 2.2em;
        font-weight: 900;
        color: #60a5fa;
        margin-bottom: 5px;
    }
    .wrapped-subtitle {
        font-size: 1em;
        color: #94a3b8;
        margin-bottom: 30px;
    }
    .stat-box {
        background: rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .stat-label {
        font-size: 0.75em;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stat-value {
        font-size: 1.3em;
        font-weight: 700;
        color: #f1f5f9;
    }
    </style>
    """, unsafe_allow_html=True)

    col_left, col_mid, col_right = st.columns([1, 2, 1])

    with col_mid:
        # Construct HTML string without indentation to avoid Streamlit interpreting it as markdown/code
        wrapped_html = f"""
<div class="wrapped-card">
    <div class="wrapped-title">🎓 {PROFILE['name']}</div>
    <div class="wrapped-subtitle">{PROFILE['major']} · {PROFILE['university']}</div>
    <div class="stat-box">
        <div class="stat-label">🏆 Top Skill Learned</div>
        <div class="stat-value">{SEMESTER_DATA['top_skill']}</div>
    </div>
    <div class="stat-box">
        <div class="stat-label">📚 Best Course This Year</div>
        <div class="stat-value">{SEMESTER_DATA['top_course']}</div>
    </div>
    <div class="stat-box">
        <div class="stat-label">💼 Internship Completed</div>
        <div class="stat-value">{SEMESTER_DATA['internship']}</div>
    </div>
    <div class="stat-box">
        <div class="stat-label">🚀 Shipped Project</div>
        <div class="stat-value">{SEMESTER_DATA['project']}</div>
    </div>
    <div class="stat-box">
        <div class="stat-label">📈 Cumulative GPA</div>
        <div class="stat-value">{SEMESTER_DATA['gpa']} / 4.0</div>
    </div>
    <div class="stat-box">
        <div class="stat-label">🎯 ML Predicted Career Path</div>
        <div class="stat-value">Java Developer (Experienced)</div>
    </div>
    <div class="stat-box">
        <div class="stat-label">📦 Total Credits Earned</div>
        <div class="stat-value">{SEMESTER_DATA['total_credits']} credits across {SEMESTER_DATA['semesters_completed']} semesters</div>
    </div>
    <br>
    <div style="color:#475569; font-size:0.7em;">
        Generated by Digital Twin Career Engine · 2025
    </div>
</div>
"""
        st.markdown(wrapped_html, unsafe_allow_html=True)

    st.divider()
    st.info("📸 Take a screenshot of the card above to share on LinkedIn!")

    # Quick stats row
    st.subheader("📊 By the numbers")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("GPA", "3.59")
    m2.metric("Credits", "154")
    m3.metric("Semesters", "6")
    m4.metric("Hard Skills", "22")
    m5.metric("Soft Skills", "16")