import re
from collections import Counter
from datetime import datetime,timedelta
#from rapidfuzz import fuzz
from fuzzywuzzy import fuzz
from langdetect import detect
from hijri_converter import convert
from datetime import datetime
import base64
import cv2
import numpy as np
from google.cloud import vision_v1
import fitz
### Define functions

def pdf_to_bytes(pdf_file_path):
#     try:
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        return pdf_bytes


def check_overlap(list1, list2):
    return any(elem in list2 for elem in list1)


def months_difference_with_grace_period(date_str):
    date_patterns = {
        r'\b\d{2}/\d{2}/\d{4}\b': "%d/%m/%Y",
        r'\b\d{2}-[a-zA-Z]{3}-\d{4}\b': "%d-%b-%Y",
        r'\b\d{4}-\d{2}-\d{2}\b': "%Y-%m-%d",
        r'\b\d{2}[a-zA-Z]{3}\d{2}': "%d%b%y",
        r'\b\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s\d{4}\b': "%d %b %Y",
        r'\b\d{2}\s[a-zA-Z]{3}\s\d{2}\b': "%d %b %y",
        r'\b\d{2}-\d{2}-\d{4}\b': "%d-%m-%Y",
        r'\b\d{2}-\d{1,2}-\d{4}\b': "%d-%m-%Y",
        r'\b\d{1,2}-[a-zA-Z]{3}-\d{2}\b': "%d-%b-%y",
    }

    # Find the correct date format
    for pattern, date_format in date_patterns.items():
        if re.match(pattern, date_str, re.IGNORECASE):
            given_date = datetime.strptime(date_str, date_format)
            break
    else:
        pass

    # Add a grace period of two days
    adjusted_date = given_date + timedelta(days=2)

    # Get today's date
    today = datetime.now()

    # Calculate the difference in months
    month_diff = (today.year - adjusted_date.year) * 12 + today.month - adjusted_date.month

    # Adjust for day difference within the month
    if today.day < adjusted_date.day:
        month_diff -= 1

    return month_diff

def check_dates_and_format_patterns_in_list(date_list):
    date_patterns = {
        r'\b\d{2}/\d{2}/\d{4}\b': "%d/%m/%Y",  # DD/MM/YYYY
        r'\b\d{2}-[a-zA-Z]{3}-\d{4}\b': "%d-%b-%Y",  # DD-MMM-YYYY
        r'\b\d{4}-\d{2}-\d{2}\b': "%Y-%m-%d",  # YYYY-MM-DD
        r'\b\d{2}[a-zA-Z]{3}\d{2}': "%d%b%y",  # DDMMMYY, removed the trailing \b to allow for text following the date
        r'\b\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s\d{4}\b': "%d %b %Y",  # DD MMM YYYY, made the month part case-insensitive
        r'\b\d{2}\s[a-zA-Z]{3}\s\d{2}\b': "%d %b %y",  # DD MMM YY
        r'\b\d{2}-\d{2}-\d{4}\b': "%d-%m-%Y",  # DD-MM-YYYY
        r'\b\d{2}-\d{1,2}-\d{4}\b': "%d-%m-%Y",  # DD-M-YYYY or D-MM-YYYY
        r'\b\d{1,2}-[a-zA-Z]{3}-\d{2}\b': "%d-%b-%y",  # D or DD-MMM-YY
    }

    # Compile the regex with the IGNORECASE flag
    date_regex = re.compile("|".join(date_patterns.keys()), re.IGNORECASE)

    matched_dates = []
    for date in date_list:
        match = date_regex.search(date)
        if match:
            # Find which pattern matched
            for pattern, format_string in date_patterns.items():
                if re.search(pattern, date, re.IGNORECASE):
                    matched_dates.append((date, format_string))
                    break

    return matched_dates

def sort_digits_preserving_order(strings):
    sorted_strings = []

    for s in strings:
        words = s.split()
        digit_words = [word for word in words if '.' in word and word.replace('.', '').replace(',', '').isdigit()]
        non_digit_words = [word for word in words if word not in digit_words]

        sorted_string = ' '.join(non_digit_words + digit_words)
        sorted_strings.append(sorted_string)

    return sorted_strings

