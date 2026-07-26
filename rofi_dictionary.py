# main.py

from subprocess import run, Popen, PIPE
from rapidfuzz import process, fuzz
import re, json, os

from providers.factory import ProviderFactory
from services.dictionary_service import DictionaryService
from models.dictionary_entry import Definition


def build_service() -> DictionaryService:
    provider = ProviderFactory.create("sqlite_2_provider")
    return DictionaryService(provider)
####################################

def split_string(s, skip):
    """
    Splits a string with \n every skip characters. Will avoid breaking words.

    Parameters:
    s (String): The string to split.
    skip (Integer): How often to split in characters.

    Returns:
    String: The split string.
    """
    words = s.split()
    current_len = 0
    result = []

    for word in words:
        if current_len + len(word) > skip:
            result.append(f'\n{word}')
            current_len = len(word)
        else:
            result.append(f'{word}')
            current_len += len(word)

    return " ".join(result)

class RofiApp:
    def __init__(self):
        # Some utils.
        # States: 
        #  -1: 'EXIT'
        #   0: 'WORD_404'
        #   1: 'DEFINE'
        #   2: 'CATEGORIES'
        #   3: 'DEFINITIONS'
        #   4: 'DETAILED_DEF'
        self.filepath = os.path.dirname(os.path.realpath(__file__))
        #with open(f"{self.filepath}/data/config.json", 'r') as f:
        #    self.config = json.load(f)

        self.state = 1
        self.rofi_command = ['rofi', '-dmenu', '-lines', '10', '-no-fixed-num-lines', '-i']
        self.pattern = re.compile(r"(\d+):")
        #self.api_req = ApiRequester()

        #call get word
        self.service = build_service()   #lookup word using 

    def display_menu(self, menu, title, back_msg, prev_state, next_state):
        """
        Displays a menu to the user.

        Parameters:
        menu (list): The menu list.
        title (String): The prompt title to show.
        back_msg (String): The message to show as the back entry.
        prev_state (Integer): The next state to go to if the user moves backward.
        next_state (Integer): The next state to go to if the user moves forward.

        Return:
        Integer: The index of the menu option chosen, -1 if to go back, None if none chosen.
        """
        rofi_input = back_msg + "\n" + "\n".join(menu)
        echo = Popen(["echo", rofi_input], stdout=PIPE)
        result = run(self.rofi_command + ['-no-custom', '-p', title], stdin=echo.stdout, capture_output=True, text=True).stdout.strip()
        echo.stdout.close()

        if back_msg == result:
            self.state = prev_state;
            return -1
        elif match := self.pattern.match(result):
            self.state = next_state;
            return int(match.group(1))
        else:
            self.state = -1
            return -1

    def run(self):
        """
        Runs the app until the user exits.
        """
        # These are used to remember the choices made in previous states when going back.

        query = ''
        part_of_speech = []
        defns_choice = 0
        defn_choice = 0 
        defns: list[Definition] = []

        while self.state != -1:
            if self.state == 0:
                # WORD_404 State - Word not found, try fuzzy search.
                with open(f'{self.filepath}/data/dictionary.json', 'r') as f:
                    words = json.load(f)["words"]
                    closest_words = process.extract(query, words, limit=3, scorer=fuzz.ratio)
                    options = [f"{idx}: {r[0]}" for idx, r in enumerate(closest_words)]

                choice = self.display_menu(options, f"ERR: Could not find \"{query}\". Did you mean:", "⬅ Go back.", 1, 2)
                if choice != -1:
                    query = closest_words[choice][0]
                    self.entry = self.service.lookup(query) #self.api_req.query(query) todo

            elif self.state == 1:
                # DEFINE State - Ask user for word.
                try:
                    result = run(self.rofi_command + ['-p', 'define:'], capture_output=True, text=True)
                    query = result.stdout.strip().lower()
                    #self.api_req.query(query) #gets the word from api call
                    self.entry = self.service.lookup(query) #self.api_req.query(query) todo

                    if query == '':
                        self.state = -1
                    elif len(self.entry.definitions) == 0:
                        self.state = 0
                    else:
                        self.state = 2
                except KeyError:
                    if query != '':
                        self.state = 0
                    else:
                        self.state = -1

            elif self.state == 2:
                # CATEGORIES State - Show lexical categories of definitions.
                # categories = self.api_req.get_results_preview()

                part_of_speech = self.entry.get_part_of_speech()

                #build list w/ index (0: )
                categories = [f"{idx}: {c}" for idx, c in enumerate(part_of_speech)]
                defns_choice = self.display_menu(categories, query, "⬅ Go back.", 1, 3)

            elif self.state == 3:
                # DEFINITIONS State- Show definitions for selected part_of_speech
                # todo implement Dictionary get_part_of_speech_definitions
                # print(self.entry.get_definitions_part_of_speech(part_of_speech[defns_choice]))

                defns = self.entry.get_definitions_part_of_speech(part_of_speech[defns_choice])
                #defns = self.api_req.get_senses_definitions(defns_choice, self.config['num_defns'])['definitions']
                fdefns = [f"{idx}: {d.get_definition()}" for idx, d in enumerate(defns)]
                defn_choice = self.display_menu(fdefns, query, "⬅ Go back.", 2, 4)

            elif self.state == 4:
                # DETAILED_DEF State - Show a selected definition in the window.
                defn = defns[defn_choice]

                # Split defn every so many characters to make space.
                #todo = self.config['chars_per_line'] #todo
                #defn = split_string(defn, skip)

                choice = self.display_menu([defn.get_definition()], query,"⬅ Go back.", 3, 4)

if __name__ == '__main__':
    app = RofiApp()
    app.run()





###################################
""" def main():
    service = build_service()

    while True:
        word = input("\nWord (Q=quit): ").strip()

        if word.upper() == "Q":
            break

        entry = service.lookup(word)

        if entry is None:
            print(f"No definition found for {word}")
        else:
            print()
            print(entry.display())
        

if __name__ == "__main__":
    main()

 """
