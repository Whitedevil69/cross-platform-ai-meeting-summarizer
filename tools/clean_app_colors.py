# tools/clean_app_colors.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Clean Mail Citation Card
text = text.replace(
    '<div class="app-card" style="background:rgba(124,58,237,0.08);border-color:rgba(124,58,237,0.2);">\n              <div style="font-size:0.8rem;font-weight:700;color:#c4b5fd;margin-bottom:4px;">💡 AI Evidence Citation</div>',
    '<div class="app-card" style="background:#fbfcfb;border-color:#edf0ed;">\n              <div style="font-size:0.8rem;font-weight:700;color:#18191b;margin-bottom:4px;">💡 AI Evidence Citation</div>'
)

# 2. Clean Scheduler Dur Button & Checkbox
text = text.replace(
    'class="app-btn-secondary sched-dur-btn active" style="border-color:#38bdf8;color:#38bdf8;"',
    'class="app-btn-secondary sched-dur-btn active" style="border-color:#18191b;color:#18191b;background:#e5f97e;font-weight:700;"'
)
text = text.replace(
    '<input type="checkbox" id="schedBotToggle" checked style="width:18px;height:18px;accent-color:#38bdf8;">',
    '<input type="checkbox" id="schedBotToggle" checked style="width:18px;height:18px;accent-color:#18191b;">'
)
text = text.replace(
    '<div style="font-size:0.78rem;font-weight:700;color:#38bdf8;margin-bottom:4px;">SHAREABLE ROOM URL</div>',
    '<div style="font-size:0.78rem;font-weight:700;color:#18191b;margin-bottom:4px;">SHAREABLE ROOM URL</div>'
)

# 3. Clean Poll Accent and Pct
text = text.replace(
    '<input type="radio" name="poll-${poll.id}" value="${oIdx}" style="accent-color:#38bdf8;">',
    '<input type="radio" name="poll-${poll.id}" value="${oIdx}" style="accent-color:#18191b;">'
)
text = text.replace(
    '<span style="font-weight:600;color:#38bdf8;font-family:var(--font-mono);">${pct}% (${opt.votes})</span>',
    '<span style="font-weight:700;color:#059669;font-family:var(--font-mono);">${pct}% (${opt.votes})</span>'
)

# 4. Clean Revenue Accelerator Next Best Action Card
text = text.replace(
    '<div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.25);border-radius:12px;padding:14px;margin-bottom:14px;">\n              <div style="font-size:0.8rem;font-weight:700;color:#c4b5fd;margin-bottom:4px;">🎯 AI Next Best Action</div>',
    '<div style="background:#fbfcfb;border:1px solid #edf0ed;border-radius:14px;padding:14px;margin-bottom:14px;">\n              <div style="font-size:0.8rem;font-weight:700;color:#18191b;margin-bottom:4px;">🎯 AI Next Best Action</div>'
)
text = text.replace(
    '<span style="color:#38bdf8;">Rep 41% / Prospect 59%</span>',
    '<span style="color:#059669;font-weight:600;">Rep 41% / Prospect 59%</span>'
)
text = text.replace(
    '<div style="font-size:0.75rem;color:#38bdf8;margin-bottom:12px;">Stage: Solution Validation & Security Review</div>',
    '<div style="font-size:0.75rem;color:#059669;font-weight:600;margin-bottom:12px;">Stage: Solution Validation & Security Review</div>'
)

# 5. Clean Contact Center percentage
text = text.replace(
    '<div style="font-size:1.6rem;font-weight:800;color:#38bdf8;margin:2px 0;">94.6%</div>',
    '<div style="font-size:1.6rem;font-weight:800;color:#18191b;margin:2px 0;">94.6%</div>'
)
text = text.replace(
    '<td style="padding:10px 8px;font-family:var(--font-mono);color:#38bdf8;">#CC-4910</td>',
    '<td style="padding:10px 8px;font-family:var(--font-mono);color:#059669;font-weight:600;">#CC-4910</td>'
)
text = text.replace(
    '<td style="padding:10px 8px;font-family:var(--font-mono);color:#38bdf8;">#CC-4911</td>',
    '<td style="padding:10px 8px;font-family:var(--font-mono);color:#059669;font-weight:600;">#CC-4911</td>'
)
text = text.replace(
    '<td style="padding:10px 8px;font-family:var(--font-mono);color:#38bdf8;">#CC-4912</td>',
    '<td style="padding:10px 8px;font-family:var(--font-mono);color:#059669;font-weight:600;">#CC-4912</td>'
)

# 6. Clean Workvivo author and hashtags
text = text.replace(
    '<strong style="color:#38bdf8;">${c.author}:</strong>',
    '<strong style="color:#18191b;">${c.author}:</strong>'
)
text = text.replace(
    '<span style="color:#38bdf8;">#SyncraWorkplace2</span>',
    '<span style="color:#059669;font-weight:600;">#SyncraWorkplace2</span>'
)
text = text.replace(
    '<span style="color:#38bdf8;">#WhisperCUDAOptimization</span>',
    '<span style="color:#059669;font-weight:600;">#WhisperCUDAOptimization</span>'
)

# 7. Clean dynamic loadDocsView row
text = text.replace(
    '<td><span style="color:#c4b5fd;font-weight:600;">${(it.type||\'item\').toUpperCase()}</span></td>',
    '<td><span class="app-badge-status app-badge-purple">${(it.type||\'item\').toUpperCase()}</span></td>'
)
text = text.replace(
    '<td><span style="color:#38bdf8;font-family:var(--font-mono);">${evQuote}</span></td>',
    '<td><span style="color:#059669;font-family:var(--font-mono);font-weight:600;">${evQuote}</span></td>'
)

# 8. Clean role in contacts
text = text.replace(
    '<div style="font-size:0.75rem;color:#38bdf8;margin:2px 0;">${c.role}</div>',
    '<div style="font-size:0.75rem;color:#059669;font-weight:600;margin:2px 0;">${c.role}</div>'
)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("[OK] Finished cleaning inline colors in app modules")
