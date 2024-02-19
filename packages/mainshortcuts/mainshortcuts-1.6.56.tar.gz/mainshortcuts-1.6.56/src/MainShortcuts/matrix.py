class DontFill:
  pass
class WrongCoordinates(Exception):
  pass
def _checkCoords(k):
  if type(k) in [list,tuple]:
    if type(k[0])==int and type(k[1])==int and len(k)==2:
      if k[0]>=0 and k[1]>=0:
        return True
      else:
        raise WrongCoordinates("coordinates must be greater than or equal to zero")
    else:
      raise WrongCoordinates("coordinates must be a pair of integers")
  else:
    raise TypeError("coordinates could be {0} or {1}, not {2}".format(tuple,list,type(k)))
class ListsInList:
  def __init__(self):
    pass
  def open(self,mtx,lines):
    if not type(lines) in [list,tuple]:
      raise TypeError("lines could be {0} or {1}, not {2}".format(tuple,list,type(lines)))
    lines=list(lines)
    sizeX,sizeY=0,len(lines)
    c=-1
    for i in lines:
      c+=1
      if not type(i) in [list,tuple]:
        raise TypeError("lines[{4}] could be {0} or {1}, not {2}".format(tuple,list,type(i),c))
      sizeX=max(sizeX,len(i))
    data={}
    y=-1
    for l in lines:
      y+=1
      l=list(l)
      if mtx.empty!=DontFill:
        while len(l)<sizeX:
          l.append(mtx.empty)
      x=-1
      for d in l:
        x+=1
        _checkCoords((x,y))
        data[x,y]=d
    return data
  def save(self,mtx):
    sizeX,sizeY=0,0
    for x,y in mtx.data:
      sizeX=max(sizeX,x+1)
      sizeY=max(sizeY,y+1)
    lines=[]
    for y in range(sizeY):
      l=[]
      for x in range(sizeX):
        if (x,y) in data:
          l.append(mtx.data[x,y])
        else:
          l.append(mtx.empty)
      lines.append(l)
    return lines
class DictWithTuple:
  def __init__(self):
    pass
  def open(self,mtx,raw):
    data={}
    for k,v in raw.items():
      _checkCoords(k)
      data[k]=v
    return data
  def save(self,mtx):
    return mtx.data
class DictWithStr:
  def __init__(self):
    pass
  def open(self,mtx,raw,split="x"):
    data={}
    for k,v in raw.items():
      _checkCoords(k)
      data[int(k.split(split)[0]),int(k.split(split)[1])]=v
    return data
  def save(self,mtx):
    raw={}
    for (x,y) in mtx.data:
      raw[f"{x}{split}{y}"]=data[x,y]
    return raw
class PillowImage:
  def __init__(self):
    from PIL import Image
    self.Image=Image
  def open(self,mtx,img):
    sizeX,sizeY=img.size
    data={}
    for x in sizeX:
      for y in sizeY:
        data[x,y]=img.getpixel((x,y))
    return data
  def save(self,mtx,mode="RGBA",*args,**kwargs):
    mtx.reload()
    try:
      img=self.Image.new(mode,(mtx.sizeX,mtx.sizeY),mtx.empty,*args,**kwargs)
    except:
      img=self.Image.new(mode,(mtx.sizeX,mtx.sizeY),*args,**kwargs)
    for x in mtx.sizeX:
      for y in mtx.sizeY:
        if mtx[x,y]!=DontFill and mtx[x,y]!=mtx.empty:
          img.putpixel((x,y),mtx[x,y])
    return img
class matrix:
  def __init__(self,raw,empty=DontFill,mode=ListsInList(),*args,**kwargs):
    self.empty=empty
    self.mode=mode
    self.data={}
    if raw!=None:
      d=mode.open(self,raw,*args,**kwargs)
      if d==None:
        pass
      if type(d)==dict:
        for k in d:
          _checkCoords(k)
        self.data=d
      else:
        raise TypeError("end could be {0} or {1}, not {2}".format(tuple,list,type(end)))
    self.reload()
  def __repr__(self):
    self.reload()
    return f"ms.matrix(size={(self.sizeX,self.sizeY)})"
  def __setattr__(self,k,v):
    self.__dict__[k]=v
  def __getitem__(self,k):
    if k in self.data:
      return self.data[k]
    else:
      return self.empty
  def __setitem__(self,k,v):
    _checkCoords(k)
    self.data[k[0],k[1]]=v
    self.reload()
  def __contains__(self,k):
    return k in self.data
  def reload(self,fill=False):
    self.sizeX,self.sizeY=0,0
    for x,y in self.data:
      self.sizeX=max(self.sizeX,x+1)
      self.sizeY=max(self.sizeY,y+1)
    if fill:
      for x in range(self.sizeX):
        for y in range(self.sizeY):
          if not (x,y) in self.data:
            self.data[x,y]=self.empty
          elif self.data[x,y]==DontFill and self.empty!=DontFill:
            self.data[x,y]=self.empty
  def slice(self,start=(None,None),end=(None,None),start_at_zero=True,mode=None,*args,**kwargs):
    if not type(start) in [list,tuple]:
      raise TypeError("start could be {0} or {1}, not {2}".format(tuple,list,type(start)))
    if not type(end) in [list,tuple]:
      raise TypeError("end could be {0} or {1}, not {2}".format(tuple,list,type(end)))
    if mode==None:
      mode=self.mode
    if start[0]==None:
      sX=0
    elif type(start[0])==int:
      sX=start[0]
    else:
      raise TypeError("start[0] could be {0}, not {1}".format(int,type(start[0])))
    if start[1]==None:
      sY=0
    elif type(start[1])==int:
      sY=start[1]
    else:
      raise TypeError("start[1] could be {0}, not {1}".format(int,type(start[1])))
    if end[0]==None:
      eX=self.sizeX-1
    elif type(end[0])==int:
      eX=end[0]
    else:
      raise TypeError("end[0] could be {0}, not {1}".format(int,type(end[0])))
    if end[1]==None:
      eY=self.sizeY-1
    elif type(end[1])==int:
      eY=end[1]
    else:
      raise TypeError("end[1] could be {0}, not {1}".format(int,type(end[1])))
    copy=self.__class__(None,empty=self.empty,mode=mode,*args,**kwargs)
    for x in range(sX,eX+1):
      for y in range(sY,eY+1):
        if start_at_zero:
          newX=x-sX
          newY=y-sY
        else:
          newX,newY=x,y
        if (x,y) in self.data:
          copy.data[newX,newY]=self.data[x,y]
    return copy
  def get(self,mode=None,*args,**kwargs):
    if mode==None:
      mode=self.mode
    return mode.save(self,*args,**kwargs)
