import os
import json

def get_conf(name):
    with open(os.path.join(os.path.dirname(__file__),"assets","conf.json"),"r") as file:
        conf = json.loads(file.read())
        if name in conf:
            return conf[name]



if __name__ == "__main__":
    print(get_conf("size"))