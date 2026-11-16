with open("frontend/room.html", "r", encoding="utf-8") as f:
    text = f.read()

pos1 = text.find("function showConsentModal")
print("=== showConsentModal ===")
print(text[pos1:pos1+400])

pos2 = text.find("function openShareModal")
print("=== openShareModal ===")
print(text[pos2:pos2+400])
