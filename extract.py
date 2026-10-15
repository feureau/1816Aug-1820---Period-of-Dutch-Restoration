import re
import os

file_path = r"F:\GitHub\1816Aug-1820 - Period of Dutch Restoration\1816Aug-1820 - Period of Dutch Restoration.md"
out_path = r"F:\GitHub\1816Aug-1820 - Period of Dutch Restoration\Names_Terms_Places.md"

if not os.path.exists(file_path):
    print("File not found.")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

entities = set()

# 1. Extract from markdown tables (first column)
for line in text.split('\n'):
    line = line.strip()
    if line.startswith('|') and '---' not in line:
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if parts:
            term = parts[0].replace('*', '').replace('_', '')
            if term and term.lower() not in ['abbreviation / term', 'abbreviation / name', 'term', 'region', 'date', 'kyai murma wat. credits']:
                entities.add(term)

# 2. Extract capitalized phrases (Names, Titles, Places, Institutions)
# Pattern: Word starting with Upper, followed optionally by more Upper-starting words or hyphens.
pattern = r'\b[A-Z][a-zA-Z]*(?:-[A-Z][a-zA-Z]*)*(?:\s+[A-Z][a-zA-Z]*(?:-[A-Z][a-zA-Z]*)*)*\b'
for match in re.finditer(pattern, text):
    m = match.group(0).strip()
    entities.add(m)

# 3. Extract italicized terms (often Javanese/Dutch terms in this text)
italics = re.findall(r'\b_([a-zA-Z0-9\s-]+)_\b|\B\*([a-zA-Z0-9\s-]+)\*\B', text)
for match in italics:
    term = match[0] or match[1]
    if term:
        entities.add(term.strip())

# Clean and filter
stop_words = {"The", "A", "An", "In", "On", "At", "To", "With", "For", "And", "But", "Or", "If", "Then", "This", "That", "These", "Those", "Is", "Are", "Was", "Were", "As", "It", "Of", "By", "From", "When", "Where", "Why", "How", "He", "She", "They", "We", "You", "I", "Not", "No", "Yes", "So", "Their", "His", "Her", "Our", "My", "Your", "Its", "All", "Some", "Any", "Many", "Few", "Much", "More", "Most", "Such", "No", "Nor", "Only", "Own", "Same", "Than", "Too", "Very", "Can", "Could", "Will", "Would", "Shall", "Should", "May", "Might", "Must", "Do", "Does", "Did", "Has", "Have", "Had", "Am", "Be", "Been", "Being", "Which", "Who", "Whom", "Whose", "What", "There", "Here", "About", "Against", "Between", "Into", "Through", "During", "Before", "After", "Above", "Below", "Under", "Over", "Again", "Further", "Once"}

final_entities = []
for e in entities:
    e = e.strip(".,;:!?()[]{}'\" \t")

    # Remove purely Roman numerals (often parts of names but on their own they aren't useful)
    if re.fullmatch(r'[IVXLCDM]+', e):
        continue

    # Filter lengths
    if len(e) <= 2 or len(e) > 50:
        continue

    # Specifically exclude pure uppercase acronyms if they are likely just formatting
    if e in ["START OF TRUNCATED OUTPUT", "END OF TRUNCATED OUTPUT", "IMG", "END", "START"]:
        continue

    # Check stop words
    if e in stop_words:
        continue

    if not e.isdigit():
        final_entities.append(e)

# Deduplicate case-insensitively but keep the original capitalization (prefer title case)
unique_entities = {}
for e in final_entities:
    lower_e = e.lower()
    if lower_e not in unique_entities:
        unique_entities[lower_e] = e
    else:
        # Prefer the one with more uppercase letters if they clash
        if sum(1 for c in e if c.isupper()) > sum(1 for c in unique_entities[lower_e] if c.isupper()):
            unique_entities[lower_e] = e

sorted_entities = sorted(unique_entities.values(), key=lambda x: x.lower())

with open(out_path, 'w', encoding='utf-8') as f:
    f.write("# Names, Terms, and Places\n\n")
    f.write(f"Extracted from 1816Aug-1820 - Period of Dutch Restoration.md\n\n")

    current_letter = ''
    for ent in sorted_entities:
        first_char = ent[0].upper()
        if first_char != current_letter and first_char.isalpha():
            current_letter = first_char
            f.write(f"\n## {current_letter}\n")
        f.write(f"- {ent}\n")

print(f"Extracted {len(sorted_entities)} entities. Wrote to {out_path}")