def remove_special_characters(input_string):
    # Using list comprehension to filter out non-letter and non-whitespace characters
    filtered_characters = [char for char in input_string if char.isalpha() or char.isspace()]
    
    # Joining the filtered characters back into a string
    return ''.join(filtered_characters)

def split_based_on_dates(text_list):
    joined_text = ' '.join(text_list)

    date_regex = re.compile(
   r'(?<![.\d])(\b\d{2}/\d{2}/\d{4}\b'  # DD/MM/YYYY
    r'|\b\d{2}-[a-zA-Z]{3}-\d{4}\b'  # DD-MMM-YYYY
    r'|\b\d{4}-\d{2}-\d{2}\b'  # YYYY-MM-DD
    r'|\b\d{2}[a-zA-Z]{3}\d{2}\b'  # DDMMMYY
    r'|\b\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}\b'  # D or DD MMM YYYY
    r'|\b\d{2}\s[a-zA-Z]{3}\s\d{2}\b'  # DD MMM YY
    r'|\b\d{2}-\d{2}-\d{4}\b'  # DD-MM-YYYY
    r'|\b\d{2}-\d{1,2}-\d{4}\b'  # DD-M-YYYY or D-MM-YYYY
    r'|\b\d{1,2}-[a-zA-Z]{3}-\d{2}\b)(?![.\d])'
    r'|\b\d{2}\s[a-zA-Z]{3}\s\d{4}\b'   # D or DD-MMM-YY
)

    # Find all matches of date patterns
    matches = [match for match in re.finditer(date_regex, joined_text)]

    if not matches:
        return [joined_text], None  # Return the original text if no dates are found
    
    def determine_format(date_str):
        for fmt in (
    "%d/%m/%Y",  # DD/MM/YYYY
    "%d-%b-%Y",  # DD-MMM-YYYY
    "%Y-%m-%d",  # YYYY-MM-DD
    "%d%b%y",    # DDMMMYY
    "%d %b %Y",  # DD MMM YYYY
    "%d %b %y",  # DD MMM YY
    "%d-%m-%Y",  # DD-MM-YYYY
    "%d-%b-%y",  # DD-MMM-YY
    # Add any other formats that you have in your regex
):
            try:
                datetime.strptime(date_str, fmt)
                return fmt
            except ValueError:
                continue
        return None
   # Function to check if the string is a valid date according to given formats
    def is_valid_date(date_str):
        for fmt in (
            "%d/%m/%Y", "%d-%b-%Y", "%Y-%m-%d", "%d%b%y", "%d %b %Y", "%d %b %y",
            "%d-%m-%Y", "%d-%b-%y", # Add any other formats that you have in your regex
        ):
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        return False
    matches = [match for match in re.finditer(date_regex, joined_text) if is_valid_date(match.group(0))]
    # Determine formats for all matches
    formats = [determine_format(match.group(0)) for match in matches]
    formats=[ele for ele in formats if ele is not None]
    # Find the most common format
    most_common_format = Counter(formats).most_common(1)[0][0]

    # Split the text into segments
    segments = []
    start_index = 0
    for i, match in enumerate(matches):
        end_index = matches[i + 1].start() if i + 1 < len(matches) else len(joined_text)
        segment = joined_text[match.start():end_index].strip()
        segments.append(segment)
        start_index = end_index

    return segments, most_common_format


def rearrange_dates_in_list(text_list):
    """
    Rearranges each element in a list by moving the first date found to the beginning of the string.

    :param text_list: List of strings to be processed.
    :param date_regex: Compiled regular expression to match date patterns.
    :return: List with rearranged strings.
    """
    # Define the date patterns and compile the regex
    date_patterns = r'\b\d{2}/\d{2}/\d{4}\b|\b\d{2}-[a-zA-Z]{3}-\d{4}\b|\b\d{4}-\d{2}-\d{2}\b|\b\d{2}[a-zA-Z]{3}\d{2}\b|\b\d{1,2}\s[a-zA-Z]{3}\s\d{4}\b|\b\d{2}\s[a-zA-Z]{3}\s\d{2}\b'

    date_regex = re.compile(date_patterns)
    rearranged_list = []
    for text in text_list:
        # Find the first date in the string
        match = date_regex.search(text)
        if match:
            # Extract the date and the rest of the string
            date = match.group()
            rest_of_string = text[:match.start()] + text[match.end():]

            # Rearrange the string with the date at the beginning
            rearranged_text = date + " " + rest_of_string
            rearranged_list.append(rearranged_text)
        else:
            # If no date is found, keep the string as is
            rearranged_list.append(text)

    return rearranged_list

