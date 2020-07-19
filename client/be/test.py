#%%
import os

username = "er6"
path = os.path.join("static", username, "processing","ru")

print(path)


# %%
#return list

lang="ru"

os.listdir(os.path.join("static", username, "raw", lang))

# %%

import pickle
from typing import List

class DocLine:
    def __init__(self, line_ids:List[int]=[], text=None):
        self.line_ids = line_ids
        self.text = text
    def __hash__(self):
        return hash(self.text)
    def __eq__(self, other):
        return self.text == other
    def isNgramed(self) -> bool:
        return len(self.line_ids)>1

docs = pickle.load(open(os.path.join(path, "kryzhovnik_ru.txt"), "rb"))


# %%
res = {}
for doc in docs:
    for line in doc:
        res[line.text] = {
            "line_ids": line.line_ids,
            "trans": [{
                "text": t[0].text, 
                "line_ids":t[0].line_ids, 
                "sim": t[1]} for t in doc[line]]
                }
# %%
res

# %%

for i,x in enumerate(sorted([1,2,3,4,8,9,0,4,3,2])):
    print(1 if i==0 else 0, x)


# %%
