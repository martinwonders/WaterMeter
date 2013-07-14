class config: #{

  def __init__(self,conf_file,parser): #{
    '''(str) -> dict, dict
  
    return a dictionary storing the room information in rooms
    and a dictionary storing serial interface information in ser.
    The information is taken from a a configuration file conf_file
    '''
    self.p = parser;
    self.p.read(conf_file);
    self.roomDict = dict(self.p.items('rooms'));
    self.rooms = [];
    self.ser = dict(self.p.items('serial'));
    self.train = dict(self.p.items('training'))
    for key,value in self.roomDict.items(): #{
      if (value == 'true'): #{
        self.rooms.append(key);
        self.roomDict[key] = dict(parser.items(key));
        self.roomDict[key]['tags']= self.roomDict[key]['tags'].split(',');
        self.roomDict[key]['events']= self.roomDict[key]['events'].split(',');
        c = self.roomDict[key]['c_params'].split(',');
        g = self.roomDict[key]['g_params'].split(',');
        self.roomDict[key]['c_params'] = map(float,c);
        self.roomDict[key]['g_params'] = map(float,g);
      #}
      else: #{
        del self.roomDict[key];
      #}
    #}
    #room now containes a room name as the key with
    #all the config options associated with it, all rooms
    #set to false are deleted
  #}

  def getSerialData(self): #{
    return self.ser['data'];
  #}

  def getSerialControl(self): #{
    return self.ser['control'];
  #}

  def getRoomNames(self): #{
    return self.rooms;
  #}

  def getDict(self): #{
    return self.roomDict;
  #}

  def getEvents(self,room): #{
    events = [];
    if room in self.roomDict: #{
      for event in self.roomDict[room]['events']: #{
        events.append(event);
      #}
        
    return events;
  #}

  def getDataFile(self,room): #{
    f = '';
    if room in self.roomDict: #{
      f = self.roomDict[room]['data'];
    #}
    return f;
  #}

  def getPir(self,room): #{
    pir = '';
    if room in self.roomDict: #{
      pir = self.roomDict[room]['pir'];
    #}
    return pir;
  #}

  def getRoom(self,PIR): #{
    r = ' ';
    for room in self.roomDict: #{
      if (self.roomDict[room]['pir']==PIR):#{
        r = room;
      #}
    #}
    return r;
  #}

  def getKnnSize(self,room): #{
    s=0;
    if room in self.roomDict: #{
      s = int(self.roomDict[room]['knnsize']);
    #}
    return s;
  #}

  def getKnnSize(self,room): #{
    s=0;
    if room in self.roomDict: #{
      s = int(self.roomDict[room]['svmsize']);
    #}
    return s;
  #}

  def getLogging(self,room): #{
    log = '';
    if room in self.roomDict: #{
      log = self.roomDict[room]['logging'];
    #}
    return log;
  #}

  def getTag(self,room,event): #{
    tag = '';
    if (room in self.roomDict) and (event in self.roomDict[room]['events']): #{
      ind = self.roomDict[room]['events'].index(event);
      tag = self.roomDict[room]['tags'][ind];
    #}

    return tag;
  #}

  def getClass(self,room,event): #{
    class_num = 0;
    if (room in self.roomDict) and (event in self.roomDict[room]['events']): #{
      class_num = self.roomDict[room]['events'].index(event)+1;
      
    #}

    return int(class_num);
  #}

  def getClassLabel(self,room,class_number): #{
    c = '';
    if (room in self.roomDict): #{
      c = self.roomDict[room]['events'][class_number-1];
      
    #}
    return c;
  #}

  def getTails(self): #{
    return int(self.train['tails']);
  #}

  def getThreshold(self): #{
    return int(self.train['threshold']);
  #}

  def getParamList(self,room): #{
    c = self.roomDict[room]['c_params'];
    g = self.roomDict[room]['g_params'];
    return c,g;
  #}

  def setOption(self,section,option,value): #{
    self.p.set(section,option,value);
  #}

  def writeConfig(self): #{
    with open('wm_config.ini', 'w') as configfile: #{
      self.p.write(configfile);
    #}
  #}

#}
