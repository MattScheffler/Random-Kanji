# Program Goal:
# Select a random kanji from a dictionary of 常用漢字
# Return kanji information and common words using it from jisho.org
# Will eventually use tkinter to display info

from bs4 import BeautifulSoup
import requests, random, time, codecs #, tkinter

# Use requests to get webpage
def page_get(web_page):
    timeout_count = 0
    timeout_check = False
    while not(timeout_check):
        try:
            jisho_page = requests.get(web_page, timeout = 5)
            timeout_check = True
        except Exception:
            if (timeout_count >= 3):
                return None
            timeout_count += 1
            time.sleep(3)
    return jisho_page


# Get kanji to search for from dictionary file
def kanji_get():
    with codecs.open("KanjiDictionary.txt", "r", encoding = "utf-8") as kd:
        for line_count, line in enumerate(kd, start = 1):
            pass
        kanji_select = random.choice(range(0, line_count))
        kd.seek(0)
        for n in range(0, kanji_select):
            kd.readline()
        random_kanji = kd.readline().strip()
    return random_kanji


# Gets a random kanji and pulls info from jisho
def kanji_info_get(kanji):
    '''List of kanji info to get'''
    #1. Common words
    #2. On/Kun readings (#kanji page)
    #3. Stroke count (#kanji page)
    #4. Meanings (#kanji page)
    
    '''Kanji page'''
    # https://jisho.org/search/[KANJI]%20%23kanji
    '''Common words page'''
    # https://jisho.org/search/%23word%20%23common%20%3F*[KANJI]
    
    kanji_page = "https://jisho.org/search/" + kanji + "%20%23kanji"
    common_page = "https://jisho.org/search/%23word%20%23common%20*" + kanji + "*"
    common_page_result = page_get(common_page)
    kanji_page_result = page_get(kanji_page)
    
    if (common_page_result == None):
        return None
    elif (kanji_page_result == None):
        return None
    else:
        common_soup = BeautifulSoup(common_page_result.text, "lxml")
        kanji_soup = BeautifulSoup(kanji_page_result.text, "lxml")

        # Kanji meanings
        meanings = kanji_soup.find("div", class_ = \
                                   "kanji-details__main-meanings").text.strip()
        
        # Stroke count
        strokes = kanji_soup.find("div", class_ = \
                                  "kanji-details__stroke_count").text.strip()

        # on/kun readings
        kanji_readings = {"on":[], "kun":[]}
        try:
            kun_yomi = kanji_soup.find("dl", class_ = "dictionary_entry kun_yomi")
            for a in kun_yomi.find_all("a"):
                kanji_readings["kun"] += a
        except Exception:
            pass
        try:
            on_yomi = kanji_soup.find_all("dl", class_ = "dictionary_entry on_yomi")
            for index,dl in enumerate(on_yomi):
                if (index == 2):
                    for a in dl.find_all("a"):
                        kanji_readings["on"] += a
        except Exception:
            pass

        # Common Words
        common_words = {}
        common_divs = common_soup.find_all("div", class_ = "concept_light clearfix")
        for div in common_divs:
            try:
                word = div.find("span", class_ = "text").string.strip()
                reading = div.find("span", class_ = "furigana").text.strip()
                meaning = div.find("span", class_ = "meaning-meaning").text.strip()
                common_words[word] = [[reading],[meaning]]
            except AttributeError:
                pass

        return [kanji, meanings, strokes, kanji_readings, common_words]


# Test function to print kanji info in command line
def kanji_info_print(kanji_data):
    print("Kanji:", kanji_data[0])
    print("Meanings:", kanji_data[1])
    print("Stroke Count:", kanji_data[2])
    print("On Readings:", kanji_data[3]["on"])
    print("Kun Readings:", kanji_data[3]["kun"])
    print()
    print("Common Words:")
    for word, info in kanji_data[4].items():
        print(word + ":", info)


# Takes in information from kanji_info_get() and displays it in a window
def kanji_page_show():
    pass


def main():
    menu_choice = str()
    while (menu_choice != "2"):
        print("1. Get random kanji info")
        print("2. Quit")
        menu_choice = input("Selection: ")
        if (menu_choice == "1"):
            print("~"*50)
            kanji_info_print(kanji_info_get(kanji_get()))
            print("~"*50)
        print()
    print("Goodbye")
        
'''
# Pulled 常用漢字 from wikipedia
wiki_soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_jōyō_kanji").text, "lxml")

with codecs.open("KanjiDictionary2.txt", "w", encoding = "utf-8") as kd:
    for a in wiki_soup.find_all("a", class_ = "extiw"):
        kd.write(a.text.strip()[0])
'''

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''


#kanji_info_print(kanji_info_get(kanji_get()))
main()
