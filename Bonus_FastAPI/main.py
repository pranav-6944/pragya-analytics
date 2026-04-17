import os, warnings
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE  = os.path.dirname(os.path.abspath(__file__))
FILE  = os.path.join(BASE, '..', 'Dataset', 'University_Management_Curation_Project.xlsx')

app = FastAPI(title="PRAGYA — University Academic Analytics")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DIST = os.path.join(BASE, "static", "dist")
app.mount("/assets", StaticFiles(directory=os.path.join(DIST,"assets")), name="assets")

# ── Global model store ────────────────────────────────────────────────────────
G = {}

def grade_std(g):
    gmap = {'A':4.0,'B':3.0,'C':2.0,'D':1.0,'F':0.0,'P':4.0}
    s = str(g).strip().upper().replace('+','').replace('-','')
    if s in gmap: return gmap[s]
    try: v=float(s); return min(v/25,4.0) if v>4 else v
    except: return np.nan

def build_df():
    xl          = pd.ExcelFile(FILE)
    students    = xl.parse('students')
    courses     = xl.parse('courses')
    enrollments = xl.parse('enrollments')
    attendance  = xl.parse('attendance')
    grades      = xl.parse('grades')
    grades['gpa']  = grades['grade'].apply(grade_std)
    grades['gpa']  = grades.groupby('course_id')['gpa'].transform(lambda x: x.fillna(x.median()))
    grades['gpa']  = grades['gpa'].fillna(2.0)
    grades['pass'] = (grades['gpa'] >= 1.0).astype(int)

    attendance['present'] = attendance['status'].apply(
        lambda x: 1 if str(x).lower().strip() in ['present','late','p'] else 0)
    att = attendance.groupby('student_id').agg(
        total=('present','count'), attended=('present','sum')).reset_index()
    att['att_pct'] = att['attended'] / att['total'] * 100

    courses['credits'] = pd.to_numeric(courses['credits'], errors='coerce').fillna(3)
    enr = enrollments.merge(courses[['course_id','credits']], on='course_id', how='left')
    ef  = enrollments.merge(courses[['course_id','faculty_id']], on='course_id', how='left')

    s_gpa  = grades.groupby('student_id')['gpa'].mean().reset_index().rename(columns={'gpa':'GPA'})
    s_pass = grades.groupby('student_id')['pass'].mean().reset_index().rename(columns={'pass':'pass_rate'})
    s_load = enr.groupby('student_id')['credits'].sum().reset_index().rename(columns={'credits':'course_load'})
    s_fac  = ef.groupby('student_id')['faculty_id'].nunique().reset_index().rename(columns={'faculty_id':'fac_int'})

    df = students[['student_id']].copy()
    for g in [s_gpa, s_pass, att[['student_id','att_pct']], s_load, s_fac]:
        df = df.merge(g, on='student_id', how='left')
    for c in ['GPA','pass_rate','att_pct','course_load','fac_int']:
        df[c] = df[c].fillna(df[c].median())
    df['internal_marks'] = df['GPA'] * 25
    df['result'] = df['internal_marks'].apply(
        lambda m: 'Distinction' if m>=75 else ('Pass' if m>=40 else 'Fail'))

    # Clustering
    X_km = StandardScaler().fit_transform(df[['GPA','att_pct','course_load','pass_rate']])
    km = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['cluster'] = km.fit_predict(X_km)
    cl_gpa = df.groupby('cluster')['GPA'].mean().sort_values(ascending=False)
    seg_map = {cl_gpa.index[0]:'High Achievers', cl_gpa.index[1]:'Average Performers',
               cl_gpa.index[2]:'Struggling Students', cl_gpa.index[3]:'At-Risk Students'}
    df['segment'] = df['cluster'].map(seg_map)

    # Dept performance
    grade_dept = grades.merge(courses[['course_id','department_id']], on='course_id', how='left')
    dept = grade_dept.groupby('department_id').agg(
        avg_gpa=('gpa','mean'), pass_rate=('pass','mean'), count=('student_id','nunique')).reset_index()
    dept['pass_pct'] = (dept['pass_rate']*100).round(1)
    dept['avg_gpa']  = dept['avg_gpa'].round(3)

    # Course difficulty
    cs = grades.merge(courses[['course_id','credits']], on='course_id', how='left')
    ca = cs.groupby('course_id').agg(avg_gpa=('gpa','mean'), pass_rate=('pass','mean'),
                                      credits=('credits','mean'), count=('student_id','nunique')).reset_index()
    ca['difficulty'] = ((1-ca['pass_rate'])*ca['credits']).round(3)
    ca['pass_pct']   = (ca['pass_rate']*100).round(1)

    return df, dept, ca

def train_models(df):
    FEATS = ['att_pct','internal_marks','course_load','pass_rate','fac_int']
    le = LabelEncoder()
    y  = le.fit_transform(df['result'])
    X  = df[FEATS]
    Xtr,Xte,ytr,yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(Xtr, ytr)

    df['dropout'] = ((df['GPA']<1.5)|(df['att_pct']<50)).astype(int)
    sc = MinMaxScaler()
    X_ann = sc.fit_transform(df[FEATS])
    Xa,Xb,ya,yb = train_test_split(X_ann, df['dropout'], test_size=0.2, random_state=42, stratify=df['dropout'])
    ann = MLPClassifier(hidden_layer_sizes=(128,64,32), activation='relu', solver='adam', max_iter=200, random_state=42)
    ann.fit(Xa, ya)
    return rf, ann, le, sc, FEATS

import threading

