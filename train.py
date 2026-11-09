import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 12 job descriptions (hand-written, ~60-90 words each)
JOBS = [
 ("Data Analyst",
  "We are hiring a Data Analyst to turn raw data into clear business insights. You will write SQL queries to pull data from databases, clean and analyse datasets in Python using pandas, and build dashboards in Excel and Power BI. You should understand basic statistics, create charts that explain trends, and present findings to managers. Experience with data cleaning, pivot tables, and storytelling with data is required. A degree in computer science or statistics is preferred."),
 ("Frontend Developer",
  "We need a Frontend Developer to build fast and beautiful web pages. You will write clean HTML, CSS and JavaScript, and build interactive user interfaces with React. You should know responsive design, flexbox, and how to fetch data from REST APIs. Experience with Git, Tailwind CSS and debugging in the browser is expected. You will work with designers to turn Figma mockups into working pages and make sure the site works well on phones and desktops."),
 ("Backend Developer",
  "We are looking for a Backend Developer to build the server side of our web applications. You will design REST APIs in Python or Node.js, work with PostgreSQL databases, write clean and tested code, and deploy services with Docker. You should understand authentication, caching, and database indexing. Experience with Git, Linux servers, and writing unit tests is required. You will work with frontend developers to ship features reliably."),
 ("Machine Learning Engineer",
  "We are hiring a Machine Learning Engineer to build and deploy predictive models. You will train models with scikit-learn and TensorFlow, clean and prepare datasets, and evaluate models with proper metrics. You should know Python, NumPy, pandas, and the basics of deep learning and natural language processing. Experience with model deployment, version control with Git, and working with large datasets is expected. A strong grasp of statistics and linear algebra helps."),
 ("UI/UX Designer",
  "We need a UI/UX Designer to design simple and delightful product experiences. You will create wireframes and prototypes in Figma, run user research interviews, and test designs with real users. You should understand colour, typography, layout and accessibility. Experience with design systems, user flows, and presenting design decisions is required. You will work closely with developers to make sure the final product matches your designs."),
 ("DevOps Engineer",
  "We are hiring a DevOps Engineer to keep our systems running smoothly. You will manage cloud infrastructure on AWS, write Docker containers, set up Kubernetes clusters, and build CI/CD pipelines with GitHub Actions. You should know Linux, shell scripting, and monitoring tools. Experience with infrastructure as code, automated testing, and handling production incidents is expected. You will help developers ship code faster and safer."),
 ("Digital Marketer",
  "We need a Digital Marketer to grow our online presence. You will run Google Ads and social media campaigns, improve our SEO rankings, and analyse traffic with Google Analytics. You should know keyword research, content planning, email marketing and A/B testing. Experience with Meta Ads, Canva, and writing ad copy is expected. You will track results every week and suggest ideas to bring in more customers at a lower cost."),
 ("Content Writer",
  "We are hiring a Content Writer to create clear and engaging articles. You will write blog posts, website pages and social media captions, research topics, and edit your own work for grammar and clarity. You should know SEO writing, keyword placement, and how to write catchy headlines. Experience with WordPress, Google Docs, and meeting deadlines is expected. You will work with the marketing team to plan a monthly content calendar."),
 ("QA Tester",
  "We need a QA Tester to make sure our software works correctly before release. You will write test cases, run manual testing on web and mobile apps, report bugs clearly, and retest fixes. You should know Selenium for automation, basic SQL, and how to use bug tracking tools like Jira. Experience with test planning, regression testing, and working in agile teams is expected. Attention to detail is essential for this role."),
 ("Cybersecurity Analyst",
  "We are hiring a Cybersecurity Analyst to protect our systems from attacks. You will monitor networks, investigate security alerts, check firewalls, and run vulnerability scans. You should know networking basics, Linux, and how phishing and malware work. Experience with penetration testing tools, SIEM dashboards, and writing incident reports is expected. You will help the team respond quickly when a security incident happens."),
 ("Product Manager",
  "We need a Product Manager to guide our product from idea to launch. You will talk to users, write product requirements, plan roadmaps, and work with engineers and designers in agile sprints. You should know prioritisation, A/B testing, and basic data analysis. Experience with Jira, Figma, and presenting to stakeholders is expected. You will measure success with clear metrics and keep the whole team aligned on what to build next."),
 ("Data Scientist",
  "We are hiring a Data Scientist to solve business problems with data. You will explore large datasets, build machine learning models, and communicate results through clear visualisations. You should know Python, statistics, scikit-learn, and SQL, and have experience with A/B testing and experimental design. Experience with TensorFlow, data visualisation in matplotlib, and presenting to non-technical teams is expected. Strong problem solving skills are essential."),
]

