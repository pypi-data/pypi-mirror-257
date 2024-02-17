import pymorphy2
import csv
import string
import pkg_resources
import os

class Borrowed:
    def __init__(self, words, found_borrowed):
        self._dict = dict(sorted(found_borrowed.items(), key=lambda x: x[1].get("Repeats", 1), reverse=True))  # order by repeats
        self._len = len(words)
        self._bor = sum(len(value["Instances"]) for value in found_borrowed.values())
        self._percent = round(self._bor / self._len * 100, 2)

    @property
    def dict(self):
        return self._dict

    @property
    def len(self):
        return self._len

    @property
    def bor(self):
        return self._bor

    @property
    def percent(self):
        return self._percent


def extract(the_text=None, output_file=None):
    morph = pymorphy2.MorphAnalyzer()
    borrowed_dictionary = pkg_resources.resource_filename(__name__, 'borrowed_dictionary.csv')
    
    words = [] # read words from the original text file
    if the_text.endswith(".txt"):
        expanded_file_path = os.path.expanduser(the_text)
        with open(expanded_file_path, "r") as file:
            for line in file:
                cleaned_line = ''
                for char in line.replace('ё', 'е'): #pymorphy dictionary not using ё!
                    if char.isalnum() or char == '-': #keep alphanumeric or '-' as it might be part of a word
                        cleaned_line += char
                    else:
                        cleaned_line += ' '
                words.extend(cleaned_line.split())
    else: 
        cleaned_text = the_text.replace('ё', 'е')  # replace 'ё' with 'е'
        cleaned_text = cleaned_text.translate(str.maketrans('', '', string.punctuation.replace('-', '')))  # remove punctuation, excluding '-'
        words.extend(cleaned_text.split())

    # normalize words
    normalized_words = {}
    for word in words:
        normalized_word = morph.parse(word)[0].normal_form.lower()
        normalized_words.setdefault(normalized_word, []).append(word)

    # read and store borrowed words from the CSV file
    borrowed_words = {}
    with open(borrowed_dictionary, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            borrowed_words[row["Key"].lower()] = {"Value": row["Value"], "Origin": row["Origin"], "Repeats": 0}

    # check if normalized word is present in borrowed_words
    found_borrowed = {}  
    for word, instances in normalized_words.items():
        if word in borrowed_words:
            repeats = len(instances) # count how many times the word is repeated in the text
            borrowed_words[word]["Repeats"] = repeats # add value "Repeats" to key,value pair in borrowed_words
            found_borrowed[word] = borrowed_words[word] 
            found_borrowed[word]["Instances"] = instances #save the list of prenormalized words

    ready_dictionary = Borrowed(words, found_borrowed)

    if output_file and output_file.endswith(".txt"):
        expanded_output_path = os.path.expanduser(output_file)
        with open(expanded_output_path, "w", encoding="utf-8") as formatted_file:
            formatted_file.write(f"Out of a total of {ready_dictionary.len} words, {ready_dictionary.bor} are borrowed, comprising {ready_dictionary.percent}% of the total.\n\n")
            for key, value in ready_dictionary.dict.items():
                formatted_file.write(f"{value['Repeats']}x: {key} {value['Value']} – {value['Origin']}.\nВ тексте встречается: {', '.join(value['Instances'])}\n\n")

    elif output_file and output_file.endswith(".csv"):
        expanded_output_path = os.path.expanduser(output_file)
        with open(expanded_output_path, "w", encoding="utf-8", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Word", "Value", "Origin", "Repeats", "Instances"])
            for key, value in ready_dictionary.dict.items():
                csv_writer.writerow([key, value["Value"], value["Origin"], value["Repeats"], value["Instances"]])

    return ready_dictionary

"""
# using from terminal
if __name__ == "__main__":
    # сheck for command-line arguments
    args = sys.argv[1:]    

    # set default values
    text_file = "text_file.txt"
    output_file = "output.txt"

    # ovverride defaults if arguments are provided
    if len(args) >= 1:
        text_file = args[0]
    if len(args) == 2:
        output_file = args[1]

    # check that file names end with '.txt' and provide 
    if text_file.endswith(".txt") and (output_file.endswith(".txt") or output_file.endswith(".csv")):
        # execute analyze_borrowed_words
        analyze_borrowed_words(text_file, output_file)
    else:
        print("Usage: python script.py [text_file] [output_file]")
        print("The first argument should end with '.txt', and the second with either '.txt' or '.csv'")
"""
