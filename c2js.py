import deformatter as dfrmt

df = dfrmt.Deformat("example.c")
for line in df.lines:
    print(line)
    print("New line:", line.find("\n"))