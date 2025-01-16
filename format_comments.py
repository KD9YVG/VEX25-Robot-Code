def count_char_at_start(string, char):
  count = 0
  for c in string:
    if c == char:
      count += 1
    else:
      break
  return count

file=open("main.py").readlines()
new_output=""
running=True
for line in file:
    line=line.rstrip()
    if line.strip()=="# commentformat off":
        running=False
    if line.strip()=="# commentformat on":
        running=True
    if running:
        isbackslash=False
        isString=False
        commentindex=None
        for row,char in enumerate(line):
            if isString:
                if isbackslash:
                    isbackslash=False
                else:
                    if char==isString:
                        isString=False
            else:
                if char=="'":
                    isString="'"
                if char=='"':
                    isString='"'
                if char=="#":
                    commentindex=row
                    break
        if commentindex is not None:
            if line.lstrip().startswith("#"):
                new_output+=line
                new_output+="\n"
            else:
                new_output+=" "*count_char_at_start(line," ")
                new_output+=line[commentindex:]
                new_output+="\n"
                new_output+=line[:commentindex]
                new_output+="\n"
        else:
            new_output+=line
            new_output+="\n"
    else:
        new_output+=line
        new_output+="\n"
open("new_main.py","w").write(new_output)