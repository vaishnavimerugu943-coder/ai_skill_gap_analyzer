from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key="mock_interview_secret"

# -------------------------------------------------
# CAREER → REQUIRED SKILLS (STEP 12)
# -------------------------------------------------
CAREER_SKILLS = {
    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Data Handling",
        "Mathematics"
    ],
    "Data Analyst": [
        "Python",
        "SQL",
        "Data Visualization",
        "Statistics",
        "Excel"
    ],
    "Full Stack Developer": [
        "HTML/CSS",
        "JavaScript",
        "Backend Development",
        "Database",
        "API Development"
    ]
}

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -------------------------------------------------
# SKILL ASSESSMENT – CAREER WISE QUESTIONS
# -------------------------------------------------
@app.route('/assessment', methods=['POST', 'GET'])
def assessment():
    if request.method == 'POST':
        career = request.form.get('career')

        questions = {}

        if career == "AI Engineer":
            questions = {
                "q1": ("What is supervised learning?", "Uses labeled data", "Uses unlabeled data"),
                "q2": ("Which language is most used in AI?", "Python", "HTML"),
                "q3": ("Neural networks are inspired by?", "Human brain", "Database"),
                "q4": ("Which library is used for deep learning?", "TensorFlow", "Bootstrap"),
                "q5": ("AI models mainly depend on?", "Data", "UI Design")
            }

        elif career == "Data Analyst":
            questions = {
                "q1": ("What is data cleaning?", "Removing errors in data", "Adding noise"),
                "q2": ("Best language for data analysis?", "Python", "CSS"),
                "q3": ("SQL is used for?", "Querying databases", "Designing UI"),
                "q4": ("Which chart shows trends?", "Line chart", "Pie chart"),
                "q5": ("Statistics helps in?", "Data interpretation", "Styling pages")
            }

        elif career == "Full Stack Developer":
            questions = {
                "q1": ("Frontend uses which technologies?", "HTML, CSS, JS", "Python only"),
                "q2": ("Backend framework example?", "Flask", "Bootstrap"),
                "q3": ("Which is a database?", "MySQL", "React"),
                "q4": ("Frontend framework?", "React", "NumPy"),
                "q5": ("API stands for?", "Application Programming Interface", "Applied Program Internet")
            }

        return render_template(
            'assessment.html',
            career=career,
            questions=questions
        )

    return redirect(url_for('home'))


# -------------------------------------------------
# DASHBOARD + SKILL GAP ANALYZER (STEP 13)
# -------------------------------------------------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    # ---------- CASE 1: Coming from assessment (POST) ----------
    if request.method == 'POST':
        career = request.form.get('career')

        QUESTION_SKILL_MAP = {
            "AI Engineer": {
                "q1": "Machine Learning",
                "q2": "Python",
                "q3": "Deep Learning",
                "q4": "Deep Learning",
                "q5": "Data Handling"
            },
            "Data Analyst": {
                "q1": "Data Cleaning",
                "q2": "Python",
                "q3": "SQL",
                "q4": "Data Visualization",
                "q5": "Statistics"
            },
            "Full Stack Developer": {
                "q1": "HTML/CSS",
                "q2": "Backend Development",
                "q3": "Database",
                "q4": "JavaScript",
                "q5": "API Development"
            }
        }

        score = 0
        total_questions = 5
        weak_skills = []

        for i in range(1, 6):
            answer = request.form.get(f"q{i}")
            skill = QUESTION_SKILL_MAP[career][f"q{i}"]

            if answer == "1":
                score += 1
            else:
                weak_skills.append(skill)

        percentage = int((score / total_questions) * 100)

        if percentage <= 40:
            level = "Beginner"
        elif percentage <= 70:
            level = "Intermediate"
        else:
            level = "Advanced"

        # ✅ SAVE EVERYTHING IN SESSION
        session['dashboard_data'] = {
            'career': career,
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'level': level,
            'weak_skills': weak_skills
        }

    # ---------- CASE 2: Coming back (GET) ----------
    else:
        data = session.get('dashboard_data')

        # 🔒 SAFETY CHECK
        if not data:
            return redirect(url_for('home'))

        career = data['career']
        score = data['score']
        total_questions = data['total']
        percentage = data['percentage']
        level = data['level']
        weak_skills = data['weak_skills']

    return render_template(
        'dashboard.html',
        career=career,
        score=score,
        total=total_questions,
        percentage=percentage,
        level=level,
        weak_skills=weak_skills
    )