def remove_dates_not_matching_format(lst, date_format):
    # Compile a regex pattern to match potential dates (broadly)
    date_regex = re.compile(r'\b\d{1,2}[-./]\d{1,2}[-./]\d{2,4}\b|\b\d{1,2}\s[a-zA-Z]{3}\s\d{2,4}\b')

    def check_format(date_str, format):
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False

    def process_string(s):
        matches = date_regex.findall(s)
        for match in matches:
            # Remove the date if it doesn't match the format
            if not check_format(match, date_format):
                s = s.replace(match, '')
        return s

    return [process_string(element) for element in lst]

def remove_word_name(s):
    # The pattern matches 'name' in any case (lowercase, uppercase, mixed)
    pattern = r'\b[nameNAME]+\b'
    
    # Replace the word 'name' with an empty string
    return re.sub(pattern, '', s, flags=re.IGNORECASE)

def remove_word_po(s):
    # The pattern matches 'name' in any case (lowercase, uppercase, mixed)
    pattern = r'\b[poPO]+\b'
    
    # Replace the word 'name' with an empty string
    return re.sub(pattern, '', s, flags=re.IGNORECASE)


# def extract_name(lst):
    
#     Name=[ele for ele in lst if( 'name'  in ele.lower() ) and (':' in ele)]
#     if len(Name)>0:
#         return [s for s in [remove_word_name(ele).replace(':','').strip() for ele in Name ] if s.isupper()][0]
    
# #     elif len([ele.replace('.','') for ele in plain_text_data if( 'p.o.'  in ele.lower() ) ])>0:
# #         Name=[ele.replace('.','') for ele in plain_text_data if( 'p.o.'  in ele.lower() ) ]
# #         return [ele.lower().split('po')[0].strip() for ele in Name][0]
#     else:
#         try:
#             Name=[s for s in lst if s.isupper() and not any(char.isdigit() for char in s) and len(s) > 4 and not any(word in s.lower() for word in ['account', 'statement', 'branch', 'bank','emirates','aed','currency'])]
#             if len(Name)==1:
#                 return Name[0]
#             else:
#                 return [element for element in Name if len(element) == max(len(e) for e in Name)][0]
#         except:
#             return None