# 12 sample resumes, each matched to the job above with the same index
RESUMES = [
 ("Asha Verma — Data Analyst",
  "Asha Verma, B.Tech Computer Science. Skills: Python, SQL, Excel, Power BI, pandas, statistics. Projects: analysed 10,000 sales records with pandas, cleaned messy data, built a Power BI dashboard showing monthly trends, wrote SQL queries with joins and pivot tables. Internship: prepared weekly reports and charts for managers, used data cleaning and storytelling with data to explain customer trends. Looking for a data analyst role."),
 ("Rahul Mehta — Frontend Developer",
  "Rahul Mehta, B.Tech IT. Skills: HTML, CSS, JavaScript, React, Tailwind CSS, Git, REST APIs. Projects: built a responsive portfolio website with React, created a weather app that fetches data from REST APIs, turned Figma mockups into working pages. Experience with flexbox, responsive design, browser debugging and Git. Looking for a frontend developer role building fast and beautiful web pages."),
 ("Priya Nair — Backend Developer",
  "Priya Nair, B.Tech Computer Science. Skills: Python, Node.js, PostgreSQL, Docker, REST APIs, Linux, Git. Projects: built REST APIs with authentication, designed a PostgreSQL database with indexing, deployed services with Docker, wrote unit tests. Experience with caching, clean code, and Linux servers. Looking for a backend developer role building reliable server side applications."),
 ("Arjun Rao — Machine Learning Engineer",
  "Arjun Rao, B.Tech AI and ML. Skills: Python, TensorFlow, scikit-learn, NumPy, pandas, NLP, statistics. Projects: trained a spam classifier with scikit-learn, built an image classifier with TensorFlow, cleaned large datasets, evaluated models with precision and recall. Experience with deep learning, natural language processing, Git and model deployment. Looking for a machine learning engineer role."),
 ("Sneha Kulkarni — UI/UX Designer",
  "Sneha Kulkarni, B.Des Communication Design. Skills: Figma, wireframes, prototyping, user research, design systems. Projects: redesigned a college app with wireframes and prototypes in Figma, ran user research interviews, tested designs with real users, created a design system with colour and typography rules. Experience with user flows, accessibility and presenting design decisions. Looking for a UI/UX designer role."),
 ("Vikram Singh — DevOps Engineer",
  "Vikram Singh, B.Tech Computer Science. Skills: AWS, Docker, Kubernetes, Linux, CI/CD, GitHub Actions, shell scripting. Projects: set up a CI/CD pipeline with GitHub Actions, containerised an app with Docker, managed a Kubernetes cluster, wrote shell scripts for automation. Experience with cloud infrastructure, monitoring tools, infrastructure as code and handling production incidents. Looking for a DevOps engineer role."),
 ("Kavya Reddy — Digital Marketer",
  "Kavya Reddy, BBA Marketing. Skills: SEO, Google Ads, Google Analytics, social media, Meta Ads, Canva, email marketing. Projects: ran a Google Ads campaign that cut cost per click by 30 percent, improved SEO rankings with keyword research, planned content and ran A/B testing on landing pages. Experience with ad copy, analytics and tracking results every week. Looking for a digital marketer role."),
 ("Rohan Gupta — Content Writer",
  "Rohan Gupta, BA English. Skills: SEO writing, blogging, editing, WordPress, Google Docs, research. Projects: wrote 40 blog posts on technology, improved article rankings with keyword placement, edited articles for grammar and clarity, wrote catchy headlines and social media captions. Experience with content calendars, meeting deadlines, and working with marketing teams. Looking for a content writer role."),
 ("Ananya Iyer — QA Tester",
  "Ananya Iyer, B.Tech Computer Science. Skills: manual testing, Selenium, test cases, Jira, SQL, regression testing. Projects: wrote 200 test cases for a web app, ran manual testing on web and mobile apps, reported bugs clearly in Jira, automated login tests with Selenium. Experience with test planning, retesting fixes, and working in agile teams. Looking for a QA tester role."),
 ("Karthik Menon — Cybersecurity Analyst",
  "Karthik Menon, B.Tech Computer Science. Skills: networking, Linux, firewalls, penetration testing, SIEM, vulnerability scanning. Projects: ran vulnerability scans on a lab network, investigated phishing emails and malware samples, configured firewalls, wrote incident reports. Experience with security alerts, monitoring tools and penetration testing. Looking for a cybersecurity analyst role."),
 ("Divya Sharma — Product Manager",
  "Divya Sharma, B.Tech + MBA. Skills: roadmaps, agile, Jira, Figma, A/B testing, stakeholder management, data analysis. Projects: led a student team building a campus app, wrote product requirements, planned sprints, talked to users and prioritised features, presented to stakeholders. Experience with metrics, prioritisation and keeping teams aligned. Looking for a product manager role."),
 ("Nikhil Joshi — Data Scientist",
  "Nikhil Joshi, B.Tech AI and ML. Skills: Python, statistics, scikit-learn, SQL, TensorFlow, matplotlib, A/B testing. Projects: built a churn prediction model, ran A/B testing on a website experiment, explored large datasets and presented results with clear visualisations. Experience with machine learning models, experimental design and communicating to non-technical teams. Looking for a data scientist role."),
]

