#%%
import os

username = "sergei"
path = os.path.join("static", username, "raw")

print(path)


# %%
#return list

lang="ru"

os.listdir(os.path.join("static", username, "raw", lang))

# %%