# -------------------------------------------------
# CAREER GROWTH PLANNER (NEXT MODULE)
# -------------------------------------------------
@app.route('/planner')
def planner():
    career = request.args.get('career')
    level = request.args.get('level')
    percentage = int(float(request.args.get('percentage', '0')))

    # Job Readiness Score
    job_readiness = percentage

    skills_focus = {
        "AI Engineer": ["Deep Learning", "Model Optimization", "MLOps"],
        "Data Analyst": ["Data Visualization", "Statistics", "SQL"],
        "Full Stack Developer": ["Backend APIs", "Database Design", "Authentication"]
    }

    projects = {
        "AI Engineer": [
            "AI Skill Gap Analyzer",
            "Face Recognition System",
            "Chatbot using NLP"
        ],
        "Data Analyst": [
            "Sales Analytics Dashboard",
            "Customer Churn Prediction",
            "Power BI Report"
        ],
        "Full Stack Developer": [
            "Job Portal Application",
            "E-commerce Website",
            "REST API System"
        ]
    }

    courses = {
        "AI Engineer": [
            "Machine Learning – Andrew Ng",
            "Deep Learning Specialization",
            "Python for AI"
        ],
        "Data Analyst": [
            "Google Data Analytics",
            "SQL for Data Science",
            "Statistics Essentials"
        ],
        "Full Stack Developer": [
            "Full Stack Web Development",
            "React & Node.js",
            "Database Design"
        ]
    }

    return render_template(
        "planner.html",
        career=career,
        level=level,
        job_readiness=job_readiness,
        skills=skills_focus.get(career, []),
        projects=projects.get(career, []),
        courses=courses.get(career, [])
    )
@app.route('/weekly-plan')
def weekly_plan():
    career = request.args.get('career')
    level = request.args.get('level')

    weekly_plans = {

        "AI Engineer": {
            "Beginner": {
                "Monday": "Python basics",
                "Tuesday": "Linear Algebra fundamentals",
                "Wednesday": "Introduction to Machine Learning",
                "Thursday": "Supervised learning basics",
                "Friday": "Simple ML models",
                "Saturday": "Practice problems",
                "Sunday": "Revision & rest"
            },
            "Intermediate": {
                "Monday": "Data preprocessing",
                "Tuesday": "ML algorithms deep dive",
                "Wednesday": "Neural Networks",
                "Thursday": "CNN & RNN basics",
                "Friday": "Mini AI project",
                "Saturday": "Model optimization",
                "Sunday": "Mock test"
            },
            "Advanced": {
                "Monday": "Advanced Deep Learning",
                "Tuesday": "Transformers & NLP",
                "Wednesday": "Model deployment (MLOps)",
                "Thursday": "Performance tuning",
                "Friday": "Real-world AI project",
                "Saturday": "Research paper reading",
                "Sunday": "System design review"
            }
        },

        "Data Analyst": {
            "Beginner": {
                "Monday": "Excel basics",
                "Tuesday": "Data cleaning",
                "Wednesday": "SQL fundamentals",
                "Thursday": "Basic statistics",
                "Friday": "Simple charts",
                "Saturday": "Practice datasets",
                "Sunday": "Revision"
            },
            "Intermediate": {
                "Monday": "Advanced SQL",
                "Tuesday": "Statistics & probability",
                "Wednesday": "Python (Pandas)",
                "Thursday": "Data visualization tools",
                "Friday": "Dashboard creation",
                "Saturday": "Mini analysis project",
                "Sunday": "Revision"
            },
            "Advanced": {
                "Monday": "Predictive analytics",
                "Tuesday": "Time series analysis",
                "Wednesday": "Advanced Python",
                "Thursday": "Power BI optimization",
                "Friday": "Real-world dataset project",
                "Saturday": "Business case analysis",
                "Sunday": "Portfolio improvement"
            }
        },

        "Full Stack Developer": {
            "Beginner": {
                "Monday": "HTML basics",
                "Tuesday": "CSS styling",
                "Wednesday": "JavaScript basics",
                "Thursday": "DOM manipulation",
                "Friday": "Simple webpage",
                "Saturday": "Practice",
                "Sunday": "Revision"
            },
            "Intermediate": {
                "Monday": "Advanced JavaScript",
                "Tuesday": "Backend with Flask/Node",
                "Wednesday": "Databases (SQL)",
                "Thursday": "REST APIs",
                "Friday": "Mini full-stack app",
                "Saturday": "Bug fixing",
                "Sunday": "Revision"
            },
            "Advanced": {
                "Monday": "System design",
                "Tuesday": "Authentication & security",
                "Wednesday": "Scalable backend",
                "Thursday": "Performance optimization",
                "Friday": "Production-level project",
                "Saturday": "Code refactoring",
                "Sunday": "Portfolio polishing"
            }
        }
    }

    plan = weekly_plans.get(career, {}).get(level, {})

    return render_template(
        'weekly_plan.html',
        career=career,
        level=level,
        plan=plan
    )

