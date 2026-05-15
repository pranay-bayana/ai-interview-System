"""
Database initialization and connection management for AI Recruitment Ecosystem
JSON-Based Persistent Mock Database for Demo Environment
"""

import os
import json
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client
from unittest.mock import MagicMock

load_dotenv()

DB_FILE = os.path.join(os.path.dirname(__file__), 'mock_db.json')

def load_json_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {
        'users': [{'id': 1, 'email': 'test@example.com', 'full_name': 'Test Candidate', 'role': 'candidate', 'password_hash': 'ef92b778bafe421e592022c3912c77b2861f06e8edfc70371d24d317b560127a'}],
        'candidate_scores': [{'user_id': 1, 'round1_score': 0, 'round2_score': 0, 'round3_score': 0, 'round4_score': 0, 'round5_score': 0}],
        'candidate_status': [{'user_id': 1, 'status': 'pending', 'current_round': 0}],
        'aptitude_answers': [],
        'technical_answers': [],
        'coding_submissions': [],
        'hr_voice_transcriptions': [],
        'resumes': []
    }

def save_json_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class DatabaseManager:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://mock.supabase.co')
        self.supabase_key = os.getenv('SUPABASE_KEY', 'mock-key')
        self._client = None

    @property
    def client(self):
        if self._client: return self._client
            
        try:
            is_real = self.supabase_url and 'your_project_url' not in self.supabase_url
            if is_real:
                self._client = create_client(self.supabase_url, self.supabase_key)
                return self._client
        except Exception: pass
            
        # Persistent JSON Mock
        mock_client = MagicMock()
        
        def get_table_mock(table_name):
            table_mock = MagicMock()
            filters = {'user_id': None, 'email': None, 'password_hash': None}
            
            def eq_side_effect(col, val):
                filters[col] = val
                return table_mock
            
            table_mock.select.return_value = table_mock
            table_mock.update.return_value = table_mock
            table_mock.eq.side_effect = eq_side_effect
            
            def execute_mock():
                db_data = load_json_db()
                data = db_data.get(table_name, [])
                
                if filters['user_id']:
                    data = [d for d in data if d.get('user_id') == filters['user_id'] or d.get('id') == filters['user_id']]
                if filters['email']:
                    data = [d for d in data if d.get('email', '').lower() == filters['email'].lower()]
                if filters['password_hash']:
                    data = [d for d in data if d.get('password_hash') == filters['password_hash']]
                    
                res = MagicMock()
                res.data = data
                return res
            
            table_mock.execute.side_effect = execute_mock
            
            def insert_side_effect(row):
                db_data = load_json_db()
                if table_name not in db_data: db_data[table_name] = []
                
                if 'id' not in row and table_name not in ['candidate_scores', 'candidate_status']:
                    row['id'] = len(db_data[table_name]) + 1
                
                db_data[table_name].append(row)
                save_json_db(db_data)
                
                ret = MagicMock()
                ret.execute.return_value.data = [row]
                return ret
            table_mock.insert.side_effect = insert_side_effect
            
            def update_side_effect(new_data):
                db_data = load_json_db()
                target_list = db_data.get(table_name, [])
                updated = False
                for item in target_list:
                    match = True
                    if filters['user_id'] and not (item.get('user_id') == filters['user_id'] or item.get('id') == filters['user_id']):
                        match = False
                    if match:
                        item.update(new_data)
                        updated = True
                
                if updated: save_json_db(db_data)
                ret = MagicMock()
                ret.execute.return_value.data = []
                return ret
            table_mock.update.side_effect = update_side_effect
            
            return table_mock

        mock_client.table.side_effect = get_table_mock
        self._client = mock_client
        return self._client

_instance = DatabaseManager()
def get_db(): return _instance
