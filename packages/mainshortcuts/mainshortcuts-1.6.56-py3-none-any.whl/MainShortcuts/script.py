from MainShortcuts.MainCore import ms, _MainCore
mcore=_MainCore()
cprint=mcore.cprint
cformat=mcore.cformat
argv=mcore.args[1:]
def mkdir(path=argv):
  if type(path)==str:
    p=[path]
  elif type(path)==tuple:
    p=list(path)
  else:
    p=path
  for i in p:
    try:
      ms.dir.create(i)
    except Exception as e:
      cprint(e,start="RED")
def jsonPretty(path=argv):
  if type(path)==str:
    p=[path]
  elif type(path)==tuple:
    p=list(path)
  else:
    p=path
  for i in p:
    try:
      d=ms.json.read(i)
      ms.json.write(i,d,mode="p")
    except Exception as e:
      cprint(e,start="RED")
def jsonCompress(path=argv):
  if type(path)==str:
    p=[path]
  elif type(path)==tuple:
    p=list(path)
  else:
    p=path
  for i in p:
    try:
      d=ms.json.read(i)
      ms.json.write(i,d,mode="c")
    except Exception as e:
      cprint(e,start="RED")
def getCore(path=argv):
  if type(path)==str:
    p=[path]
  elif type(path)==tuple:
    p=list(path)
  else:
    p=path
  from MainShortcuts.MainCore import __file__ as corePath
  for i in p:
    try:
      if ms.path.exists(i):
        a=ms.file.read(i)
        b=ms.file.read(corePath).strip()
        c=b.rstrip()+"\n"+a
        ms.file.write(i,c.rstrip())
        cprint(f'MainCore added to the beginning of the file "{i}"',start="GREEN")
      else:
        ms.file.copy(corePath,i)
        cprint(f'MainCore is written to file "{i}"',start="GREEN")
    except Exception as e:
      cprint(e,start="RED")
def getCoreMini(path=argv):
  if type(path)==str:
    p=[path]
  elif type(path)==tuple:
    p=list(path)
  else:
    p=path
  d='from MainShortcuts.MainCore import ms, _MainCore, dictplus\nmcore=_MainCore(__name__=__name__,__file__=__file__)\ncprint=mcore.cprint\ncformat=mcore.cformat\nglobals=dictplus()\ncfg=ms.cfg(mcore.dir+"/cfg.json")\ntry:\n  cfg.load()\nexcept FileNotFoundError:\n  cfg.data={}\ncfg.default={}\ncfg.set_default()\n'
  for i in p:
    try:
      if ms.path.exists(i):
        a=ms.file.read(i)
        c=d+a
        ms.file.write(i,c.rstrip())
        cprint(f'MainCore added to the beginning of the file "{i}"',start="GREEN")
      else:
        ms.file.write(i,d)
        cprint(f'MainCore is written to file "{i}"',start="GREEN")
    except Exception as e:
      cprint(e,start="RED")