SKILLS = [
 "python", "sql", "excel", "power bi", "pandas", "statistics", "data cleaning",
 "html", "css", "javascript", "react", "tailwind css", "rest apis", "figma",
 "node.js", "postgresql", "docker", "git", "linux", "unit tests",
 "tensorflow", "scikit-learn", "numpy", "nlp", "deep learning",
 "wireframes", "prototyping", "user research", "design systems",
 "aws", "kubernetes", "ci/cd", "github actions", "shell scripting",
 "seo", "google ads", "google analytics", "social media", "meta ads", "canva",
 "email marketing", "blogging", "editing", "wordpress",
 "manual testing", "selenium", "test cases", "jira", "regression testing",
 "networking", "firewalls", "penetration testing", "siem",
 "roadmaps", "agile", "a/b testing", "machine learning", "data visualisation",
]

job_texts = [j[1] for j in JOBS]
resume_texts = [r[1] for r in RESUMES]
all_docs = job_texts + resume_texts
vec = TfidfVectorizer(sublinear_tf=True, lowercase=True)
X = vec.fit_transform(all_docs)
Xj = X[:12]
Xr = X[12:]
sims = cosine_similarity(Xr, Xj)  # sims[i][j] = resume i vs job j
matched = [float(sims[i][i]) for i in range(12)]
mismatched = [float(sims[i][j]) for i in range(12) for j in range(12) if i != j]
top1 = sum(1 for i in range(12) if int(np.argmax(sims[i])) == i)
print(f"n_jobs=12 n_resumes=12 vocab={len(vec.vocabulary_)}")
print(f"matched mean cosine={np.mean(matched):.3f} range {min(matched):.3f}-{max(matched):.3f}")
print(f"mismatched mean cosine={np.mean(mismatched):.3f} range {min(mismatched):.3f}-{max(mismatched):.3f}")
print(f"top-1 retrieval accuracy: {top1}/12 = {top1/12:.1%}")
print(f"lift: matched/mismatched = {np.mean(matched)/np.mean(mismatched):.1f}x")

def skills_in(text):
    t = text.lower()
    return [s for s in SKILLS if s in t]

def py_score(resume, job):
    v = vec.transform([resume, job])
    c = float(cosine_similarity(v[0], v[1])[0][0])
    rs, js = skills_in(resume), skills_in(job)
    matched_sk = [s for s in js if s in rs]
    missing_sk = [s for s in js if s not in rs]
    return c, matched_sk, missing_sk

# parity samples: matched pair, cross pair, strong resume vs wrong job, near-empty resume
pairs = [
 (RESUMES[0][1], JOBS[0][1]),   # matched Data Analyst
 (RESUMES[3][1], JOBS[3][1]),   # matched ML Engineer
 (RESUMES[0][1], JOBS[5][1]),   # data analyst resume vs DevOps job
 (RESUMES[6][1], JOBS[6][1]),   # matched Digital Marketer
 (RESUMES[11][1], JOBS[11][1]), # matched Data Scientist
 ("I am a student with no experience yet.", JOBS[1][1]),  # near-empty resume
]
samples = []
for r, j in pairs:
    c, msk, miss = py_score(r, j)
    samples.append({"resume": r, "job": j, "cosine": c,
                    "matched": msk, "missing": miss})
    print(f"cos={c:.4f} matched_skills={msk} missing={miss}")
with open("parity_samples.json", "w") as f:
    json.dump(samples, f, indent=1)

mj = {"vocabulary": vec.vocabulary_, "idf": vec.idf_.tolist(),
      "jobs": [{"title": t, "text": d} for t, d in JOBS],
      "resumes": [{"name": n, "text": d} for n, d in RESUMES],
      "skills": SKILLS,
      "metrics": {"matched_mean": float(np.mean(matched)),
                  "mismatched_mean": float(np.mean(mismatched)),
                  "top1_accuracy": top1 / 12, "top1_count": top1,
                  "n_jobs": 12, "n_resumes": 12, "vocab": len(vec.vocabulary_),
                  "matched_range": [min(matched), max(matched)],
                  "mismatched_range": [min(mismatched), max(mismatched)]}}
with open("model.json", "w") as f:
    json.dump(mj, f, indent=1)
print("model.json written")
