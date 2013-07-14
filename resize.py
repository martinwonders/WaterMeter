import numpy;
from scipy import stats;
import sys;


def resize_event(data,length): #{
  '''(list,int) -> list
  
  resizes the list data to the length

  >>> resize_event([2,3,3,2],2)
  '''  
  n = len(data);
  window = numpy.zeros(length);
  while (n > length): #{
    m,q = stats.mode(data);
    ind = data.index(m[0]);
    del data[ind];
    n=len(data);
  #}
  if (len(data)<=length): #{
    n=len(data);
    window[0:n]= data[0:n];
    data = window;
  #}
  return data;
#}

def main(): #{
  if (len(sys.argv)==4): #{
    infile=sys.argv[1];
    outfile=sys.argv[2];
    length=int(sys.argv[3]);
  #}
  else: #{
    print 'usage {} inputfile ouptfile length'.format(sys.argv[0]);
    exit(1);
  #}
  
  data=numpy.genfromtxt(infile,delimiter=',',dtype=int);
  new = numpy.array([resize_event(data,length)]);
  numpy.savetxt(outfile,new,delimiter=',',fmt='%i');
  
#}
  
if (__name__ == '__main__'): #{
  main()
#}
