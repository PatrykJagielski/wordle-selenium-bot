from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

NUM_OF_LETTERS = 11

def clear_row(element):
    for _ in range(NUM_OF_LETTERS):
        element.send_keys(Keys.BACKSPACE)

def send_row(element, word, d):
    for letter in word:
        if letter in u'ąćęłńóśźż':
            key = d.find_element(by=By.XPATH, value=f"//*[contains(text(), '{letter.upper()}')]")
            key.click()
        else:
            element.send_keys(letter)
    sleep(0.1)
    element.send_keys(Keys.RETURN)

def best_matches(words):
    freq = {
        'a': 0, 'ą': 0, 'b': 0, 'c': 0, 'ć': 0, 'd': 0, 'e': 0, 'ę': 0,
        'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'ł': 0,
        'm': 0, 'n': 0, 'ń': 0, 'o': 0, 'ó': 0, 'p': 0, 'q': 0, 'r': 0,
        's': 0, 'ś': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0,
        'z': 0, 'ź': 0, 'ż': 0
    }
    letter_count = 0

    for word in words:
        for letter in word:
            freq[letter] += 1
            letter_count += 1

    normalized = {}
    for letter, count in freq.items():
        normalized[letter] = count / letter_count

    bests = {}
    for word in words:
        bests[word] = sum(normalized[c] / word.count(c) for c in word)

    return sorted(bests.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    best_opener = 'ikona'
    if NUM_OF_LETTERS == 11:
        best_opener = 'wieczorynka'
    
    driver = webdriver.Chrome()
    driver.get(f'https://wordleplay.com/pl/{NUM_OF_LETTERS}-letter-words')
    driver.implicitly_wait(1)
    body = driver.find_element(by=By.TAG_NAME, value='body')
    sleep(1)

    body.send_keys(best_opener)
    body.send_keys(Keys.RETURN)
    first_row = driver.find_element(by=By.CLASS_NAME, value='Row-locked-in')

    exclude_letters = ''
    elsewhere = {}
    match_letters = {}

    for i, sqr in enumerate(first_row.find_elements(by=By.TAG_NAME, value='td')):
        letter, label = sqr.get_attribute('aria-label').split()
        letter = letter[0].lower()
        if label == 'no':
            exclude_letters += letter
        elif label == 'elsewhere':
            elsewhere[letter] = [i]
        else:
            match_letters[i] = letter

    # GAME LOOP
    while True:
        words = []

        with open(f'{NUM_OF_LETTERS}.txt') as file:
            for line in file:
                if all(line[i] == l for i, l in match_letters.items()) and \
                        all(c not in exclude_letters for i, c in enumerate(line[:-1]) if i not in match_letters.keys()) and \
                        all(i not in elsewhere.get(l, []) for i, l in enumerate(line[:-1])) and \
                        all(c in line for c in elsewhere.keys()):
                    words.append(line[:-1])

        bests = list(best_matches(words))
        print(bests[:20])
        
        for best in bests:
            send_row(body, best[0], driver)
            print(best[0])
            fail = driver.find_elements(by=By.CLASS_NAME, value='Hint-background')
            if fail:
                clear_row(body)
                sleep(3)
            else:
                break
        
        win = driver.find_elements(by=By.CLASS_NAME, value='Top-window-frame')
        if win:
            sleep(3)
            driver.close()
            break

        last_row = driver.find_elements(by=By.CLASS_NAME, value='Row-locked-in')[-1]

        for i, sqr in enumerate(last_row.find_elements(by=By.TAG_NAME, value='td')):
            letter, label = sqr.get_attribute('aria-label').split()
            letter = letter[0].lower()
            if label == 'no':
                exclude_letters += letter
            elif label == 'elsewhere':
                if letter in elsewhere.keys():
                    elsewhere[letter] += [i]
                else:
                    elsewhere[letter] = [i]
            else:
                match_letters[i] = letter
