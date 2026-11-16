# -*- coding: utf-8 -*-
"""
build_dribbble_layout.py
Rebuilds frontend/index.html to match the exact layout, color palette, gradients,
sidebar dock, cards, and typography of the reference Dribbble image:
- Outer canvas: Soft sage #a9b8aa
- Floating app window: Pure white #ffffff, border-radius: 36px, soft shadow
- Left vertical dock: Sleek dark capsule #18191b, border-radius: 28px
- Header: Bold editorial title "Managing Your Meetings and Workflows" with badges
- Capsule pill bar: Organization / Dashboard (dark active pill #18191b), Chat, Phone, Docs, Whiteboards, Clips, More Apps
- 3 Top Hero Cards:
  1. Operations Metric card (#fbfcfb, border-radius: 24px, 780 count, 8-capsule indicator row)
  2. Chartreuse-lime highlight card (linear-gradient(135deg, #e5f97e 0%, #def670 100%), 163 count, 68% pill)
  3. Dark hero card (#18191b, "Take Your AI Automation to the Next Level", white pill button)
- Wide Statistics / Decision Graph Card (#fbfcfb, border-radius: 24px, dual-color capsule bars)
- Right Column:
  - 2 top square cards: Community (chat) & Academy (whiteboard graph)
  - 4 vertical link cards: Help Center (AI Companion), Partner Directory (Contacts), Blog (Docs), Use Cases (More Apps)
- Preserves ALL existing JavaScript, modals, forms, and features without removing anything!
"""
import re

with open("frontend/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Make backup
with open("frontend/index.html.bak_dribbble", "w", encoding="utf-8") as f:
    f.write(content)
print("Backup created.")
