import numpy;
import sys;

def shift_data(data,tails,threshold): #{
  """ (list,int,int)->numpy.array

  x=[118,118,121,118,136,278,287,290,142,130,127,127,127,127,127,
  124,127,127,127,127,127,127,127,130,124,37,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4]
  >>> n = shift_data(x,2,10)
  >>> numpy.shape(n)
  (34, 101)

  returns a numpy array that has data in the first row, subsequent
  rows up to halfway contain data with the raised portion shifted
  to the right. the remaining rows contain the previous rows flipped
  from right to left.
  """
  
  shifted=[];
  flipped=[];
  n = numpy.shape(data);
  n=n[0]-1;
  y = data[n];
  ind = numpy.nonzero(numpy.array(data)==0);
  
  if (len(ind[0]) == 0): #{
    sig_end = n;
  #}
  else: #{
    sig_end = ind[0][0];
  #}
     
  mid = sim(data[tails:sig_end-tails],threshold);
  
  if numpy.shape(numpy.atleast_2d(mid))[0] > 1: #{
    flipped  = numpy.fliplr(mid);
    mid = numpy.vstack((mid,flipped));
    shifted = numpy.zeros((numpy.shape(mid)[0],n+1),dtype=int);
    shifted[:,0:tails] = data[0:tails];
    shifted[:,sig_end-tails:sig_end+1] = data[sig_end-tails:sig_end+1];
    shifted[:,n]=y;
    shifted[:,tails:numpy.shape(mid)[1]+tails] = mid[:,:];
    return shifted;
  #}
  else: #{
    print 'Data couldn\'t be shifted, returning original data....';
    return data;
  #}
#}

def rand(l): #{
  """ (list)->int

  returns and int that is +/-2 from the average of the list

  >>>rand([18,20,22,21])
  18 to 22
  >>>rand([18,20,22,21,22])
  19 to 23
  >>>rand([120,130,122,118,125])
  121 to 125
  >>>rand([120])
  120
  """
  if len(l) > 1: #{
    ave = numpy.average(l);
    return int(numpy.around(ave)) + numpy.random.randint(-2,3);
  #}
  else:#{
    return l[0];
  #{
#}

def find_lump(l,threshold): #{
  """ (list,int)-> (int,int)

  Return the indices of a raised section in a list of integers.
  The raised section is defined by a threshold.
  
  >>> find_lump([120,120,370,370,370,250,250,250],50)
  (1,5)
  >>> find_lump([120,120,120,120,120,370,370,370],50)
  (4,-1)
  >>> find_lump([370,370,370,120,120,120,120,120],50)
  (0,3)
  >>> find_lump([120,120,120,120,370,370,370,120],50)
  (3,7)
  >>> find_lump([120,120,370,370,370,250,250,250],50)
  (1, 5)
  >>> find_lump([120,120,120,120,120,120,120,120],50)
  (0, -1)
  >>> find_lump([120,120,120,120,169,169,169,120],50)
  (0, -1)
  """
  
  flag = False;
  start = 0;
  end = -1;
  ind=0;
  print l
  for item in l: #{
      if not flag  and ind < len(l)-1 and (item + threshold) < l[ind+1]: #{
          start = ind;
          flag=True;
      #}
      elif ind < len(l)-1 and (item - threshold) > l[ind+1]: #{
          end = ind+1;
          break;
      #}
      ind=ind+1;
  #}
  print 'found start at sample {} and end at sample {}'.format(start,end);
  return start,end;

#}

def shift(l,threshold): #{
  """ (list, int)->list

  Returns a list where a rise in a range of numbers is detected
  and shifted one place up the list. The rise is detected using
  threshold.
  
  >>> shift([370,370,370,120,120,120,120,120],50)
  [120,370,370,370,120,120,120,120]
  >>> shift([120,120,120,120,120,370,370,370],50)
  [120,120,120,120,120,370,370,370]
  >>> shift([120,120,120,120,370,370,370,120],50)
  [120,120,120,120,120,370,370,370]
  >>> shift([120,120,120,370,370,370,120,120],50)
  [120,120,120,120,370,370,370,120,]
  >>> shift([120,120,370,370,370,250,250,250],50)
  [120, 120, 120, 370, 370, 370, 250, 250]
  """
  shifted=[0] * len(l);
  start,end = find_lump(l,threshold);
  lump_len = end - start;
  if end == -1: #{
    return l;
  #}
  elif start == 0: #{
    shifted[0] = rand(l[end:]);
    shifted[1:1+end] = l[0:end];
    shifted[1+end:] = l[end:-1];
  #}
  else: #{
    shifted[0:start+1] = l[0:start+1];
    shifted[start+1] = rand(l[0:start+1]); #stuffing
    shifted[start+2:start+1+lump_len] = l[start+1:start+lump_len];
    if start+1+lump_len < len(l): #{
      shifted[end+1:] = l[end+1:];
    #{
  #}
  return shifted;
#}

def sim(l,threshold): #{
  """ (list,int) -> numpy.array

  >>> sim([120,120,370,370,370,250,250,250],50)
  array([[120, 120, 370, 370, 370, 250, 250, 250],
       [120, 120, 120, 370, 370, 370, 250, 250],
       [120, 120, 120, 120, 370, 370, 370, 250],
       [120, 120, 120, 120, 120, 370, 370, 370]])
  >>> sim([120, 120, 120, 370, 370, 370, 120, 120],50)
  array([[120, 120, 120, 370, 370, 370, 120, 120],
       [120, 120, 120, 120, 370, 370, 370, 120],
       [120, 120, 120, 120, 120, 370, 370, 370]])
  >>> sim([120,120,120,120,120,370,370,370],50)
  array([120, 120, 120, 120, 120, 370, 370, 370])
  >>> sim([370,370,370,120,120,120,120,120],50)
  array([[370, 370, 370, 120, 120, 120, 120, 120],
       [120, 370, 370, 370, 120, 120, 120, 120],
       [120, 120, 370, 370, 370, 120, 120, 120],
       [120, 120, 120, 370, 370, 370, 120, 120],
       [120, 120, 120, 120, 370, 370, 370, 120],
       [120, 120, 120, 120, 120, 370, 370, 370]])
  """
  x = numpy.array(l);
  start,end = find_lump(l,threshold);
  
  if end == -1: #{
    print 'cannot be shifted adjust threshold..'
    new = numpy.array(l,dtype=int);
    return new;
  #}
  
  count = len(l)-end;
  new = numpy.zeros((count,len(l)),dtype=int);
  new = numpy.vstack((x,new));
  
  for i in range(count): #{
    new[i+1] = shift(new[i],threshold);
  #}
  
  return new;
#}


def main(): #{
  
  if len(sys.argv)==5: #{
    infile=sys.argv[1];
    outfile=sys.argv[2];
    tails=sys.argv[3];
    threshold=sys.argv[4];
  #}
  else: #{
    print 'usage {} <inputfile> <outfile> <tails> <threshold>\n'.format(sys.argv[0])
    exit(1)
  #}

  data=numpy.genfromtxt(infile,delimiter=',',dtype=int);
  new = shift_data(data,tails,threshold);
  numpy.savetxt(outfile,new,delimiter=',',fmt='%i');

#}

  
#if __name__ == '__main__': #{
#  main();
#}
