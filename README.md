# 🎓 AI Adaptive Study Material Recommender System

## 📌 Project Description
An intelligent study material recommender system built with Python.
It recommends videos, notes, and practice problems based on the
student's subject, difficulty preference, and material type.
The system LEARNS from user ratings to improve future recommendations.

## 🧠 AI/ML Concepts Used
- **Intelligent Agent** – Agent perceives, acts, and learns
- **Search Strategy** – Constraint-based filtering of materials
- **Heuristic Ranking** – Score-based ranking formula
- **Adaptive Learning** – Score updates based on user ratings

## 🛠️ Technologies Used
- Python 3.x
- Pandas
- CSV (for data storage)

## 📁 Folder Structure
```
study_recommender/
├── data/
│   ├── materials.csv       ← Study material dataset (30 entries)
│   └── feedback.csv        ← Auto-filled by program when you rate
├── agent.py                ← Intelligent Agent logic
├── recommender.py          ← Search + Heuristic Ranking
├── feedback.py             ← Adaptive Learning from ratings
├── main.py                 ← Main program (run this!)
├── utils.py                ← Helper functions
└── README.md               ← This file
```

## 🚀 How to Run

### Step 1 — Install requirement
```bash
pip install pandas
```

### Step 2 — Run the program
```bash
python main.py
```

## 📊 Ranking Formula
```
Final Score  = adaptive_score × difficulty_weight × type_weight
adaptive_score = (base_score + Σ ratings) / (1 + N)

difficulty_weight: Easy=1.0, Medium=1.1, Hard=1.2
type_weight:       Video=1.0, Notes=1.05, Practice=1.1
```

## 📚 Available Subjects
- Python
- Math
- DSA
- AI

## 🎯 Difficulty Levels
- Easy
- Medium
- Hard

## 📂 Material Types
- Video
- Notes
- Practice

## 💡 How Adaptive Learning Works
1. All materials start with base_score = 3.5
2. When you rate a material, the score is recalculated
3. High ratings → score goes UP → ranked higher next time
4. Low ratings  → score goes DOWN → ranked lower next time

## 👨‍💻 Author
Sayan Mondal
B.Tech CSE(AIML), 1st Year
VIT Bhopal University

## 📅 Submitted For
-AI/ML Course Project
-Registration no. 25BAI11532
