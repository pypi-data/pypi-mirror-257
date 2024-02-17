PTWordFinder
============

|Build| |Tests Status| |Coverage Status| |Flake8 Status|

“What specific words would you like to read?” Counting words in “Pan
Tadeusz” poem

It is a Python-based command-line tool designed to efficiently find and count occurrences of specific words within text files. It offers flexible input options, supporting both individual words, patterns and word lists in various formats.

Python version
--------------

tested with Python >= 3.10.6

Why
---

It was started as a project to exercise python language. The code helped
to find specific words in a selected file. It became command line tool
that help find any word within any file. The files can be selected by
command line

Install
----------

you can run the following command in your terminal to install the program from pip:

::

       pip install PTWordFinder

This will download and install the program, along with any required dependencies.


If you prefer, you can also install the program from source:

Clone the repository containing the program code:

::

       git clone https://github.com/DarekRepos/PanTadeuszWordFinder.git


Replace your-username with your actual username on GitHub.
Navigate to the cloned directory:

::

       cd  PanTadeuszWordFinder

This method requires poetry or Python build tools. If you don't have them, install poetry using pip install poetry or install your system's package manager's equivalent for build.
Install the program using poetry (https://python-poetry.org/):

::

       poetry install

The second method involves directly building the wheel and installing it, which is less commonly used.
Install the program directly:

::

       python -m build

::

       python -m pip install dist/PTWordFinder-*.whl

Note:

    If you install from source, you will need to have Python development tools installed. You can usually install these using your system's package manager.
    Installing from pip is the easiest and most recommended method for most users.



Usage: 
----------

::

       python word_counter.py [OPTIONS]
       Options:
        -w, --words-input-file FILE          File containing words to search for (mutually exclusive with --single-word)
        -s, --searched-file FILE              Path to the text file to search in (required)
        -w, --single-word WORD                Specific word to count (mutually exclusive with --words-input-file)
        -p, --pattern PATTERN                 Regular expression pattern to match
        -h, --help                            Show this help message and exit


Examples:
----------


Count the word "python" in my_text.txt:

::

       python word_counter.py --single-word python --searched-file my_text.txt

Find the frequency of all words in word_list.txt in large_file.txt:

::

       python word_counter.py --words-input-file word_list.txt --searched-file large_file.txt

Match instances of the regular expression [a-z0-9]{5} in passwords.txt:

::

       python word_counter.py --pattern "[a-z0-9]{5}" --searched-file passwords.txt


.. |Build| image:: https://github.com/DarekRepos/PanTadeuszWordFinder/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/DarekRepos/PanTadeuszWordFinder/actions/workflows/python-package.yml
.. |Tests Status| image:: https://github.com/DarekRepos/PanTadeuszWordFinder/blob/master/reports/coverage/coverage-unit-badge.svg
   :target: https://github.com/DarekRepos/PanTadeuszWordFinder/blob/master/reports/coverage.xml
.. |Coverage Status| image:: https://github.com/DarekRepos/PanTadeuszWordFinder/blob/master/reports/coverage/coverage-badge.svg
   :target: https://github.com/DarekRepos/PanTadeuszWordFinder/tree/master/tests/unit
.. |Flake8 Status| image:: https://github.com/DarekRepos/PanTadeuszWordFinder/blob/master/reports/flake8/flake8-badge.svg
   :target: https://github.com/DarekRepos/PanTadeuszWordFinder/