@app.route('/advanced-features')
def advanced_features():
    return render_template('advanced_features.html')
@app.route('/skill-progress')
def skill_progress():
    previous_score = 40
    current_score = 65

    improvement = current_score - previous_score

    return render_template(
        'skill_progress.html',
        previous=previous_score,
        current=current_score,
        improvement=improvement
    )
@app.route('/resume-ats')
def resume_ats():
    return render_template('resume_ats.html')


@app.route('/resume-ats-result', methods=['POST'])
def resume_ats_result():
    resume_text = request.form.get('resume').lower()

    skills = ['python', 'sql', 'html', 'css', 'javascript', 'flask']

    matched = []
    missing = []

    for skill in skills:
        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(skills)) * 100)

    return render_template(
        'resume_ats_result.html',
        score=score,
        matched=matched,
        missing=missing
    )
@app.route('/mock-interview', methods=['GET', 'POST'])
def mock_interview():
    career = request.args.get('career', 'AI Engineer')
    q_index = int(request.args.get('q', 0))
    show_feedback = request.args.get('feedback') == 'true'

    interview_questions = {
        "AI Engineer": [
            "What is the difference between supervised and unsupervised learning?",
            "Explain overfitting and underfitting.",
            "What is a neural network?",
            "Difference between classification and regression?",
            "What is backpropagation?"
        ],
        "Data Analyst": [
            "How do you handle missing values in a dataset?",
            "What is data normalization?",
            "Difference between mean and median?",
            "Explain SQL JOINs.",
            "What is data visualization?"
        ],
        "Full Stack Developer": [
            "What is the difference between frontend and backend?",
            "Explain REST APIs.",
            "What is MVC architecture?",
            "Difference between SQL and NoSQL?",
            "What is responsive web design?"
        ]
    }

    questions = interview_questions.get(career)
    question = questions[q_index]

    # When answer is submitted
    if request.method == 'POST':
        answer = request.form.get('answer')

        if len(answer) >= 30:
            session['feedback'] = "Good answer. Your explanation is clear."
        else:
            session['feedback'] = "Answer is too short. Please explain in more detail."

        session['answered'] = True

    feedback = session.get('feedback')
    answered = session.get('answered', False)

    next_q = q_index + 1 if q_index < len(questions) - 1 else None

    return render_template(
        'mock_interview.html',
        career=career,
        question=question,
        q_index=q_index,
        feedback=feedback,
        show_feedback=show_feedback,
        answered=answered,
        next_q=next_q
    )

   
@app.route('/certifications')
def certifications():
    certifications = [
        "Google Data Analytics Professional Certificate",
        "IBM AI Engineering Professional Certificate",
        "AWS Certified Developer – Associate",
        "Meta Front-End Developer Certificate"
    ]

    return render_template(
        'certifications.html',
        certifications=certifications
    )


# -------------------------------------------------
# RUN APP
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)