def background_load():
    print("Loading data & training models in background...")
    try:
        df, dept, ca = build_df()
        rf, ann, le, sc, FEATS = train_models(df)
        G.update(dict(df=df, dept=dept, ca=ca, rf=rf, ann=ann, le=le, sc=sc, FEATS=FEATS))
        print("Ready.")
    except Exception as e:
        print("Error during background load:", e)

@app.on_event("startup")
async def startup():
    # Start training in a background thread so the port binds instantly
    threading.Thread(target=background_load, daemon=True).start()

# ── API Router (registered before the SPA catch-all) ─────────────────────────
api = APIRouter(prefix="/api")

@api.get("/overview")
async def api_overview():
    if 'df' not in G:
        return {"error": "Models are still training in the background. Please wait ~30 seconds and refresh."}
    
    df = G['df']
    rc = df['result'].value_counts().to_dict()
    sc = df['segment'].value_counts().to_dict()
    gpa_hist, gpa_bins = np.histogram(df['GPA'], bins=30)
    att_hist, att_bins = np.histogram(df['att_pct'], bins=30)
    return {
        "total_students"  : int(len(df)),
        "avg_gpa"         : round(float(df['GPA'].mean()), 3),
        "avg_attendance"  : round(float(df['att_pct'].mean()), 1),
        "at_risk"         : int(((df['GPA']<1.5)|(df['att_pct']<50)).sum()),
        "distinctions"    : int((df['internal_marks']>=75).sum()),
        "pass_count"      : int(((df['internal_marks']>=40)&(df['internal_marks']<75)).sum()),
        "fail_count"      : int((df['internal_marks']<40).sum()),
        "result_counts"   : rc,
        "segment_counts"  : sc,
        "gpa_hist"        : {"values": gpa_hist.tolist(), "bins": [round(b,2) for b in gpa_bins.tolist()]},
        "att_hist"        : {"values": att_hist.tolist(), "bins": [round(b,1) for b in att_bins.tolist()]},
    }

@api.get("/scatter")
async def api_scatter():
    if 'df' not in G: return {"error": "Models are loading, please wait."}
    df = G['df']
    sample = df.sample(min(1500, len(df)), random_state=42)
    return {
        "attendance" : sample['att_pct'].round(1).tolist(),
        "gpa"        : sample['GPA'].round(3).tolist(),
        "result"     : sample['result'].tolist(),
        "segment"    : sample['segment'].tolist(),
    }

@api.get("/departments")
async def api_departments():
    if 'dept' not in G: return {"error": "Models are loading, please wait."}
    dept = G['dept'].sort_values('avg_gpa', ascending=False).head(15)
    return {
        "ids"        : dept['department_id'].tolist(),
        "avg_gpa"    : dept['avg_gpa'].round(3).tolist(),
        "pass_pct"   : dept['pass_pct'].tolist(),
        "count"      : dept['count'].tolist(),
    }

@api.get("/courses")
async def api_courses():
    if 'ca' not in G: return {"error": "Models are loading, please wait."}
    ca = G['ca'].sort_values('difficulty', ascending=False).head(15)
    return {
        "ids"        : ca['course_id'].tolist(),
        "difficulty" : ca['difficulty'].round(3).tolist(),
        "pass_pct"   : ca['pass_pct'].tolist(),
        "count"      : ca['count'].tolist(),
    }

@api.get("/segments")
async def api_segments():
    if 'df' not in G: return {"error": "Models are loading, please wait."}
    df   = G['df']
    cols = ['GPA','att_pct','course_load','pass_rate']
    prof = df.groupby('segment')[cols].mean().round(3).reset_index()
    return {
        "segments"    : prof['segment'].tolist(),
        "avg_gpa"     : prof['GPA'].tolist(),
        "avg_att"     : prof['att_pct'].tolist(),
        "avg_load"    : prof['course_load'].tolist(),
        "avg_passrate": prof['pass_rate'].tolist(),
        "counts"      : df['segment'].value_counts().reindex(prof['segment']).tolist(),
    }

@api.post("/predict")
async def api_predict(request: Request):
    if 'rf' not in G: return {"error": "Models are loading, please wait."}
    body    = await request.json()
    att     = float(body.get('attendance', 75))
    marks   = float(body.get('marks', 60))
    load    = float(body.get('load', 20))
    prate   = float(body.get('pass_rate', 0.8))
    fac     = float(body.get('faculty', 5))

    inp     = np.array([[att, marks, load, prate, fac]])
    rf, ann, le, sc = G['rf'], G['ann'], G['le'], G['sc']

    cls_pred  = int(rf.predict(inp)[0])
    cls_proba = rf.predict_proba(inp)[0].tolist()
    cls_label = le.inverse_transform([cls_pred])[0]

    inp_sc    = sc.transform(inp)
    drop_prob = float(ann.predict_proba(inp_sc)[0][1])
    risk      = "High" if drop_prob>0.6 else ("Medium" if drop_prob>0.3 else "Low")

    return {
        "result"      : cls_label,
        "probabilities": {c: round(p,4) for c,p in zip(le.classes_, cls_proba)},
        "dropout_prob": round(drop_prob, 4),
        "risk_level"  : risk,
        "gpa_estimate": round(marks/25, 2),
    }

app.include_router(api)

# ── Pages ──────────────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react(full_path: str = ""):
    # Don't catch API routes explicitly just in case, though ordering should fix it
    if full_path.startswith("api/") or full_path.startswith("assets/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404)
    index = os.path.join(DIST, "index.html")
    if not os.path.exists(index):
        return JSONResponse({"error": "Frontend not built. Run 'npm run build' in frontend directory."})
    return FileResponse(index)

if __name__ == "__main__":
    import uvicorn
    # Render provides a dynamic PORT environment variable.
    # We default to 8080 for local development if PORT is missing.
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
