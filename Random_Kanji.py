# Selects a random kanji from a dictionary text file
# Gets information on kanji from jisho.org and displays in command line or a window

from bs4 import BeautifulSoup
import requests, random, time, codecs, tkinter


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


# Get kanji from dictionary file
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


# Pulls info from jisho.org
def kanji_info_get(kanji):
    '''This will return'''
    #1. The kanji
    #2. Kanji meanings
    #3. Stroke count
    #4. On/kun readings
    #5. Common words containing the kanji
    
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
                common_words[word] = [reading, meaning]
            except AttributeError:
                pass

        return [kanji, meanings, strokes, kanji_readings, common_words]


# Prints kanji info in command line
def kanji_info_print(kanji_data):
    if (kanji_data == None):
        return
    print()
    print("~"*70)
    print("Kanji:", kanji_data[0])
    print("Meanings:", kanji_data[1])
    print("Stroke Count:", kanji_data[2])
    print("On Readings:", kanji_data[3]["on"])
    print("Kun Readings:", kanji_data[3]["kun"])
    print()
    print("Common Words:")
    for word, info in kanji_data[4].items():
        print(word + " (" + info[0] + "): " + info[1])
    print("~"*70)


# Displays kanji info in a window
def kanji_page_show(kanji_data):
    root = tkinter.Tk()
    root.title("Kanji Information")
    root.geometry("800x900")

    root_scroll = tkinter.Scrollbar(root)
    root_scroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)

    kanji_message = tkinter.Message(root, text = kanji_data[0])
    kanji_message.config(font = ("times", 150, "bold"))
    kanji_message.pack(fill = tkinter.X)

    on_label = tkinter.Label(root, text = kanji_data[3]["on"])
    on_label.config(font = ("times", 20, ""))
    on_label.pack()

    kun_label = tkinter.Label(root, text = kanji_data[3]["kun"])
    kun_label.config(font = ("times", 20, ""))
    kun_label.pack()

    stroke_label = tkinter.Label(root, text = "Strokes: " + kanji_data[2])
    stroke_label.config(font = ("times", 20, ""))
    stroke_label.pack()

    meaning_label = tkinter.Label(root, text = "Meanings: " + kanji_data[1] + "\n")
    meaning_label.config(font = ("times", 20, ""))
    meaning_label.pack()

    root_scroll = tkinter.Scrollbar(root)
    root_scroll.pack(side = tkinter.RIGHT)
    
    common_lb = tkinter.Listbox(root, yscrollcommand = root_scroll.set)
    common_lb.insert(tkinter.END, "Common Words")
    for key, value in kanji_data[4].items():
        common_lb.insert(tkinter.END, key + " (" + str(value[0]) + "): " + str(value[1]))
    common_lb.config(font = ("times", 20, ""))
    common_lb.pack(fill = tkinter.BOTH)
    
    root_scroll.config(command = common_lb.yview)

    root.mainloop()


def main():
    menu_choice = str()
    while (menu_choice != "3"):
        print("1. Get random kanji info (text version)")
        print("2. Get random kanji info (graphical version)")
        print("3. Quit")
        menu_choice = input("Selection: ").strip()
        if (menu_choice == "1"):
            kanji_info_print(kanji_info_get(kanji_get()))
        elif (menu_choice == "2"):
            kanji_page_show(kanji_info_get(kanji_get()))
        print()
    print("Goodbye")

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''        
'''
# Pulled 常用漢字 from wikipedia
wiki_soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_jōyō_kanji").text, "lxml")

with codecs.open("KanjiDictionary.txt", "w", encoding = "utf-8") as kd:
    for a in wiki_soup.find_all("a", class_ = "extiw"):
        kd.write(a.text.strip()[0])
'''
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

main()
