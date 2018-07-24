import deformatter as dfrmt
import postagger as post
import sltransfer as slt
import postgenerator as pg

def tagprint(tags):
    for tag in tags:
        print(f"{tag['token']} - {tag['type']}", end=", " )
    print("")

print("-------------------------------------------------")
df = dfrmt.Deformat("example.c")
tagger = post.POSTagger()
transfer = slt.StructuralLexicalTransfer()
pgen = pg.PostGenerator("output.js")

# for stmt in df._statements_generator():  

#     tagged = tagger.tag(stmt)
#     # print(stmt)
#     print(transfer.identify(tagged))

stmts = [stmt for stmt in df._statements_generator()]
tagged_stmts = map(lambda x: tagger.tag(x), stmts)
identified_stmts = list(map(lambda x: transfer.translate(x), tagged_stmts))

for stmt in identified_stmts:
    print(stmt)

pgen.write(identified_stmts)


