import sys;
import os;
import serial;
import numpy;
from ConfigParser import SafeConfigParser;
import configC;
import resize;
import simulate;
import shiftCompound;
import flip;

def main(): #{
  room='';
  device='';
  compound=False;
  sample_no=2;
  if (len(sys.argv) < 3): #{
    sys.stderr.write("E: usge: " + sys.argv[0] + " <room> <device> [<true/false>]\n");
    sys.stderr.flush();
    exit(1);
  #}
  else: #{
    room = sys.argv[1];
    device = sys.argv[2];
    if (len(sys.argv) == 4): #{
      compound = (sys.argv[3][0].upper()=='T');
      sample_no = 1;
      print 'generating training data for a compound event using 1 sample..\n';
    #}
  #}
  parser=SafeConfigParser();
  con = configC.config('wm_config.ini',parser);
  rooms = con.getDict();
  s1 = serial.Serial(con.getSerialData(),9600);
  s1.open();
  s1.flushInput();
  print('serial open...\n');
  count=0;
  sample = [];
  
  while (count < sample_no): #{
    print ('Waiting for flow data count:{} - from {} {}\n'.format(count+1,room, device));
    ml = s1.readline();
    if ('<' in ml): #{
      ml = s1.readline();
      ml = ml.strip('\r\n');
      while ('>' not in ml): #{
        print(ml);
        sample.append(int(ml));
        ml = s1.readline();
        ml = ml.strip('\r\n');
      #}
      vol= sum(sample);
      if (vol > 0): #{  
        if (count==0): #{
          s = resize.resize_event(sample,101);
          s[100]=con.getClass(room,device);
          count = count + 1;
        #}
        else: #{
          s = numpy.vstack((s,[resize.resize_event(sample,101)]));
          s[:,100]=con.getClass(room,device);
          count = count + 1;
        #}
      #}
      else: #{
        print 'no data ={}\n'.format(sample);
      #}
    #}
    sample = [];
    
  #}
  s1.close();
  
  
  if (compound): #{
    print 'modifying data with tails={} and threshold={}'.format(con.getTails(),con.getThreshold());
    sim = shiftCompound.shift_data(s,con.getTails(),con.getThreshold());
    sim = numpy.atleast_2d(sim);
  #}
  else: #{
    sim = simulate.new_data(s);
    flipped = flip.flip_data(sim);
    sim = numpy.vstack((sim,flipped));
  #}
  
  new = len(sim);
  print 'Data simulated for {} {}.\n'.format(room,device);
  r = room[0].upper() + room[1:len(room)];
  f = 'AllSim{}.csv'.format(r);
  if os.path.isfile(f): #{
    data=numpy.genfromtxt(f,delimiter=',');
    sim = numpy.vstack((data,sim));
  #}
  print 'Saving data in {}\n'.format(f);
  numpy.savetxt(f,sim,delimiter=',',fmt='%i');
  print '{} Samples of data saved\n'.format(new);
#}

if (__name__ == "__main__"): #{
  main();
#}
