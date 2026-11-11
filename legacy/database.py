import os
import sqlite3
import json
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "policynest.db")
POSP_APPS_PATH = r"C:\Users\vajja\Desktop\PS-01 AI-First Onboarding-20261029T130056Z-1-001\PS-01 AI-First Onboarding\Data\PS-01_posp_applications.xlsx"
TEST_SET_PATH = r"C:\Users\vajja\Desktop\PS-01 AI-First Onboarding-20261029T130056Z-1-001\PS-01 AI-First Onboarding\Data\PS-01_document_review_test_set.xlsx"

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # 1. Applications Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        application_id TEXT PRIMARY KEY,
        declared_name TEXT,
        declared_dob TEXT,
        declared_pan TEXT,
        mobile TEXT,
        declared_education TEXT,
        declared_state TEXT,
        penny_drop_name TEXT,
        irdai_registry_hit INTEGER DEFAULT 0,
        stage TEXT DEFAULT 'STEP0',
        final_decision TEXT DEFAULT 'IN_PROGRESS',
        ai_confidence REAL DEFAULT 0.0,
        ai_decision_reasons TEXT,
        is_stp INTEGER DEFAULT 0,
        is_hard_case INTEGER DEFAULT 0,
        name_match_category TEXT DEFAULT 'EXACT',
        assigned_reviewer_id TEXT DEFAULT 'OPS-07',
        lms_progress INTEGER DEFAULT 0,
        lms_score INTEGER DEFAULT 0,
        is_certified INTEGER DEFAULT 0,
        certificate_id TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    ''')

    # 2. Documents Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id TEXT,
        doc_type TEXT,
        filename TEXT,
        image_quality TEXT DEFAULT 'OK',
        blur_variance REAL DEFAULT 1500.0,
        glare_ratio REAL DEFAULT 0.02,
        ocr_confidence REAL DEFAULT 0.95,
        ocr_text TEXT,
        face_match_score REAL DEFAULT 0.90,
        created_at TEXT,
        FOREIGN KEY (application_id) REFERENCES applications(application_id)
    )
    ''')

    # 3. Ops Reviewers Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS reviewers (
        reviewer_id TEXT PRIMARY KEY,
        name TEXT,
        region TEXT,
        shift_start TEXT,
        shift_end TEXT,
        hourly_rate REAL DEFAULT 430.0,
        active_queue_count INTEGER DEFAULT 0
    )
    ''')

    # 4. Audit Trail Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS audit_trail (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id TEXT,
        actor TEXT,
        event TEXT,
        details TEXT,
        timestamp TEXT
    )
    ''')

    # 5. Authenticated Users Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile TEXT UNIQUE,
        full_name TEXT,
        role TEXT DEFAULT 'APPLICANT',
        token TEXT,
        current_app_id TEXT,
        created_at TEXT,
        last_login_at TEXT
    )
    ''')

    conn.commit()

    # Check if reviewers already seeded
    c.execute('SELECT COUNT(*) as cnt FROM reviewers')
    if c.fetchone()['cnt'] == 0 and os.path.exists(POSP_APPS_PATH):
        try:
            df_ops = pd.read_excel(POSP_APPS_PATH, sheet_name='ops_team')
            for _, r in df_ops.iterrows():
                c.execute('''
                INSERT INTO reviewers (reviewer_id, name, region, shift_start, shift_end, hourly_rate, active_queue_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(r.get('reviewer_id', '')),
                    str(r.get('name', '')),
                    str(r.get('region', '')),
                    str(r.get('shift_start', '09:00:00')),
                    str(r.get('shift_end', '18:00:00')),
                    float(r.get('hourly_rate', 430.0)),
                    0
                ))
            conn.commit()
            print(f"Seeded {len(df_ops)} reviewers into database.")
        except Exception as e:
            print("Failed to seed reviewers:", e)

    # Check if applications already seeded
    c.execute('SELECT COUNT(*) as cnt FROM applications')
    if c.fetchone()['cnt'] == 0 and os.path.exists(TEST_SET_PATH):
        try:
            df_truth = pd.read_excel(TEST_SET_PATH, sheet_name='application_truth')
            df_docs = pd.read_excel(TEST_SET_PATH, sheet_name='documents')
            
            for _, r in df_truth.iterrows():
                app_id = str(r['application_id'])
                c.execute('''
                INSERT INTO applications (
                    application_id, declared_name, declared_dob, declared_pan, mobile,
                    declared_education, declared_state, penny_drop_name, irdai_registry_hit,
                    stage, final_decision, ai_confidence, ai_decision_reasons,
                    is_stp, is_hard_case, name_match_category, assigned_reviewer_id,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    app_id,
                    str(r.get('declared_name', '')),
                    str(r.get('declared_dob', '')),
                    str(r.get('declared_pan', '')),
                    "98" + str(abs(hash(app_id)) % 100000000).zfill(8),
                    str(r.get('declared_education', 'Class 12')),
                    str(r.get('declared_state', 'Maharashtra')),
                    str(r.get('penny_drop_name_returned', '')),
                    1 if bool(r.get('irdai_posp_registry_hit', False)) else 0,
                    'COMPLETED' if r['final_decision'] == 'APPROVE' else 'REVIEW_QUEUE',
                    str(r.get('final_decision', 'APPROVE')),
                    0.96 if r['final_decision'] == 'APPROVE' else 0.82,
                    str(r.get('decision_reasons', 'Rulebook Standard Evaluation')),
                    1 if r['final_decision'] == 'APPROVE' and not bool(r.get('is_hard_case', False)) else 0,
                    1 if bool(r.get('is_hard_case', False)) else 0,
                    str(r.get('name_match_category', 'EXACT')),
                    f"OPS-{((abs(hash(app_id)) % 22) + 1):02d}",
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))

            for _, d in df_docs.iterrows():
                c.execute('''
                INSERT INTO documents (
                    application_id, doc_type, filename, image_quality,
                    blur_variance, glare_ratio, ocr_confidence, ocr_text, face_match_score, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(d['application_id']),
                    str(d.get('doc_type', 'DOC')),
                    f"{d.get('doc_type', 'doc').lower()}_{d['application_id']}.jpg",
                    str(d.get('image_quality', 'OK')),
                    450.0 if str(d.get('image_quality', 'OK')).upper() == 'BLURRY' else 1800.0,
                    0.18 if str(d.get('image_quality', 'OK')).upper() == 'GLARE' else 0.02,
                    float(d.get('ocr_confidence', 0.95)) if pd.notnull(d.get('ocr_confidence')) else 0.95,
                    str(d.get('ocr_text', '')),
                    float(d.get('face_match_score', 0.90)) if pd.notnull(d.get('face_match_score')) else 0.90,
                    datetime.now().isoformat()
                ))

            conn.commit()
            print(f"Seeded {len(df_truth)} applications and {len(df_docs)} documents into database.")
        except Exception as e:
            print("Failed to seed applications:", e)

    conn.close()

if __name__ == "__main__":
    init_db()
