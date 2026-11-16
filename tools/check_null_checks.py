# tools/check_null_checks.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line_no, line in enumerate(lines):
    for m in ['recentMeetingsSection', 'rmSearchClear', 'btnAccountContinue', 'displayUserEmail', 'uploadMeetingTitle', 'btnScrollToUpload', 'themeIcon', 'avatarLetter', 'rmSearchInput', 'btnOpenJoinModal']:
        if f"'{m}'" in line or f'"{m}"' in line:
            print(f"Line {line_no+1}: {line.strip()[:80]}")
