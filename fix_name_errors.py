import os

def fix_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    fixed = False
    for line in lines:
        if "user = st.session_state.get('user')" in line or "user = st.session_state.get('user', {})" in line:
            indent = line[:line.find("user")]
            new_lines.append(line)
            new_lines.append(f"{indent}user_id = user.get('id', 0) if user else 0\n")
            fixed = True
        elif "user = get_current_user()" in line:
            indent = line[:line.find("user")]
            new_lines.append(line)
            new_lines.append(f"{indent}user_id = user.get('id', 0) if user else 0\n")
            fixed = True
        else:
            new_lines.append(line)
    
    if fixed:
        with open(path, 'w') as f:
            f.writelines(new_lines)
        return True
    return False

modules = [
    'modules/round1_resume.py',
    'modules/round2_aptitude.py',
    'modules/round3_technical.py',
    'modules/round4_coding.py',
    'modules/round5_voice.py',
    'modules/round6_chatbot.py',
    'modules/round7_dashboard.py',
    'modules/admin.py',
    'modules/anticheat.py'
]

for m in modules:
    path = f"/Users/pranaybayana/Desktop/AI intervuew system/{m}"
    if os.path.exists(path):
        if fix_file(path):
            print(f"Fixed {m}")
        else:
            print(f"Skipped {m} (no user pattern found)")
