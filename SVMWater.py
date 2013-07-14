import sys;
import time;
import numpy;
import configC;
from sklearn import svm, grid_search;
from ConfigParser import SafeConfigParser;



def getBestParams(X,y,cVals,gVals): #{
  C = 0;
  gamma=0;
  score=0;
  
  #cVals = numpy.arange(0.1,1.5,0.2).tolist();
  #gVals = numpy.arange(0.000001,0.000016,0.000003).tolist();
  param={'kernel':['rbf'],'C':cVals,'gamma':gVals};
  print 'Estimating best parameters, please wait this could take a while..';
  svr = svm.SVC();
  clf = grid_search.GridSearchCV(svr,param);
  clf.fit(X,y)
  C = clf.best_params_['C'];
  gamma = clf.best_params_['gamma'];
  score = clf.best_score_
  return C,gamma,score;
#}

def main(): #{

  if (len(sys.argv) < 2): #{
    sys.stderr.write("E: usge: " + sys.argv[0] + " <room>\n");
    sys.stderr.flush();
    exit(1);
  #}
  else: #{
    room = sys.argv[1];
  #}

  parser=SafeConfigParser();
  con = configC.config('wm_config.ini',parser);
  data = numpy.genfromtxt(con.getDataFile(room),delimiter=',');
  m,n = numpy.shape(data);
  X = data[:,0:n-1];
  y = data[:,n-1];
  start = time.clock();
  c_list,g_list = con.getParamList(room);
  C, gamma, score = getBestParams(X,y,c_list,g_list);
  end = time.clock();
  minutes, seconds = divmod(end-start, 60)
  hours, minutes = divmod(minutes, 60)
  print 'Estimation took ' + '%d:%02d:%02d' % (hours,minutes,seconds);
  print 'The chosen values of C={} and gamma={}, produced an accuracy of {:.2%}'.format(C,gamma,score);
  con.setOption(room,'C',str(C));
  con.setOption(room,'gamma',str(gamma));
  con.writeConfig();

if (__name__ == "__main__"): #{
  main();
#}
