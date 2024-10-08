import re

def clean_text(text):
    # Clean unnecessary phrases in Turkish and English
    patterns = [
        r"Ara",
        r"Search",
        r"Followers",
        r"People",
        r"Hashtags",
        r"Takip Ettikleri",
        r"Kişiler",
        r"Konu Etiketleri",
        r"Takipçiler",
        r"Following",
        r"'in profil resmi",  # Turkish: 'in profil resmi'
        r"'s profile picture"  # English: 's profile picture'
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text.strip()

def has_common_words(text1, text2):
    words1 = set(text1.split())
    words2 = set(text2.split())
    # Check if there are common words between the two texts
    return bool(words1 & words2)

def group_related_lines(lines):
    groups = []
    current_group = []

    for line in lines:
        cleaned_line = clean_text(line.strip().lower())
        if not cleaned_line:
            continue  # Skip empty lines

        # If current_group is empty, add this line to the group
        if not current_group:
            current_group.append(cleaned_line)
        else:
            # If there is a relationship between the last line and this line, add to the group
            if has_common_words(current_group[-1], cleaned_line):
                current_group.append(cleaned_line)
            else:
                # If there is no relationship, close the current group and start a new one
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
            # Merge the groups and check each word
            words_in_group1 = set(' '.join(group1).split())
            words_in_group2 = set(' '.join(group2).split())

            # If any word matches, it indicates a match
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
    print("Groups with no matching words:")
    for group in unmatched_groups:
        print(group)
else:
    print("All groups have at least one matching word.")
