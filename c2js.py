import deformatter as dfrmt

str = "Hello World!"

lowerstr = str.lower()
df = dfrmt.Deformat("example.c")
print(df.lines)