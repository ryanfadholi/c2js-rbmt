#------------------------------------------------
#Clean terminal when run. Delete on final version!
# import os
# os.system("cls")
#------------------------------------------------

import deformatter as dfrmt
import postagger as post

def tagprint(tags):
    for tag in tags:
        print(f"{tag['token']} - {tag['type']}", end=", " )
    print("")

print("-------------------------------------------------")
df = dfrmt.Deformat("example.c")
tagger = post.POSTagger()

for stmt in df._statements_generator():
    print(tagger.tag(stmt))

