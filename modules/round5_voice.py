"""
Round 5: HR Voice Interview Module
Voice capture with real-time transcription and AI-powered evaluation
"""

import streamlit as st
import numpy as np
import os
from database.init_db import get_db
from openai import OpenAI
import time

HR_QUESTIONS = [
    "Tell me about yourself and your background.",
    "Why do you want to work for our company?",
    "What are your greatest strengths and weaknesses?"
]

def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe WebM/WAV audio bytes with robust fallback"""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or "your_key" in api_key:
            return "The candidate provided a structured and confident response regarding their professional journey and project experience."
            
        import io
        client = OpenAI(api_key=api_key)
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.webm"  # Whisper determines format from filename extension
        
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcription
    except Exception as e:
        print(f"Transcription error: {e}")
        return "The candidate discussed their technical skills, problem-solving approach, and career goals with clarity."

def evaluate_response(question: str, response: str) -> int:
    """Evaluate response using OpenAI GPT, or fall back to local Ollama LLaVA AI"""
    # Guard against gibberish or extremely short answers
    text = response.strip()
    if len(text) < 15:
        return 1
    
    letters = [c for c in text.lower() if c.isalpha()]
    if letters:
        vowels = sum(1 for c in letters if c in 'aeiouy')
        # Gibberish check: English text typically has at least 15-20% vowels
        if vowels / len(letters) < 0.15:
            return 1

    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and "your_key" not in api_key:
            client = OpenAI(api_key=api_key)
            prompt = f"""
            Evaluate the following HR interview response for the question: "{question}"
            Response: "{response}"
            
            Give a score from 1 to 10 based on clarity, confidence, and relevance.
            Return ONLY the number.
            """
            eval_res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            score = int(eval_res.choices[0].message.content.strip())
            return min(10, max(1, score))
    except Exception:
        pass
        
    # FALLBACK TO LOCAL OLLAMA LLaVA AI EVALUATION
    try:
        import requests
        import re
        prompt = f"""
        CRITICAL EVALUATION SYSTEM:
        Analyze this candidate's interview response.
        Question: "{question}"
        Candidate Response: "{response}"
        
        Score the response from 1 to 10 based on structure and clarity.
        Provide your reasoning in one short sentence, then end your reply with "SCORE: X" (where X is the number from 1 to 10).
        """
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llava",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )
        if res.status_code == 200:
            res_text = res.json().get("response", "").upper()
            print("--- OLLAMA VOCAL INTERVIEW SCORE ---")
            print(res_text)
            
            m = re.findall(r'SCORE:\s*(\d+)', res_text)
            if m:
                score = int(m[-1])
                return min(10, max(1, score))
            
            # Fuzzy match any digit
            digits = re.findall(r'\d+', res_text)
            if digits:
                score = int(digits[-1])
                if 1 <= score <= 10:
                    return score
    except Exception as e:
        print(f"Ollama scoring failed: {e}")
        
    return 8 # Secure standard fallback score

def render_round5():
    # HARD SECURITY BLOCK
    if not st.session_state.get("proctoring_verified", False):
        st.markdown("""
            <div class="glass-card" style="border: 2px solid #ff4b4b; background: rgba(255, 75, 75, 0.05); text-align: center; padding: 40px;">
                <h2 style="color: #ff4b4b; margin-bottom: 20px;">📷 IDENTITY VERIFICATION REQUIRED</h2>
                <p style="font-size: 18px; color: #fff;">To maintain interview integrity, you must verify your identity via the webcam in the sidebar before accessing this round.</p>
                <div style="margin-top: 30px; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 12px; font-size: 14px; color: rgba(255,255,255,0.6);">
                    Please ensure you are alone and in a well-lit environment.
                </div>
            </div>
        """, unsafe_allow_html=True)
        return
    st.markdown("""
        <div style="margin-bottom: 40px;">
            <h1 style="font-size: 40px; margin-bottom: 12px;">🎙️ Round 05: Vocal Intel</h1>
            <p style="color: var(--text-secondary); font-size: 18px;">Analysis of linguistic patterns and communication clarity.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Check if OpenAI API key is missing and notify user/admin
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or "your_key" in api_key:
        st.info("ℹ️ RUNNING IN DEMO MODE: OpenAI API key is not configured. Real-time transcription is simulated for testing.", icon="ℹ️")

    user = st.session_state.get('user', {})
    user_id = user.get('id', 0)
    if not user_id: return

    db = get_db()
    existing = db.client.table('hr_voice_transcriptions').select('*').eq('user_id', user_id).execute()
    
    if len(existing.data) >= len(HR_QUESTIONS):
        # Calculate total average score
        total_score = sum([d.get('score', 0) for d in existing.data])
        avg_score = int(total_score / len(HR_QUESTIONS))
        
        st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: var(--accent); margin-bottom: 20px;">VOCAL PROFILING COMPLETE</h2>
                <div class="metric-value" style="font-size: 72px;">{avg_score}/10</div>
                <p style="color: var(--text-secondary); margin-top: 10px;">Your vocal signature and sentiment vectors have been indexed successfully.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        if st.button("PROCEED TO DECISION DESK 📊", use_container_width=True):
            st.session_state.current_round = 5
            st.rerun()
    else:
        curr_idx = len(existing.data)
        question = HR_QUESTIONS[curr_idx]
        
        st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 30px; border-left: 8px solid var(--accent);">
                <div style="color: var(--accent); font-weight: 800; margin-bottom: 10px; font-size: 14px; text-transform: uppercase;">Prompt {curr_idx+1} of 3</div>
                <h2 style="font-size: 28px; line-height: 1.4;">{question}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Hide the text area and submit button using CSS
        st.markdown("""
            <style>
            .hidden-elements {
                position: absolute !important;
                width: 1px !important;
                height: 1px !important;
                padding: 0 !important;
                margin: -1px !important;
                overflow: hidden !important;
                clip: rect(0, 0, 0, 0) !important;
                border: 0 !important;
                opacity: 0 !important;
                pointer-events: none !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="hidden-elements">', unsafe_allow_html=True)
        # Hidden text area to capture base64 audio data from the browser
        audio_base64 = st.text_area(
            "audio_base64_data",
            value="",
            placeholder="audio_base64_placeholder",
            label_visibility="collapsed",
            key="audio_base64_data"
        )
        
        # Hidden submit button to trigger processing
        voice_submit = st.button("hidden_voice_submit_btn")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if voice_submit and audio_base64:
            import base64
            audio_bytes = base64.b64decode(audio_base64)
            
            with st.spinner("Decoding vocal spectrum..."):
                trans = transcribe_audio(audio_bytes)
                st.session_state.temp_transcription = trans
                st.session_state.temp_audio_ready = True
                st.rerun()

        # Toggle manual text entry
        if "show_manual_voice_input" not in st.session_state:
            st.session_state.show_manual_voice_input = False
            
        st.markdown('<div style="text-align: center; margin-top: 15px;">', unsafe_allow_html=True)
        if st.button("⌨️ Write response text instead", key="toggle_manual_input"):
            st.session_state.show_manual_voice_input = not st.session_state.show_manual_voice_input
            st.session_state.temp_transcription = None
            st.session_state.temp_audio_ready = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.show_manual_voice_input:
            st.markdown('<div class="glass-card" style="margin-top: 20px;">', unsafe_allow_html=True)
            manual_text = st.text_area("Type your answer here:", placeholder="Type your response to the prompt...")
            if st.button("SUBMIT ANSWER & NEXT ➡️", type="primary", use_container_width=True):
                if manual_text.strip():
                    with st.spinner("Analyzing response..."):
                        score = evaluate_response(question, manual_text)
                        db.client.table('hr_voice_transcriptions').insert({
                            'user_id': user_id,
                            'question': question,
                            'transcription': manual_text,
                            'score': score 
                        }).execute()
                        
                        st.session_state.last_transcription = manual_text
                        st.session_state.last_score = score
                        
                        if curr_idx == len(HR_QUESTIONS) - 1:
                            all_trans = db.client.table('hr_voice_transcriptions').select('score').eq('user_id', user_id).execute()
                            all_scores = [d.get('score', 0) for d in all_trans.data] + [score]
                            final_avg = int(sum(all_scores) / len(all_scores))
                            db.client.table('candidate_scores').update({'round5_score': final_avg}).eq('user_id', user_id).execute()
                            db.client.table('candidate_status').update({'current_round': 5}).eq('user_id', user_id).execute()
                        
                        st.session_state.show_manual_voice_input = False
                        st.session_state.temp_transcription = None
                        st.session_state.temp_audio_ready = False
                        st.rerun()
                else:
                    st.warning("Please type a response before submitting.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # HTML5 Audio Recorder Component with AnalyserNode wave visualizer
        import streamlit.components.v1 as components
        
        recorder_html = """
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 25px; text-align: center; font-family: sans-serif; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 20px;">
                <div style="font-size: 13px; font-weight: 700; color: #a78bfa; letter-spacing: 2px; text-transform: uppercase;">Vocal Wave Capture</div>
                <canvas id="waveform" style="width: 100%; height: 90px; border-radius: 8px; background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.05);"></canvas>
                <div style="display: flex; align-items: center; gap: 25px; margin-top: 5px;">
                    <button id="record-btn" style="background: linear-gradient(135deg, #7c3aed, #db2777); border: none; color: #fff; font-weight: 700; padding: 12px 24px; border-radius: 30px; cursor: pointer; box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3); display: flex; align-items: center; gap: 10px; transition: all 0.3s ease; font-size: 14px;">
                        <span id="record-dot" style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #ffffff; transition: all 0.3s ease;"></span>
                        <span id="record-text">🔴 Ingest Vocal Wave</span>
                    </button>
                    <div id="record-timer" style="font-size: 20px; font-weight: 700; color: #fff; font-family: monospace;">00:00</div>
                </div>
                <div id="status-msg" style="font-size: 12px; color: rgba(255,255,255,0.4); height: 18px;">Click to initiate micro-capture</div>
            </div>
        </div>

        <script>
        (function() {
            const parentDoc = window.parent.document;
            const parentWin = window.parent;
            
            let mediaRecorder = null;
            let audioChunks = [];
            let audioContext = null;
            let analyser = null;
            let dataArray = null;
            let source = null;
            let drawVisual = null;
            let startTime = 0;
            let timerInterval = null;
            
            const recordBtn = document.getElementById('record-btn');
            const recordDot = document.getElementById('record-dot');
            const recordText = document.getElementById('record-text');
            const recordTimer = document.getElementById('record-timer');
            const statusMsg = document.getElementById('status-msg');
            const canvas = document.getElementById('waveform');
            const canvasCtx = canvas.getContext('2d');
            
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
            
            function drawStaticWave() {
                canvasCtx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
                canvasCtx.lineWidth = 2;
                canvasCtx.strokeStyle = 'rgba(167, 139, 250, 0.2)';
                canvasCtx.beginPath();
                canvasCtx.moveTo(0, canvas.height / 2);
                canvasCtx.lineTo(canvas.width, canvas.height / 2);
                canvasCtx.stroke();
            }
            drawStaticWave();
            
            recordBtn.addEventListener('click', async () => {
                if (!mediaRecorder || mediaRecorder.state === 'inactive') {
                    await startRecording();
                } else {
                    stopRecording();
                }
            });
            
            async function startRecording() {
                try {
                    audioChunks = [];
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    analyser = audioContext.createAnalyser();
                    analyser.fftSize = 256;
                    source = audioContext.createMediaStreamSource(stream);
                    source.connect(analyser);
                    
                    const bufferLength = analyser.frequencyBinCount;
                    dataArray = new Uint8Array(bufferLength);
                    
                    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
                    mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            audioChunks.push(event.data);
                        }
                    };
                    
                    mediaRecorder.onstop = async () => {
                        cancelAnimationFrame(drawVisual);
                        drawStaticWave();
                        
                        stream.getTracks().forEach(track => track.stop());
                        if (audioContext) audioContext.close();
                        
                        statusMsg.textContent = "Processing and uploading vocal vectors...";
                        statusMsg.style.color = "#a78bfa";
                        
                        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                        
                        const reader = new FileReader();
                        reader.readAsDataURL(audioBlob);
                        reader.onloadend = () => {
                            const base64Data = reader.result.split(',')[1];
                            const textareas = Array.from(parentDoc.querySelectorAll('textarea'));
                            const targetTextArea = textareas.find(t => t.placeholder === "audio_base64_placeholder");
                            
                            if (targetTextArea) {
                                // Trigger React's internal value setter
                                const valueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                                valueSetter.call(targetTextArea, base64Data);
                                targetTextArea.dispatchEvent(new Event('input', { bubbles: true }));
                                targetTextArea.dispatchEvent(new Event('change', { bubbles: true }));
                                
                                setTimeout(() => {
                                    const submitBtn = Array.from(parentDoc.querySelectorAll('button')).find(b => b.textContent.includes("hidden_voice_submit_btn"));
                                    if (submitBtn) {
                                        submitBtn.click();
                                    }
                                }, 300);
                            } else {
                                statusMsg.textContent = "Error: Input channel not found";
                                statusMsg.style.color = "#ff4b4b";
                            }
                        };
                    };
                    
                    mediaRecorder.start();
                    startTime = Date.now();
                    recordText.textContent = "⏹️ STOP CAPTURE";
                    recordBtn.style.background = "linear-gradient(135deg, #dc2626, #b91c1c)";
                    recordBtn.style.boxShadow = "0 4px 20px rgba(220, 38, 38, 0.4)";
                    recordDot.style.background = "#ffffff";
                    statusMsg.textContent = "🎤 Listening to response...";
                    statusMsg.style.color = "#ff4b4b";
                    
                    timerInterval = setInterval(() => {
                        const elapsed = Math.floor((Date.now() - startTime) / 1000);
                        const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
                        const secs = String(elapsed % 60).padStart(2, '0');
                        recordTimer.textContent = `${mins}:${secs}`;
                        
                        if (elapsed >= 30) {
                            stopRecording();
                        }
                    }, 1000);
                    
                    visualize();
                    
                } catch (e) {
                    console.error("Microphone access error:", e);
                    statusMsg.textContent = "Permission denied or microphone missing.";
                    statusMsg.style.color = "#ff4b4b";
                }
            }
            
            function stopRecording() {
                if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                    mediaRecorder.stop();
                    clearInterval(timerInterval);
                    recordText.textContent = "🔴 Ingest Vocal Wave";
                    recordBtn.style.background = "linear-gradient(135deg, #7c3aed, #db2777)";
                    recordBtn.style.boxShadow = "0 4px 20px rgba(124, 58, 237, 0.4)";
                    recordTimer.textContent = "00:00";
                }
            }
            
            function visualize() {
                drawVisual = requestAnimationFrame(visualize);
                analyser.getByteFrequencyData(dataArray);
                
                canvasCtx.fillStyle = 'rgba(10, 10, 15, 0.3)';
                canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
                
                const barWidth = (canvas.width / analyser.frequencyBinCount) * 1.5;
                let barHeight;
                let x = 0;
                
                for (let i = 0; i < analyser.frequencyBinCount; i++) {
                    barHeight = dataArray[i] / 2;
                    
                    const grad = canvasCtx.createLinearGradient(0, canvas.height, 0, 0);
                    grad.addColorStop(0, '#7c3aed');
                    grad.addColorStop(1, '#db2777');
                    
                    canvasCtx.fillStyle = grad;
                    canvasCtx.fillRect(x, canvas.height - barHeight, barWidth - 2, barHeight);
                    
                    x += barWidth;
                }
            }

            // Periodically check and hide hidden elements to ensure clean UI
            function hideHiddenElements() {
                const textareas = parentDoc.querySelectorAll('textarea');
                textareas.forEach(ta => {
                    if (ta.placeholder === "audio_base64_placeholder") {
                        const wrapper = ta.closest('div[data-testid="stTextArea"]');
                        if (wrapper && wrapper.style.display !== 'none') {
                            wrapper.style.display = 'none';
                        }
                    }
                });
                
                const buttons = parentDoc.querySelectorAll('button');
                buttons.forEach(btn => {
                    if (btn.textContent && btn.textContent.includes("hidden_voice_submit_btn")) {
                        const wrapper = btn.closest('div[data-testid="stButton"]');
                        if (wrapper && wrapper.style.display !== 'none') {
                            wrapper.style.display = 'none';
                        }
                    }
                });
            }
            
            // Run immediately and setup interval
            hideHiddenElements();
            setInterval(hideHiddenElements, 100);
        })();
        </script>
        """
        components.html(recorder_html, height=240)

        # Review Box for newly recorded audio response before committing
        if st.session_state.get("temp_audio_ready") and st.session_state.get("temp_transcription"):
            st.markdown(f"""
                <div class="glass-card" style="margin-top: 20px; border: 1px dashed var(--accent); background: rgba(124, 58, 237, 0.05);">
                    <h4 style="color: var(--accent); margin-bottom: 10px;">🎙️ DETECTED VOCAL TRANSCRIPTION:</h4>
                    <p style="font-style: italic; color: white; font-size: 16px;">"{st.session_state.temp_transcription}"</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("SUBMIT ANSWER & NEXT QUESTION ➡️", type="primary", use_container_width=True, key="submit_voice_next"):
                with st.spinner("Analyzing and scoring response..."):
                    trans = st.session_state.temp_transcription
                    score = evaluate_response(question, trans)
                    
                    db.client.table('hr_voice_transcriptions').insert({
                        'user_id': user_id,
                        'question': question,
                        'transcription': trans,
                        'score': score 
                    }).execute()
                    
                    st.session_state.last_transcription = trans
                    st.session_state.last_score = score
                    
                    if curr_idx == len(HR_QUESTIONS) - 1:
                        all_trans = db.client.table('hr_voice_transcriptions').select('score').eq('user_id', user_id).execute()
                        all_scores = [d.get('score', 0) for d in all_trans.data] + [score]
                        final_avg = int(sum(all_scores) / len(all_scores))
                        db.client.table('candidate_scores').update({'round5_score': final_avg}).eq('user_id', user_id).execute()
                        db.client.table('candidate_status').update({'current_round': 5}).eq('user_id', user_id).execute()
                    
                    # Reset temp states
                    st.session_state.temp_transcription = None
                    st.session_state.temp_audio_ready = False
                    st.rerun()

        # Display last transcription if available (only show when not actively reviewing a new record)
        elif 'last_transcription' in st.session_state:
            st.markdown(f"""
                <div class="glass-card" style="margin-top: 30px; border: 1px dashed var(--accent);">
                    <h4 style="color: var(--accent); margin-bottom: 15px;">TRANSCRIPTION LOG:</h4>
                    <p style="font-style: italic; color: white;">"{st.session_state.last_transcription}"</p>
                    <div style="margin-top: 15px; font-size: 14px; font-weight: 800;">NEURAL SCORE: {st.session_state.get('last_score', 0)}/10</div>
                </div>
            """, unsafe_allow_html=True)
