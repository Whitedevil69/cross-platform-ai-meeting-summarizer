# tools/fix_balance.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the duplicate closing div at the end of view-home
target = """            </section>
          </div>

          <!-- ════════════════════════════════════════════════════════════════ -->
          <!-- RIGHT COLUMN (Preserved Matching Dribbble Reference)             -->
          <!-- ════════════════════════════════════════════════════════════════ -->
          </div>"""

replacement = """            </section>
          </div>"""

if target in text:
    text = text.replace(target, replacement, 1)
    print("[OK] Removed extra closing div at end of view-home")
else:
    print("[WARN] Target not found")

# Add id="wpAppSuiteModalDialog"
text = text.replace(
    '<div class="wp-app-modal-dialog" onclick="event.stopPropagation()">',
    '<div class="wp-app-modal-dialog" id="wpAppSuiteModalDialog" onclick="event.stopPropagation()">'
)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("[OK] Finished balance fix")
