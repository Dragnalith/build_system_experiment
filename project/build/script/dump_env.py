import os

"""
It can be a bit tricky to manage environment variable for build action. For instance
ninja does not let you setup those variable, you need to use 'ninja -t msvc -e {env}'
to do so. It is not easiy to see if a program receive the correct environment variable
so the purpose of that script is to be used at a build action and it will print the 
environment variable of its context.

(I used it to investigate 'ninja -t msvc -e {env}' and make sure about the {env} file format)
"""

for key, val in os.environ.items():
    print("{}={}".format(key,val))