from distutils.core import setup

desc = 'Multifile spellcheck.'

setup(name = 'pyspell',
        version = '0.1',
        author = 'Kenneth P. J. Dyer',
        author_email = 'kenneth@avoceteditors.com',
        url = 'https://github.com/avoceteditors/pyspell',
        description = desc,
        license = 'BSD 3-clause',
        packages = ['pyspell'],
        scripts = ['scripts/pyspell'],
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            ]
        )
