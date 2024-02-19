import os, traceback
import MainShortcuts as ms
class dictplus:
  def __init__(self,data=None):
    if data==None:
      self.__data__={}
    else:
      self.__data__=data
  def __getattr__(self,k):
    if k=="__data__":
      return self.__dict__[k]
    else:
      return self[k]
  def __setattr__(self,k,v):
    if k=="__data__":
      self.__dict__[k]=v
    else:
      self[k]=v
  def __repr__(self):
    return f"dictplus({str(self.__data__)})"
  def __dir__(self):
    return list(self.__data__.keys())+["__data__"]
  def __len__(self):
    return len(self.__data__.keys())
  def __contains__(self,k):
    return (k in self.__data__)
  __hasattr__=__contains__
  def __eq__(self,o):
    if type(o)==dict:
      return self.__data__==o
    else:
      return self.__data__==o.__data__
  def __getitem__(self,k):
    return self.__dict__["__data__"][k]
  def __setitem__(self,k,v):
    self.__dict__["__data__"][k]=v
  def __delitem__(self,k):
    self.__dict__["__data__"].pop(k)
  def __delattr__(self,k):
    self.__dict__["__data__"].pop(k)
class _MainCore:
  def __init__(self,color=True,__name__=__name__,__file__=__file__):
    self.args=ms.proc.args # Все аргументы запуска (то же самое, что и sys.argv)
    self.core_name="MainCore"
    self.core_version=4
    self.dir=os.path.dirname(__file__) # Папка, в которой находится программа
    self.exception=traceback.format_exc
    self.pid=os.getpid() # PID программы
    self.run=__name__=="__main__" # Запущена программа или её импортируют?
    self.color_names=["","BG_BLACK","BG_BLUE","BG_GREEN","BG_LIGHTBLACK","BG_LIGHTBLUE","BG_LIGHTGREEN","BG_LIGHTPINK","BG_LIGHTRED","BG_LIGHTWHITE","BG_LIGHTYELLOW","BG_PINK","BG_RED","BG_WHITE","BG_YELLOW","BLACK","BLUE","GREEN","HIGH","LIGHTBLACK","LIGHTBLUE","LIGHTGREEN","LIGHTPINK","LIGHTRED","LIGHTWHITE","LIGHTYELLOW","LOW","PINK","RED","RESET","WHITE","YELLOW"]
    self.colors={}
    for i in self.color_names:
      self.colors[i]=""
    if color:
      try:
        import colorama as clr
        clr.init()
        self.colors["BG_BLACK"]=clr.Back.BLACK
        self.colors["BG_BLUE"]=clr.Back.BLUE
        self.colors["BG_GREEN"]=clr.Back.GREEN
        self.colors["BG_LIGHTBLACK"]=clr.Back.LIGHTBLACK_EX
        self.colors["BG_LIGHTBLUE"]=clr.Back.LIGHTBLUE_EX
        self.colors["BG_LIGHTGREEN"]=clr.Back.LIGHTGREEN_EX
        self.colors["BG_LIGHTPINK"]=clr.Back.LIGHTMAGENTA_EX
        self.colors["BG_LIGHTRED"]=clr.Back.LIGHTRED_EX
        self.colors["BG_LIGHTWHITE"]=clr.Back.LIGHTWHITE_EX
        self.colors["BG_LIGHTYELLOW"]=clr.Back.LIGHTYELLOW_EX
        self.colors["BG_PINK"]=clr.Back.MAGENTA
        self.colors["BG_RED"]=clr.Back.RED
        self.colors["BG_WHITE"]=clr.Back.WHITE
        self.colors["BG_YELLOW"]=clr.Back.YELLOW
        self.colors["BLACK"]=clr.Fore.BLACK
        self.colors["BLUE"]=clr.Fore.BLUE
        self.colors["GREEN"]=clr.Fore.GREEN
        self.colors["HIGH"]=clr.Style.BRIGHT
        self.colors["LIGHTBLACK"]=clr.Fore.LIGHTBLACK_EX
        self.colors["LIGHTBLUE"]=clr.Fore.LIGHTBLUE_EX
        self.colors["LIGHTGREEN"]=clr.Fore.LIGHTGREEN_EX
        self.colors["LIGHTPINK"]=clr.Fore.LIGHTMAGENTA_EX
        self.colors["LIGHTRED"]=clr.Fore.LIGHTRED_EX
        self.colors["LIGHTWHITE"]=clr.Fore.LIGHTWHITE_EX
        self.colors["LIGHTYELLOW"]=clr.Fore.LIGHTYELLOW_EX
        self.colors["LOW"]=clr.Style.DIM
        self.colors["PINK"]=clr.Fore.MAGENTA
        self.colors["RED"]=clr.Fore.RED
        self.colors["RESET"]=clr.Style.RESET_ALL
        self.colors["WHITE"]=clr.Fore.WHITE
        self.colors["YELLOW"]=clr.Fore.YELLOW
      except:
        color=False
  def __repr__(self):
    return ms.json.encode({"name":self.core_name,"version":self.core_version},mode="c")
  def cprint(self,a,start="",**kwargs): # Вывести цветной текст | cprint("Обычный текст, {BLUE}Синий текст")
    try:
      b=str(a).rstrip().format(**self.colors)
    except KeyError:
      b=str(a).rstrip()
      for k,v in self.colors.items():
        try:
          arg={k:v}
          b=b.format(**arg)
        except KeyError:
          pass
    print(self.colors["RESET"]+self.colors[start]+b.rstrip()+self.colors["RESET"],**kwargs)
  def cformat(self,a,start=""): # Аналогично cprint, но вывод в return, и нет strip
    try:
      b=str(a).format(**self.colors)
    except KeyError:
      b=str(a).rstrip()
      for k,v in self.colors.items():
        try:
          arg={k:v}
          b=b.format(**arg)
        except KeyError:
          pass
    return self.colors["RESET"]+self.colors[start]+b+self.colors["RESET"]
  def ctest(self): # Вывод всех доступных цветов
    for k,v in self.colors.items():
      if k!="":
        print("{0}{1}: {2}EXAMPLE ░▒▓ ███{0}".format(self.colors["RESET"],k,v))
  def ignoreException(self,target,*args,**kwargs):
    try:
      return target(*args,**kwargs)
    except:
      return self.exception()
mcore=_MainCore()
cprint=mcore.cprint
cformat=mcore.cformat
globals=dictplus()
