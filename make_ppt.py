from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "resumematch-orcin.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "ResumeMatch — Resume–Job Match Scorer", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "Paste a resume and a job description — get a match score plus the skills you have and the ones you are missing"])
add(1, "The Problem", ["Job seekers send the same resume to every job and hear nothing back", "Recruiters skim hundreds of resumes and miss good candidates", "Nobody tells the applicant which skills are missing for a role", "A quick, honest match score would save time on both sides"])
add(2, "The Solution — ResumeMatch", ["Paste any resume and any job description into the browser demo", "The model returns a match score from 0% to 100% in a second", "It also lists matched skills and the skills the job needs but the resume lacks", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset and model training", "TF-IDF (word unigrams, sublinear TF, L2 normalisation) + cosine similarity", "A 58-skill checklist for matched vs missing skill extraction", "HTML, CSS and vanilla JavaScript for the interactive demo; GitHub + Vercel for hosting"])
add(4, "Architecture", ["Dataset: 12 hand-written job descriptions + 12 matched sample resumes, 486-word vocabulary", "Text -> tokens -> TF-IDF weights -> L2-normalised vectors -> cosine similarity", "model.json ships with the site; JavaScript applies the same formula in the browser", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: pick a sample resume and job, or paste your own, then press Score My Match", "Asha Verma's Data Analyst resume vs the Data Analyst job: 44.3% — strong match", "Same resume vs the DevOps Engineer job: 2.2% — and all 8 DevOps skills shown as missing", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["Matched resume–job pairs: mean cosine 0.509 vs 0.056 for wrong pairs — a 9.0x gap", "Top-1 job retrieval: 12 out of 12 resumes matched to their correct job (100%)", "A resume with no real content scores near 0% against any job — the model is honest", "Browser demo matches Python cosine exactly on all test samples"])
add(7, "Future Scope", ["Score a resume against many jobs at once and rank the best fits", "Add a real resume dataset and support PDF uploads", "Suggest courses or projects to close the missing-skill gaps", "Add more roles and support Telugu and Hindi resumes"])
add(8, "Thank You", ["ResumeMatch — Resume–Job Match Scorer", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/resumematch", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_ResumeMatch_2026-11-09.pptx")
print("slides:", len(prs.slides._sldIdLst))
