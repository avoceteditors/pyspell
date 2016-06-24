# Copyright (c) 2016, Kenneth P. J. Dyer
# All rights reserved.
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided
# that the following conditions are met:
#
# * Redistributions of source code must retain the
#   above copyright notice, this list of conditions
#   and the following disclaimer.
#
# * Redistributions in binary form must reproduce the
#   above copyright notice, this list of conditions
#   and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of pyspell nor the names of its
#   contributors may be used to endorse or promote
#   products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS
# AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Module Imports
import sys
import subprocess
import cowtermcolor

# Controller Class
class PySpell():
    """Main Process for the PySpell Application

    This application provides a wrapper with some minor additional functionality to
    the Linux utility spell, which itself is a wrapper for the GNU Aspell list 
    functionality.  If you call spell on a file, it returns a list of mispelled 
    words in the file.  If you call spell on a dozen files, it returns a list of
    all mispelled words found collectively.

    PySpell iterates over the source filles, calling spell on each via subprocess,
    it then removes any entries matching a user-defined ignore list and formats
    the results to list each file read and the errors found in that file.

    It provides no functionality for correcting these errors or updating the
    ignore list.  The purpose of PySpell is to report on spelling errors in
    large documentation projects.  That is, to generate and update a list
    of misspellings for the technical writers to work through in making
    corrections.
    """

    # Initialize Class
    def __init__(self, args):
        """ Initialize the class and begin the main process

        Receive the argparse object from the command-line script.
        """

        # Masthead
        version = "0.1"
        name = "PySpell - The Project Level Spellchecker"

        if args.verbose or args.version:
            content = [     name,
                            "Kenneth P. J. Dyer",
                            "Avocet Editorial Consultants",
                            "kenneth@avoceteditors.com",
                            "Version %s" % version, ' ' ]
            masthead = '\n   '.join(content)
        else:
            content = [name, "Version %s" % version]
            masthead = ' - '.join(content)
        print(masthead)

        if args.version:
            sys.exit(0)

        # Run Spell for Base
        data = self.run_spell(args.source)

        # Load Ignorelist
        if args.ignore is not None:
            ignorelist = self.build_ignore(args.ignore)
        else:
            ignorelist = ['']
        data = self.clear_ignores(data, ignorelist)

        # Print to Stdout
        self.report(data)

        # Exit
        sys.exit(0)

    # Run Basic Check
    def run_spell(self, paths):
        """ Check the given files for spelling errors

        Method iterates over each file given from the command-line.
        It executes the spell application with subprocess, then checks
        the output from stdout into the data dict.

        Returns the data dict.
        """

        # Initialize Data Dict
        data = {}

        # Check Input for Misspellings
        for i in paths:

            command = ['spell', i]
            errors = subprocess.check_output(command)

            # Store, Decode and Split Output
            data[i] = errors.decode().split('\n')

        return data


    # Build Ignorelist
    def build_ignore(self, path):
        """ Generate the Ignorelist

        The ignorelist is an arbitrary list of words that PySpell should
        ignore.  This is not the same as words that you want to add to the
        main dictionary.  For instanc, a documentation file might include
        code sampls, which contain a number of variable names like targetBA.
        This is something you might ignore in one project rather than add to
        the main dictionary.
        """

        # Open Ignorelist
        try:
            f = open(path, 'r')
            content = f.read()
            f.close()
        except:
            content = ''

        # Convert and Clean Ignorelist
        base = content.split('\n')
        ignores = []
        for entry in base:
            if entry != '':
                entry = entry.strip()
                ignores.append(entry)

        return ignores


    # Clear Ignorelist from Data
    def clear_ignores(self, data, ignorelist):
        """ Checks the errorslist found in each file and removes the words
        that you want it to ignore.

        This method appears to be the principal bottleneck for the application.
        If you have any suggestions of how to improve performance, feel free to
        open an issue on GitHub or submit a pull request.
        """

        # Check if Ignorelist Empty
        if ignorelist == ['']:
            return data

        for i in data:
            newlist = []

            for entry in data[i]:
                if entry not in ignorelist:
                    newlist.append(entry)

            data[i] = newlist
        return data


    # Report Findings
    def report(self, data):
        """ Report Findings to Stdout

        Method iterates over the data dict, for each entry it prints the
        filename in green, then prints a list of the misspelled words in
        yellow.
        """

        # Initialize Cowtermcolor
        yellow = cowtermcolor.Color(cowtermcolor.YELLOW)
        green = cowtermcolor.Color(cowtermcolor.GREEN)



        # Print Outputs
        for key in data:
            errors = data[key]

            # Print File Name
            print(green(key))

            # Print Errors
            for err in errors:
                if err != '':
                    line = ' - ' + yellow(err)
                    print(line)
