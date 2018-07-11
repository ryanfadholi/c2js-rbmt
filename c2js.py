import deformatter as dfrmt
import postagger as post
import sltransfer as slt
def tagprint(tags):
    for tag in tags:
        print(f"{tag['token']} - {tag['type']}", end=", " )
    print("")

print("-------------------------------------------------")
df = dfrmt.Deformat("example.c")
tagger = post.POSTagger()
transfer = slt.StructuralLexicalTransfer()

for stmt in df._statements_generator():
    # print("----------------NEW STATEMENT")    

    tagged = tagger.tag(stmt)
    # print(stmt)
    # print(transfer.identify(tagged))


