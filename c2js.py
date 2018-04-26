#------------------------------------------------
#Clean terminal when run. Delete on final version!
import os
os.system("cls")
#------------------------------------------------

import deformatter as dfrmt
import postagger as post

print("-------------------------------------------------")
df = dfrmt.Deformat("example.c")
tagger = post.POSTagger()

for stmt in df._statements_generator():
    print("**Statement")
    print(tagger.tag(stmt))

