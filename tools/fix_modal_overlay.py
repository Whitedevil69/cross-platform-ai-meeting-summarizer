import re, subprocess

with open("frontend/room.html", "r", encoding="utf-8") as f:
    text = f.read()

old_listeners = """        // End meeting
        btnEndMeeting.addEventListener('click', openEndConfirmModal);
        btnCancelEnd.addEventListener('click', closeEndConfirmModal);
        btnConfirmEnd.addEventListener('click', executeEndMeeting);"""

new_listeners = """        // End meeting
        btnEndMeeting.addEventListener('click', (e) => {
          e.preventDefault();
          openEndConfirmModal();
        });
        btnCancelEnd.addEventListener('click', closeEndConfirmModal);
        btnConfirmEnd.addEventListener('click', executeEndMeeting);
        modalEndConfirm.addEventListener('click', (e) => {
          if (e.target === modalEndConfirm) closeEndConfirmModal();
        });"""

if old_listeners in text:
    text = text.replace(old_listeners, new_listeners, 1)
    with open("frontend/room.html", "w", encoding="utf-8") as f:
        f.write(text)
    print("[OK] Updated btnEndMeeting listeners")
else:
    print("[ERROR] old_listeners not found")

# Node check
script_m = re.search(r'<script>([\s\S]*?)</script>', text)
if script_m:
    with open("tools/temp_script.js", "w", encoding="utf-8") as f:
        f.write(script_m.group(1))
    res = subprocess.run(["node", "-c", "tools/temp_script.js"], capture_output=True, text=True)
    if res.returncode == 0:
        print("[OK] JavaScript syntax is valid!")
    else:
        print("[FAIL] JavaScript error:", res.stderr)
