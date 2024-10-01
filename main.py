import re

def clean_text(text):
    # 'in profil resmi' gibi gereksiz ifadeleri temizle
    return re.sub(r"in profil resmi", "", text, flags=re.IGNORECASE).strip()

def has_common_words(text1, text2):
    words1 = set(text1.split())
    words2 = set(text2.split())
    # iki metin arasında ortak kelimeler var mı kontrol et
    return bool(words1 & words2)

def group_related_lines(lines):
    groups = []
    current_group = []

    for line in lines:
        cleaned_line = clean_text(line.strip().lower())
        if not cleaned_line:
            continue  # Boş satırları atla

        # Eğer current_group boşsa, bu satır gruba eklenir
        if not current_group:
            current_group.append(cleaned_line)
        else:
            # Eğer son satır ile bu satır arasında ilişki varsa gruba ekle
            if has_common_words(current_group[-1], cleaned_line):
                current_group.append(cleaned_line)
            else:
                # İlişki yoksa mevcut grubu kapat ve yeni bir grup başlat
                groups.append(current_group)
                current_group = [cleaned_line]

    if current_group:
        groups.append(current_group)

    return groups

def read_groups_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return group_related_lines(lines)

def compare_groups(file1, file2):
    groups_file1 = read_groups_from_file(file1)
    groups_file2 = read_groups_from_file(file2)

    unmatched_groups = []

    for group1 in groups_file1:
        found_match = False
        for group2 in groups_file2:
            # Grupları birleştirip her kelimeyi kontrol et
            words_in_group1 = set(' '.join(group1).split())
            words_in_group2 = set(' '.join(group2).split())

            # Eğer herhangi bir kelime eşleşirse eşleşme var demektir
            if words_in_group1 & words_in_group2:
                found_match = True
                break

        if not found_match:
            unmatched_groups.append(' '.join(group1))

    return unmatched_groups

file1_path = 'file1'
file2_path = 'file2'

unmatched_groups = compare_groups(file1_path, file2_path)

if unmatched_groups:
    print("Hiçbir kelimesi eşleşmeyen gruplar:")
    for group in unmatched_groups:
        print(group)
else:
    print("Tüm gruplarda en az bir kelime eşleşti.")