def extract_name(lst):
    try:
        # Look for patterns like Mr., Ms., Mrs. followed by a name (until a digit is encountered)
        name_candidates = []
        for ele in lst:
            words = ele.lower().split()
            for i, word in enumerate(words):
                match = re.match(r'(mr\.?|ms\.?|mrs\.?)', word)
                if match:
                    name = ' '.join(words[i:i+3])  # Assuming a name might consist of max three words
                    if any(char.isdigit() for char in name):
                        break
                    name_candidates.append(name.title())  # Convert the name to title case

        if name_candidates:
            return name_candidates[0]  # Returning the first extracted name
        else:
            # If no explicit title prefix is found, attempt to find an all-uppercase name
            potential_names = [s for s in lst if s.isupper() and not any(char.isdigit() for char in s)]
            for name in potential_names:
                if not any(word in name.lower() for word in ['account', 'statement', 'branch', 'bank', 'emirates', 'aed', 'currency', 'uae dirham', 'postpay']):
                    if name.lower()!='account name' or 'account statement':
                        return name.title()  # Convert the name to title case and return
                
            data = ','.join(lst)
  
            ## handle mashreq case
            if 'mashreq' in data.lower():
         
                keyword = 'statement for period'

                # Find the index where the keyword appears
                keyword_index = None
                for i, elem in enumerate(lst):
                    if keyword in elem.lower():
                        keyword_index = i
                        break

                if keyword_index is not None and keyword_index > 0:
                    # Extract the element before the keyword
                    cleaned_potential_name = lst[keyword_index - 1]
                    if cleaned_potential_name:
                        return cleaned_potential_name
            
            # If still no name is found, look for 'Name' keyword - ### ENBD bank     
            for ele in lst:
                # print(f"\n\nele: {ele}")
                if 'name' in ele.lower():
                    to_index = ele.lower().index('name')

                    # Extracting the substring after 'To'
                    potential_name = ele[to_index:].strip()
                    potential_name = potential_name.lower().replace("name", "").replace(":", "")
                    potential_name = potential_name.split()[:4]
                    potential_name = ' '.join(potential_name)
                    cleaned_potential_name = potential_name.title()

                    if cleaned_potential_name:
                        return cleaned_potential_name
                    
            # If still no name is found, try extracting from 'Account No' information - ### DIB bank
            for ele in lst:
                # print(f"\n\nele: {ele}")
                if 'account no' in ele.lower():
  
                    account_index = ele.lower().index('account no')
                    # branch_index = ele.lower().index('branch')

                    # Extracting the substring between 'branch' and 'Account No'
                    potential_name = ele[:account_index].strip()
                    cleaned_potential_name = potential_name.title()

                    if cleaned_potential_name:
                        return cleaned_potential_name
            
            # If still no name is found, look for 'Villa/Flat No' information - ### Alhilal bank
            for ele in lst:
                # print(f"\n\nele: {ele}")
                if 'villa/flat no' in ele.lower():
                    villa_index = ele.lower().index('villa/flat no')

                    # Extracting the substring before 'Villa/Flat No'
                    potential_name = ele[:villa_index].strip()
                    cleaned_potential_name = potential_name.title()

                    if cleaned_potential_name:
                        return cleaned_potential_name
                    
            # If still no name is found, look for 'balance carried forward' - ### FAB bank     
            for i, ele in enumerate(lst):
                # print(f"\n\nele: {ele}")
                if 'balance carried forward' in ele.lower():
                    # Extract the subsequent words but limit to 3 words and remove digits
                    next_words = lst[i+1:i+2]  # Extracting the next 3 words after 'balance carried forward'
       
                    potential_name = ' '.join(next_words)
                    potential_name = potential_name.split(' ')
                    potential_name = ' '.join(potential_name[:4])
                    potential_name = re.sub(r'\d+', '', potential_name)  # Remove digits
                    cleaned_potential_name = potential_name.title()

                    if cleaned_potential_name:
                        return cleaned_potential_name
            
            # If still no name is found, look for 'To' keyword - ### CBD bank     
            for ele in lst:
                # print(f"\n\nele: {ele}")
                if 'to' in ele.lower():
                    to_index = ele.lower().index('to')

                    # Extracting the substring after 'To'
                    potential_name = ele[to_index:].strip()
                    potential_name = potential_name.lower().replace("to", "")
                    potential_name = potential_name.split()[:3]
                    potential_name = ' '.join(potential_name)
                    cleaned_potential_name = potential_name.title()

                    if cleaned_potential_name:
                        return cleaned_potential_name

            # If still no name is found, look for 'PO Box' - ### ADIB bank     
            pattern = re.compile(r'(?P<name>.+)(?=p[.\s]*o[.\s]*\s*box)', re.IGNORECASE)
            for ele in lst:
                # print(f"\n\nele: {ele}")
                match = re.search(pattern, ele)
                if match:
                    potential_name = match.group().strip()
                    potential_name = re.sub(r'\d+', '', potential_name)  # Remove digits
                    cleaned_potential_name = potential_name.title()

                    if cleaned_potential_name:
                        return cleaned_potential_name

        return None  # If no name is found
    except:
        return None

def validate_name(eid_name, extracted_name):
            threshold = 65
            similarity = fuzz.token_sort_ratio(eid_name, extracted_name)
            return similarity >= threshold

def limit_string_to_tokens(data, limit):
    tokens = data.split()  # Split the string into tokens
    limited_tokens = tokens[:limit]  # Select the tokens up to the limit
    limited_data = ' '.join(limited_tokens)  # Join the limited tokens back into a string
    return limited_data


