# russborrow

This is a test version of the russborrow package.

# Overview

[russborrow]{.title-ref} is a Python package for analyzing Russian text
to identify and extract borrowed words from other languages. The package
uses the pymorphy2 library to normalize words, and it includes a
dictionary of borrowed words for comparison.

# Usage

The [russborrow]{.title-ref} package provides various options for
analyzing text and extracting borrowed words. Here are the available
usage scenarios.

Make sure to import it in your script or Python environment: ..
code-block:: python

import russborrow

**Note:** If a variable is initialized (e.g., borrowed in the examples),
it will store the returned object. If no variable is used, the module
will work with provided input and output files. If neither a variable is
initialized nor an output file is provided, the code won\'t crash, but
no output or return will be given.

## Option 1: Analyze Text String

Example 1:

``` python
borrowed = russborrow.extract("""
Значимость этих проблем настолько очевидна, что синтетическое тестирование 
требует анализа экспериментов, поражающих по своей масштабности и грандиозности.
""")
```

Example 2:

``` python
text_to_analyze = """
Значимость этих проблем настолько очевидна, что синтетическое тестирование 
требует анализа экспериментов, поражающих по своей масштабности и грандиозности.
"""
borrowed = russborrow.extract(text_to_analyze)
```

## Option 2: Analyze Text File

Example 1, Standard Usage with \~:

``` python
file_path = '~/Desktop/text.txt' 
borrowed = russborrow.extract(file_path)
```

Example 2, Windows Path:

``` python
file_path = r"C:\Users\Username\Documents\file.txt"
borrowed = russborrow.extract(file_path)
```

Example 3 (File in the same directory as the code):

``` python
borrowed = russborrow.extract('text.txt')
```

## Option 3: Provide Output File Path

Specify an output file path to create a file containing the analysis
results. The provided file path must end with either [.txt]{.title-ref}
or [.csv]{.title-ref}. If the specified file already exists, it will be
overwritten.

Example 3:

``` python
output_path = '-/Desktop/newoutput.txt'
borrowed = russborrow.extract(string, output_path)
```

# Returned Object Attributes

The [russborrow.extract]{.title-ref} function returns an object of the
[Borrowed]{.title-ref} class with the following attributes:

-   **borrowed.len:** Total number of words in the text.
-   **borrowed.bor:** Number of borrowed words in the provided text.
-   **borrowed.percent:** Percentage of borrowed words in the provided
    text.
-   **borrowed.dict:** A dictionary containing normalized versions of
    borrowed words as keys with the following values:
    -   **value\[\'Repeats\'\]:** Count of the word (normalized version)
        in the text.
    -   **value\[\'Value\'\]:** Description of the word.
    -   **value\[\'Origin\'\]:** Language of origin of the borrowed
        word.
    -   **value\[\'Instances\'\]:** List of all borrowed words before
        normalization found in the original text that have the
        normalized version as the key.

**Note:** Object attributes have no setters.

# Used Resources

## Pymorphy2

\[Pymorphy2\](<https://pymorphy2.readthedocs.io/en/stable/>) is a Python
library for morphological analysis and inflection. It is used in the
russborrow package to normalize words for comparrison with dictionary.

## Borrowed Words Dictionary

The dictionary used for identifying borrowed words is sourced from
[Wiktionary](https://ru.wiktionary.org/wiki/Приложение:Заимствованные_слова_в_русском_языке).
It is stored in the [borrowed_dictionary.csv]{.title-ref} file within
the russborrow package. The dictionary format includes the following
columns:

-   **Key:** Borrowed word
-   **Value:** Description of the word
-   **Origin:** Language of origin

Example entry in the dictionary:

    гламур, — glamer, от gramarye «магия, заклинание», Из гэльского (шотландского)

**Exclusion Note:** The word \"они\"\" --- 鬼 «демон» (демоны-людоеды,
умеющие обращаться в людей) has been intentionally excluded from the
dictionary for the following reasons: - Pymorphy and its resources
recognize the word \"они\" solely as a pronoun (местоимение) without
noun form (существительное). - Retaining \"они\" in the dictionary leads
the program to classify the highly common pronoun \"они\" as a borrowed
word. - According to Wiktionary, the usage of \"они\" as borrowed word
is infrequent. If your text focuses on Japanese folklore or demons, it
is advisable to manually verify the output for accuracy.
