-- AI Recruitment Ecosystem Database Schema

-- Users Table (Candidates and Admins)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'candidate', -- 'candidate' or 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Candidate Scores Table
CREATE TABLE IF NOT EXISTS candidate_scores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    round1_score INTEGER DEFAULT 0, -- Resume skills (max 5)
    round2_score INTEGER DEFAULT 0, -- Aptitude (max 5)
    round3_score INTEGER DEFAULT 0, -- Technical (max 10)
    round4_score INTEGER DEFAULT 0, -- Coding (max 10)
    round5_score INTEGER DEFAULT 0, -- HR Voice (max 10)
    total_score INTEGER DEFAULT 0, -- Total (max 40)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Candidate Status Table
CREATE TABLE IF NOT EXISTS candidate_status (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    current_round INTEGER DEFAULT 0, -- 0 = not started, 1-7 = rounds
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'selected', 'hold', 'rejected'
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resumes Table
CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    extracted_text TEXT,
    skills JSONB, -- Array of extracted skills
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Aptitude Answers Table
CREATE TABLE IF NOT EXISTS aptitude_answers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL,
    answer VARCHAR(10) NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Technical Answers Table
CREATE TABLE IF NOT EXISTS technical_answers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL,
    answer TEXT NOT NULL,
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Coding Submissions Table
CREATE TABLE IF NOT EXISTS coding_submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    language VARCHAR(50) NOT NULL,
    code TEXT NOT NULL,
    test_cases_passed INTEGER DEFAULT 0,
    total_test_cases INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- HR Voice Transcriptions Table
CREATE TABLE IF NOT EXISTS hr_voice_transcriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    transcription TEXT,
    audio_file_path TEXT,
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chatbot Conversations Table
CREATE TABLE IF NOT EXISTS chatbot_conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Anti-Cheating Violations Table
CREATE TABLE IF NOT EXISTS anticheat_violations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    violation_type VARCHAR(100) NOT NULL, -- 'multiple_faces', 'tab_switching', 'fullscreen_exit'
    violation_details TEXT,
    round_number INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_candidate_scores_user_id ON candidate_scores(user_id);
CREATE INDEX IF NOT EXISTS idx_candidate_status_user_id ON candidate_status(user_id);
CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_aptitude_answers_user_id ON aptitude_answers(user_id);
CREATE INDEX IF NOT EXISTS idx_technical_answers_user_id ON technical_answers(user_id);
CREATE INDEX IF NOT EXISTS idx_coding_submissions_user_id ON coding_submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_hr_voice_transcriptions_user_id ON hr_voice_transcriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_chatbot_conversations_user_id ON chatbot_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_anticheat_violations_user_id ON anticheat_violations(user_id);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_candidate_scores_updated_at BEFORE UPDATE ON candidate_scores
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_candidate_status_updated_at BEFORE UPDATE ON candidate_status
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
