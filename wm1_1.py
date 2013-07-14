import os
import serial
import classify
import resize
import configC
import numpy
import sys
import datetime
from scipy import stats
from lxml import etree
from ConfigParser import SafeConfigParser;
import threading
import time


last = ''
pir_flag = 'unk'
g_truth = 'unk'
Eflag = False

def rec(s2,rooms):
  '''(str,dict) -> thread

  starts a thread that listens to the KNX interface defined
  by s2 and uses the dictionary named rooms to decode the KNX
  messages listening for pir and tag data. pir data is used to  
  set the global variable pir_flag and the tag data is used to 
  set the global variable g_truth.
  ''' 
  global last
  global g_truth
  global pir_flag
  global Eflag
  start = time.time()
  buff = ''
  s2.open()
    
  print 'serial open','\n'
  print 'waitng for KNX data...','\n'
  while True:
    buff += s2.read(32)
    if 'tdi' in buff:
      last,buff = buff.split('t')[-2:]
      last = 't{}'.format(last)
      for key,value in rooms.items():
        if value['pir'] in last:
          pir_flag = key
          print 'Data from {} PIR'.format(pir_flag)
          Eflag = True
          start = time.time()
        elif (time.time()- start) > 40:
          pir_flag = 'unk'
          Eflag = False

      for key,value in rooms.items():
        i=0
        for tag in value['tags']:
          if tag in last:
            g_truth = value['events'][i] + '(' + key + ')'
            print 'Ground Truth registered as {}'.format(g_truth)
          i=i+1

      
  s2.close()


def main():
  svm_model = {}
  knn_model = {}
  pirs = []
  global g_truth
  global pir_flag
  loc='unk'
  samples=[]
  event=[]
  parser=SafeConfigParser();
  con = configC.config('wm_config.ini',parser);
  
  s1 = serial.Serial(con.getSerialData(),9600)
  s2 = serial.Serial(con.getSerialControl(),9600)
  s1.open()
  s1.flushInput()
  now = datetime.datetime.now()
  print 'serial open on {}/{}/{} at {}:{}'.format(now.day,now.month,now.year,now.hour,now.minute);
  print 'reading training data...','\n'
 
  #read the rooms dictionary and build a model for each room
  #store the models in a model dictionary
  rooms = con.getDict();
  for key,value in rooms.items():
    X,y = classify.get_data(rooms[key]['data'])
    if value=='true': #{
      pirs.append(rooms[key])
    #}
    print 'Building SVM model for {}.'.format(key)
    svm_model[key] = classify.train_svm(X,y,float(rooms[key]['c']),float(rooms[key]['gamma']))
    print 'SVM model built.'
    print 'Building KNN model for {}.'.format(key)
    knn_model[key] = classify.train_knn(X,y,1)
    print 'KNN model built.'
 
  print 'Starting KNX serial thread...','\n'
  threading.Thread(target=rec, args=(s2,rooms)).start()
  print 'waiting for water flow...','\n'
  
  while 1:
    if s1.isOpen(): #{
      ml = s1.readline()
      sample_cnt = 0;
      if '<' in ml:
        ml = s1.readline()
        ml = ml.strip('\r\n')
        while '>' not in ml:
          sample_cnt = sample_cnt + 1;
          if sample_cnt < 10: #{
            loc = pir_flag;
          #}
          print '{}:'.format(sample_cnt),ml, '->{}'.format(loc)
          try:
            samples.append(int(ml));
          except:
            print 'No sample, carrying on regardless...';
          
          ml = s1.readline()
          ml = ml.strip('\r\n')
        vol= sum(samples)
        if vol > 0 and Eflag:
          s=samples[:]
          resized=resize.resize_event(samples,100)
          now = datetime.datetime.now()
          event_node = etree.Element('event')
          loc_node = etree.Element('location')
          loc_node.text = loc
          event_node.append(loc_node)
          start_node = etree.Element('start')
          start_node.text = '{}:{}:{}'.format(now.hour,now.minute,now.second)
          event_node.append(start_node)
          vol_node = etree.Element('volume')
          vol_node.text = str(vol)
          event_node.append(vol_node)
          sample_node = etree.Element('samples')
          sample_node.text = ','.join(str(x) for x in s)
          event_node.append(sample_node)
          knn_node = etree.Element('knn')
          svm_node = etree.Element('svm')
          if not loc == 'unk': #{
            knn_node.text = classify.classify(resized,knn_model[loc],loc)
            svm_node.text = classify.classify(resized,svm_model[loc],loc)
          #}
          else: #{
            knn_node.text = 'unk'
            svm_node.text = 'unk'
          #}
          event_node.append(knn_node)
          event_node.append(svm_node)
          truth_node = etree.Element('truth')
          truth_node.text = g_truth
          event_node.append(truth_node)
          print etree.tostring(event_node,pretty_print=True)

          dirname = '/var/www/wmlog/';
          if not loc == 'unk': #{
            dirname = con.getLogging(loc);
          #}
          try:
            os.makedirs(dirname)
          except OSError:
            if os.path.exists(dirname):
              pass
            else:
              raise 
          filename='{}log{}_{}_{}'.format(con.getLogging(loc),now.day,now.month,now.year)
          try:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(filename,parser)
            root = tree.getroot()
            root.append(event_node)
            print 'new event appended on {}/{}/{} writing to file..'.format(now.day,now.month,now.year)
            f = open(filename,"w")
            f.write(etree.tostring(root,pretty_print=True))
            f.close()
          except IOError as e:
            print 'file does not exist, creating file..\n'
            f = open(filename,"w")
            root = etree.Element('events')
            root.append(event_node)
            f.write(etree.tostring(root,pretty_print=True))
            f.close()
            os.chmod(filename,0765);
            os.chown(filename,-1,33);
          except:
            print 'could not open {}'.format(filename)
          
        else:
          print 'Unknown source for data={}\n'.format(samples)
          print 'Data not logged - only logging data for..'
          print pirs
          print '\n'
    
      samples = []
      event=[]
      loc='unk'
    #}
    else: #{
      s1.open()
      s1.flushInput()
    #}
  s1.flushInput()
  s1.close() 

if __name__ == '__main__':
  main()
  
