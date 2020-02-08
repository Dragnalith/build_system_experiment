import os

for key, val in os.environ.items():
    print("{}={}".format(key,val))