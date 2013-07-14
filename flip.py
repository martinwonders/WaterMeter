import sys;
import numpy;

def flip_data(data):

  if (data.ndim == 1): #{
    data = numpy.atleast_2d(data);
  #}
  m,n = numpy.shape(data);
  flipped = numpy.zeros((m,n))
  n=n-1
  y = data[0,n]
  flipped[:,n] = y

  for i in range(m):
    k = 0
    for j in range(1,n+1):
      if data[i,n-j] != 0:
        flipped[i,k] = data[i,n-j]
        k = k + 1


  return flipped





def main():
  if len(sys.argv)==3:
    infile=sys.argv[1]
    outfile=sys.argv[2]
  else:
    print 'usage {} inputfile ouptfile'.format(sys.argv[0])
    exit(1)
  
  data=numpy.genfromtxt(infile,delimiter=',',dtype=int)
  new = flip_data(data)
  numpy.savetxt(outfile,new,delimiter=',',fmt='%i')
  

  
if __name__ == '__main__':
  main()
