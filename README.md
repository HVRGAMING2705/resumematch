# ResumeMatch — Resume–Job Match Scorer

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

TF-IDF (word unigrams, sublinear TF, L2) + cosine similarity between a resume and a job description, plus matched/missing skill extraction from a 58-skill list. Trained on 12 hand-written job descriptions and 12 matched sample resumes (486 vocabulary words, seed 42).

- Matched pairs: mean cosine 0.509 vs mismatched pairs 0.056 (9.0x gap)
- Top-1 job retrieval: 12/12 resumes matched to their correct job
- Live demo: https://resumematch-orcin.vercel.app (runs fully in the browser — no backend)
- `train.py` builds the model and writes `model.json`; `index.html` applies the same TF-IDF weights in JavaScript.
