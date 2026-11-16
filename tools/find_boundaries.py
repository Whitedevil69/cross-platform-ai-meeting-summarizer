# tools/find_boundaries.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def find_line(pattern, start=0):
    for i in range(start, len(lines)):
        if pattern in lines[i]:
            return i
    return -1

popover_css_start = find_line('.wp-more-popover {')
popover_css_end = find_line('.dark .wp-app-tile:hover span', popover_css_start)

views_css_start = find_line('/* ── View: Chat ── */')
views_css_end = find_line('/* ══════════════════════════════════════════════════════════════════════ */', views_css_start)

app_modal_css_start = find_line('.wp-app-modal-overlay {')
app_modal_css_end = find_line('/* ── POINT 1: REFINED HEADER SUB-BAR', app_modal_css_start)

view_home_start = find_line('<div class="wp-tab-view" id="view-home">')
view_clips_end = find_line('<!-- ═════════ 6. CLIPS TAB ═════════ -->')
popover_html_start = find_line('<div class="wp-more-popover" id="wpMoreAppsPopover"')
popover_html_end = find_line('<div class="wp-modal-overlay" id="joinMeetingModal"')

print(f"Popover CSS: lines {popover_css_start+1} to {popover_css_end+1}")
print(f"Views CSS: lines {views_css_start+1} to {views_css_end+1}")
print(f"App Modal CSS: lines {app_modal_css_start+1} to {app_modal_css_end+1}")
print(f"View Home HTML: line {view_home_start+1}")
print(f"View Clips End: line {view_clips_end+1}")
print(f"Popover HTML: lines {popover_html_start+1} to {popover_html_end+1}")