def extract_digits_from_gpt_resp(s):
    """
    Extracts digits from a given string and returns the number.
    """
    salary_pattern = r'Salary:\s*(.*)'
    s=re.search(salary_pattern,s ).group(1)
        
    # Extract digits and decimal points
    digits = ''.join([char for char in s if char.isdigit() or char == '.'])

    # Convert the extracted string to a number
    if digits:
        return float(digits)
    else:
        return 0
    

def extract_name_from_gpt_resp(text):
    name_pattern = r'Name:\s*(.*)'  # Regex pattern for extracting name

    name_match = re.search(name_pattern, text)
   
    name = name_match.group(1) if name_match else None
    
    if name and name.lower() == 'not available in the given data':
        name = None

    return name

def determine_order(date_list):
    dates = []
    
    date_formats = ["%d/%m/%Y", "%d-%b-%Y", "%Y-%m-%d", "%d%b%y", "%d %b %Y", "%d %b %y", "%d-%m-%Y", "%d-%b-%y"]

    for s in date_list:
        for fmt in date_formats:
            date_pattern = fmt.replace('%d', r'(\d{2})').replace('%b', r'(\w{3})').replace('%Y', r'(\d{4})').replace('%y', r'(\d{2})').replace('%m', r'(\d{2})')
            match = re.search(date_pattern, s)
            if match:
                date_str = match.group()
                try:
                    date = datetime.strptime(date_str, fmt)
                    dates.append(date)
                    break  # Break the inner loop if a date is found
                except ValueError:
                    continue  # Try the next format if the current one fails

    if not dates:
        return "No valid dates found or format mismatch"

    # Checking the order of the dates
    if all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1)):
        return "Ascending"
    elif all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1)):
        return "Descending"
    else:
        return "Not sorted"


def parse_date_from_start(string, date_format):
    date_length = len(datetime.now().strftime(date_format))
    try:
        return datetime.strptime(string[:date_length], date_format)
    except ValueError:
        return None

def sort_list_by_date(lst, date_format, order='Ascending'):
    # Add an index to each element to track its original position
    indexed_lst = [(ele, idx) for idx, ele in enumerate(lst)]

    # Determine the secondary sort key based on the order
    secondary_sort_key = -1 if order == 'Descending' else 1

    # Sort in ascending order by date, then by original index or its reverse based on the order
    filtered_sorted_list = sorted(
        indexed_lst,
        key=lambda x: (parse_date_from_start(x[0], date_format) or datetime.min, secondary_sort_key * x[1])
    )

    # Extract and return only the elements from the sorted list
    return [ele for ele, idx in filtered_sorted_list]


# def extract_elements_with_date(lst, date_format):
#     extracted_elements = []
#     date_pattern = date_format.replace('%d', r'(\d{2})').replace('%m', r'(\d{2})').replace('%Y', r'(\d{4})')

#     for s in lst:
#         match = re.match(date_pattern, s)
#         if match:
#             date_str = match.group()
#             try:
#                 # Try parsing the date
#                 datetime.strptime(date_str, date_format)
#                 extracted_elements.append(s)
#             except ValueError:
#                 continue  # Skip entries that don't match the format

#     return extracted_elements

def extract_liquidity(s):
    # Find all numbers with decimal points
    numbers_with_decimal = re.findall(r'\d+(?:,\d{3})*\.\d+', s)
    
    # Return the last number found, if any
    return numbers_with_decimal[-1] if numbers_with_decimal else None

def filter_elements_with_decimal_digit(lst):

    decimal_number_pattern = re.compile(r'\b\d+\.\d+\b')

    return [s for s in lst if decimal_number_pattern.search(s)]

def extract_date_from_string(string, date_format):
    date_length = len(datetime.now().strftime(date_format))
    for i in range(len(string) - date_length + 1):
        substring = string[i:i + date_length]
        try:
            parsed_date = datetime.strptime(substring, date_format)
            return parsed_date.strftime(date_format)
        except ValueError:
            continue
    return None

