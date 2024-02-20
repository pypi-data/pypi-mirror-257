import re


def extract_dong_from_address(address: str):
    import re
    # Regular expression pattern to find text inside parentheses
    pattern = r"\(([^)]+)\)"
    # Search for the pattern in the text
    match = re.search(pattern, address)

    # Extracting the matched group if it exists
    extracted_text = match.group(1) if match else None
    s = extracted_text.split(",")
    extracted_text = s[0]
    return extracted_text


# Function to remove "(주)" from the strings
def remove_company_indicator_in_strings(strings):
    return [re.sub(r'\(주\)\s*', '', s) for s in strings]


def remove_company_indicator(string):
    return re.sub(r'\(주\)\s*', '', string)


def remove_brackets_if_not_korean(string):
    # Check if the content inside the brackets is 100% Korean
    if re.search(r'\([가-힣\s\d\W]+\)', string):
        # Keep the string as it is if the brackets contain only Korean
        return string
    else:
        # Remove the brackets and their contents otherwise
        return re.sub(r'\([^\)]*\)', '', string)


def split_bracket_contents(string):
    parts = re.split(r'\((.*?)\)', string)
    # Keep only the part outside and inside the brackets, exclude the empty string at the end
    if len(parts) > 1:
        return (parts[0], parts[1])
    else:
        # If no brackets, return the original string and an empty string
        return (parts[0], '')


def filter_string(t):
    output = []
    for s in t:
        match = re.match(r'^[가-힣\s\d\W]+$', s)
        matched_data = match.group() if match else None
        if matched_data is not None:
            output.append(matched_data)
    return tuple(output)


def make_simple_store_name(store_name):
    transformed = remove_company_indicator(store_name)
    transformed = remove_brackets_if_not_korean(transformed)

    # 수정된 정규표현식: 문자열 끝에 단일 숫자만 있는 경우에만 숫자 제거
    regex_single_digit_strict_at_end = r"(?<!\d)\d(?=\s*$)"
    # 네이버 지도 검색에 적합하지않은 브랜드명 교정
    transformed = re.sub(regex_single_digit_strict_at_end, "", transformed)
    transformed = transformed.replace("메가엠지씨커피", "메가MGC")

    splited = split_bracket_contents(transformed)
    filtered = filter_string(splited)
    if len(filtered) == 0:
        return store_name
    return " ".join(filtered)

