PySpell
=======

This application provides a wrapper with some additional functionality to the Linux utility spell, which is based on the old Unix spell, but is a wrapper for the ``list`` functionality in GNU Aspell.

When you call spell on one file, it returns a list of all the unqiue misspelled words it finds, using the default dictionary.  When you call spell on many files, it adds the additional unique misspelled words, but it doesn't differentiate to show which misspelled words are in which files.  PySpell uses the subprocess module to call spell, it then takes the output and sorts out entries in a user-defined ignore list and prints the results in a conveniently format: file path followed by the list of misspelled words for that file.

PySpell does not provide functionality for updating the ignore list or for correcting the misspelled words.  It's intended for use in documentation and similar large writing projects, where you need to check many files for errors before committing changes to Git.  To correct the changes, you can call Aspell directly on the given file, run a script using sed and awk, or open the file in your preferred text editor.  PySpell is just about letting you know there's something there to fix or ignore.

Installation
------------

PySpell is available on the Python Package Index.  It is currently being used in production on Python 3.  It is presumably usable in Python 2.  In order to use it you must install GNU Aspell, as well as an Aspell dictionary for the language you want to use.  On Fedora, you would use the following commands:

.. code-block:: console

   # dnf install aspell 