def extract_salary(s):
    # Find all numbers with decimal points
    numbers_with_decimal = [ele for ele in re.findall(r'\d+(?:,\d{3})*\.\d+', s) if ele!='0.00']
    
    if len (numbers_with_decimal )==3:
        return numbers_with_decimal[1] 
    
    elif len (numbers_with_decimal )<=2:
        return numbers_with_decimal[0] 
    
    else:
        return ''
    


def extract_elements_with_specific_date_format(lst, input_date_format):
    extracted_elements = []
    date_formats = ["%d/%m/%Y", "%d-%b-%Y", "%Y-%m-%d", "%d%b%y", "%d %b %Y", "%d %b %y", "%d-%m-%Y", "%d-%b-%y"]


    # Check if the input date format is in the list of date formats
    if input_date_format not in date_formats:
        return extracted_elements  # Return empty list if format not found

    # Convert the input date format to a regex pattern
    date_pattern = r'\b' + input_date_format.replace('%d', r'(\d{2})')\
                                           .replace('%m', r'(\d{2})')\
                                           .replace('%Y', r'(\d{4})')\
                                           .replace('%b', r'([A-Za-z]{3})')\
                                           .replace('%y', r'(\d{2})') + r'\b'

    for s in lst:
        match = re.search(date_pattern, s)
        if match:
            date_str = match.group()
            try:
                # Try parsing the date
                datetime.strptime(date_str, input_date_format)
                extracted_elements.append(s)
            except ValueError:
                continue  # Skip entries that don't match the format

    return extracted_elements

def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "Unknown"

def extract_text_from_image(client, image_base64):
    image_bytes = base64.b64decode(image_base64)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    image_content = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    _, image_bytes = cv2.imencode('.png', image_content)

    image = vision_v1.types.Image(content=image_bytes.tobytes())
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description

def get_scanned_pdf_text(client, doc):
    text = ''
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        # Convert each page to an image
        pix = page.get_pixmap()
        image = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, -1))

        _, image_bytes = cv2.imencode('.png', image)
        image_base64 = base64.b64encode(image_bytes.tobytes()).decode('utf-8')

        page_text = extract_text_from_image(client, image_base64)
        text += page_text
    
    return text

def perform_data_extraction(client, pdf_bytes):
    try:
        doc = fitz.open("pdf", pdf_bytes)
        # Extract text from each page
        text = ''
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        
        ## scanned invoice
        if not text:
            text = get_scanned_pdf_text(client, doc)

        return text
    
    except Exception as e:
        text = get_scanned_pdf_text(client, doc)
        if text:
            return text
        else:
            return str(e)

def hijri_to_gregorian(hijri_date):
    try:
        day, month, year = map(int, hijri_date.split('/'))

        gregorian_date = convert.Hijri(year, month, day).to_gregorian()
    
        return f"{gregorian_date.day:02}/{gregorian_date.month:02}/{gregorian_date.year}"
    except:
        return hijri_date
    
def clean_and_convert_date(date_str):
    cleaned_date_str = re.sub(r'[^\d/]', '', date_str)
    try:
        date_obj = datetime.strptime(cleaned_date_str, "%d/%m/%Y")
        formatted_date_str = date_obj.strftime("%d/%m/%Y")
        gregorian_date = hijri_to_gregorian(formatted_date_str)
        return gregorian_date
    except ValueError:
        return date_str

def eastern_arabic_to_english(eastern_numeral):
    try:
        arabic_to_english_map = {
            '٠': '0', '۰': '0',
            '١': '1', '۱': '1',
            '٢': '2', '۲': '2',
            '٣': '3', '۳': '3',
            '٤': '4', '۴': '4',
            '٥': '5', '۵': '5',
            '٦': '6', '۶': '6',
            '٧': '7', '۷': '7',
            '٨': '8', '۸': '8',
            '٩': '9', '۹': '9',
            '/': '/'
        }

        english_numeral = ''.join([arabic_to_english_map[char] if char in arabic_to_english_map else char for char in eastern_numeral])
        
        return english_numeral

    except:
        return eastern_numeral

def clean_salary(salary):
    cleaned_salary = ''.join(char for char in salary if char.isdigit() or char in {',', '.'})
    return cleaned_salary
