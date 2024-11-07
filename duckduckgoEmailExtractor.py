from seleniumbase import Driver
import re
import time
import random
import mmap


query_ = input('Do you have a search string? (Yes or No) ')
valid_data = False
while not valid_data:
    if query_.isalpha():
        if query_.lower() == 'yes':
            valid_data = True
        elif query_.lower() == 'no':
            valid_data = True
        else:
            print('Please answer correctly! (Yes or No)\n')
            query_ = input('Do you have a search string? (Yes or No) ')
    else:
        print('Please answer correctly! (Yes or No)\n')
        query_ = input('Do you have a search string? (Yes or No) ')
if query_.lower() == 'yes':
    search_string = input('Input the search string ')
elif query_.lower() == 'no':
    ticker = input('Please input the email domain. Eg gmail, yahoo, outlook etc ' )
    site_domain_name = input('Please input the site domain name or url. Eg facebook.com, linkedin.com etc ')
    country =  input('Please input the country. Eg United States, Italy etc ')
    city_state = input('Please input the city and state or just state. Eg california, or New York, New York etc ')
    occupation = input('Please input the occupation. Eg CEO, founder, receptionist etc ')
    search_string = f'site:{site_domain_name} "{occupation}" "{city_state}, {country}" "@{ticker}.com"'

email_list = []

def email1_parse():
    contain_emails = driver.find_elements('.kY2IgmnCmOGjharHErah')
    for contents in contain_emails:
        text_emails = contents.text
        if f'@' in text_emails:
            regex_pattern = r'[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}'
            try:
                email_match = re.search(regex_pattern, text_emails).group()
                if email_match not in email_list:
                    email_list.append(email_match)
                time.sleep(random.randint(1,2))
            except:
                continue

try:
    driver = Driver(uc=True, incognito=True)
    url = "https://duckduckgo.com/"
    driver.uc_open_with_reconnect(url,5)
    driver.implicitly_wait(15)
    driver.wait_for_element('.footer_aboutHeading__JZ81k',timeout=20)
    driver.uc_gui_write(search_string)
    time.sleep(random.randint(4,7))
    driver.uc_click(".searchbox_searchButton__F5Bwq")
    time.sleep(random.randint(8,11))

    number_of_pages = 1
    counter = 1
    while True:
        try:
            driver.wait_for_element('#more-results',timeout=16)
        except:
            pass
        while counter < 6:
            driver.execute_script('window.scrollBy(0,250)','')
            if counter == 4:
                driver.execute_script('window.scrollBy(0,document.body.scrollHeight)')
            elif counter == 5:
                counter = 1
                break
            time.sleep(random.randint(2, 4))
            counter += 1
        try:
            driver.uc_click("#more-results")
            number_of_pages += 1
            time.sleep(random.randint(2,4))
        except:
            break
    email1_parse()
finally:
    driver.quit()

email_input_counter = 0
email_found_counter = 0
with open('emailsDuckduckgo.txt', 'a') as emails_txt:
    try:
        with open(r'emailsDuckduckgo.txt', 'rb') as file:
            s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            for email in email_list:
                if s.find(bytes(email,encoding='utf-8')) == -1:
                    emails_txt.write(email + '\n')
                    email_input_counter += 1
                else:
                    email_found_counter += 1
    except:
        emails_txt.write('!!! This is file contains emails !!!\n')
        print('###############')
        print('Please run the script again!!!')
        print('###############\n')

print(f'scraped {str(len(email_list))} emails from {str(number_of_pages)} search pages')
print(f'added {email_input_counter} emails to emailsDuckduckgo.txt')
print(f'found {email_found_counter} emails to be existing in the emailsDuckduckgo.txt')