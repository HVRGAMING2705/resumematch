import json
m = json.load(open("model.json"))
vocab, idf = m["vocabulary"], m["idf"]
jobs, resumes, skills = m["jobs"], m["resumes"], m["skills"]
mt = m["metrics"]
DOMAIN = "resumematch-orcin.vercel.app"
JS_MODEL = f"""const VOCAB = {json.dumps(vocab)};
const IDF = {json.dumps(idf)};
const SKILLS = {json.dumps(skills)};
function tfidfVec(text){{
  const toks = (text.toLowerCase().match(/[a-z0-9_]{{2,}}/g) || []);
  const counts = {{}};
  toks.forEach(t => {{ if (t in VOCAB) counts[t] = (counts[t] || 0) + 1; }});
  const vals = {{}}; let norm = 0;
  for (const t in counts) {{
    const v = (1 + Math.log(counts[t])) * IDF[VOCAB[t]];
    vals[t] = v; norm += v * v;
  }}
  norm = Math.sqrt(norm);
  if (norm > 0) for (const t in vals) vals[t] /= norm;
  return vals;
}}
function cosine(a, b){{
  let dot = 0;
  for (const t in a) if (t in b) dot += a[t] * b[t];
  return dot;
}}
function skillsIn(text){{
  const t = text.toLowerCase();
  return SKILLS.filter(s => t.indexOf(s) !== -1);
}}
function matchScore(resume, job){{
  const c = cosine(tfidfVec(resume), tfidfVec(job));
  const rs = skillsIn(resume), js = skillsIn(job);
  return {{cosine: c, matched: js.filter(s => rs.indexOf(s) !== -1), missing: js.filter(s => rs.indexOf(s) === -1)}};
}}"""
job_options = "".join(f'<option value="{i}">{j["title"]}</option>' for i, j in enumerate(jobs))
resume_options = "".join(f'<option value="{i}">{r["name"]}</option>' for i, r in enumerate(resumes))
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ResumeMatch — Resume–Job Match Scorer | AI/ML Project</title>
<meta name="description" content="ResumeMatch scores how well a resume fits a job description using TF-IDF and cosine similarity. Paste a resume and a job post, get a match score plus matched and missing skills. Runs fully in your browser.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="ResumeMatch — Resume–Job Match Scorer">
<meta property="og:description" content="Paste a resume and a job description and get an instant match score with matched and missing skills — a real TF-IDF model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="ResumeMatch — Resume–Job Match Scorer">
<meta name="twitter:description" content="TF-IDF + cosine similarity resume–job matcher. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"ResumeMatch","applicationCategory":"EducationalApplication","description":"Resume-job match scorer using TF-IDF and cosine similarity.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:760px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
textarea{{width:100%;padding:10px;font-size:15px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
select{{padding:8px;font-size:15px;border:1px solid #000;border-radius:4px}}
button{{margin-top:16px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b.big{{font-size:2em}}
.tag{{display:inline-block;background:#eee;border:1px solid #000;border-radius:12px;padding:2px 10px;margin:2px;font-size:14px}}
.tag.miss{{background:#fff;color:#900;border-color:#900}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
</style>
</head>
<body>
<h1>&#128196; ResumeMatch — Resume–Job Match Scorer</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A TF-IDF + cosine similarity model trained on 12 job descriptions and 12 sample resumes ({mt['vocab']} words) scores how well a resume fits a job post. Matched pairs score <b>{mt['matched_mean']:.2f} on average</b> vs <b>{mt['mismatched_mean']:.2f}</b> for wrong pairs — a {mt['matched_mean']/mt['mismatched_mean']:.1f}x gap — and the model picks the right job for a resume <b>{mt['top1_count']}/12 times</b>.</p>
<label>Pick a sample resume</label>
<select id="resumePick" onchange="loadResume()">{resume_options}</select>
<label>Your resume</label>
<textarea id="resume" rows="6"></textarea>
<label>Pick a sample job description</label>
<select id="jobPick" onchange="loadJob()">{job_options}</select>
<label>Job description</label>
<textarea id="job" rows="6"></textarea>
<button onclick="score()">Score My Match</button>
<button onclick="loadPair(0,0)">Try the Data Analyst pair</button>
<div id="result"></div>
<p class="note">How it works: both texts are turned into TF-IDF vectors (rare, meaningful words weigh more than common ones), then the cosine similarity between the two vectors is the match score. The page also checks a list of {len(skills)} job skills and shows which ones the resume already has and which ones the job asks for but the resume is missing. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try it: Asha Verma&rsquo;s Data Analyst resume against the Data Analyst job scores about 44%. The same resume against the DevOps Engineer job scores about 2% — and the page lists all 8 DevOps skills as missing. A resume with no real content scores near 0% against any job.</p>
<p><a href="https://github.com/HVRGAMING2705/resumematch">View source on GitHub</a></p>
<script>
{JS_MODEL}
const JOBS = {json.dumps([j["text"] for j in jobs])};
const RESUMES = {json.dumps([r["text"] for r in resumes])};
function loadResume(){{ document.getElementById("resume").value = RESUMES[document.getElementById("resumePick").value]; }}
function loadJob(){{ document.getElementById("job").value = JOBS[document.getElementById("jobPick").value]; }}
function loadPair(r, j){{ document.getElementById("resumePick").value = r; document.getElementById("jobPick").value = j; loadResume(); loadJob(); score(); }}
function verdict(c){{
  if (c >= 0.40) return "Strong match — this resume fits the job well.";
  if (c >= 0.25) return "Decent match — a few key skills are missing.";
  if (c >= 0.10) return "Weak match — the resume and the job barely overlap.";
  return "Poor match — this resume does not fit this job.";
}}
function score(){{
  const r = document.getElementById("resume").value;
  const j = document.getElementById("job").value;
  const out = matchScore(r, j);
  const el = document.getElementById("result");
  el.style.display = "block";
  let html = "<b class=big>Match score: " + (out.cosine * 100).toFixed(1) + "%</b><br><span class=note>" + verdict(out.cosine) + "</span><br><br>";
  html += "<b>Matched skills (" + out.matched.length + "):</b><br>" + (out.matched.length ? out.matched.map(s => "<span class=tag>" + s + "</span>").join("") : "<span class=note>None of the listed job skills appear in the resume.</span>") + "<br><br>";
  html += "<b>Missing skills (" + out.missing.length + "):</b><br>" + (out.missing.length ? out.missing.map(s => "<span class=tag miss>" + s + "</span>").join("") : "<span class=note>None — the resume covers every listed skill.</span>");
  html += "<br><br><span class=note>Demo trained on 12 hand-written job descriptions and resumes; real recruiters weigh much more than keywords.</span>";
  el.innerHTML = html;
}}
loadPair(0, 0);
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — ResumeMatch</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on ResumeMatch.</p><p><a href="https://{DOMAIN}/">Back to ResumeMatch</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>
""")
open("README.md", "w").write(f"""# ResumeMatch — Resume–Job Match Scorer

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

TF-IDF (word unigrams, sublinear TF, L2) + cosine similarity between a resume and a job description, plus matched/missing skill extraction from a {len(skills)}-skill list. Trained on 12 hand-written job descriptions and 12 matched sample resumes ({mt['vocab']} vocabulary words, seed 42).

- Matched pairs: mean cosine {mt['matched_mean']:.3f} vs mismatched pairs {mt['mismatched_mean']:.3f} ({mt['matched_mean']/mt['mismatched_mean']:.1f}x gap)
- Top-1 job retrieval: {mt['top1_count']}/12 resumes matched to their correct job
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` builds the model and writes `model.json`; `index.html` applies the same TF-IDF weights in JavaScript.
""")
samples = json.load(open("parity_samples.json"))
parity = JS_MODEL + "\n" + "\n".join(
    f"console.log(JSON.stringify({{cosine: matchScore({json.dumps(s['resume'])}, {json.dumps(s['job'])}).cosine, matched: matchScore({json.dumps(s['resume'])}, {json.dumps(s['job'])}).matched, missing: matchScore({json.dumps(s['resume'])}, {json.dumps(s['job'])}).missing, py_cosine: {s['cosine']}, py_matched: {json.dumps(s['matched'])}, py_missing: {json.dumps(s['missing'])}}}));"
    for s in samples)
open("parity.js", "w").write(parity)
print("site files written, matched", round(mt['matched_mean'], 3), "top1", mt['top1_count'], "/12")
