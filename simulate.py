import numpy;
import sys;
from scipy import stats;

def new_data(data): #{
  z=[];                     #used to store the index of zeroed elements
  m,n=numpy.shape(data);    #get the dimensions of the matrix
  y=int(data[0,n-1]);       #extract the classification from the last column  
  sim_length = numpy.zeros(m) #create a 2 element array to store the lengths
  for i in range(m):
    z.append(numpy.nonzero(data[i,:]==0)[0])
    if len(z[i])>0:
      sim_length[i] = z[i][0]
    else:
      sim_length[i] = n

  longest = max(sim_length)
  shortest = min(sim_length)
  
  i=0
  for i in range(m):
    length = sim_length[i]
    if length<longest:
      stuffing = int(longest-length)
      start=int(numpy.floor(length/2))
      
      
      x= numpy.zeros((stuffing-1,n),dtype=int)
      in_proc_stretch = numpy.vstack((data[1,:],x))
      offset = start; 
      for j in range(1,stuffing):
        in_proc_stretch[j,0:offset]=in_proc_stretch[j-1,0:offset]
        md = stats.mode(data[0,0:sim_length[0]-1])
        in_proc_stretch[j,offset]= md[0]+numpy.random.random_integers(-3,3)
        in_proc_stretch[j,offset+1:length+1] = in_proc_stretch[j-1,offset:length]
        length=length+1
        offset=offset+1
      
      
    else:
      shrinkage = int(length-shortest)
      x = numpy.zeros((shrinkage-2,n),dtype=int)
      in_proc_shrink = numpy.vstack((data,x))
      in_proc_shrink[1,:]= 0
      
      for j in range(0,shrinkage-1):
        md = stats.mode(in_proc_shrink[j,0:length])
        ind = numpy.nonzero(in_proc_shrink[j,0:length]==md[0])
        in_proc_shrink[j+1,0:ind[0][-1]] = in_proc_shrink[j,0:ind[0][-1]]
        in_proc_shrink[j+1,ind[0][-1]:-2] = in_proc_shrink[j,(ind[0][-1]+1):-1]
        length = length-1
      
      
  in_proc_stretch[:,n-1]=y
  in_proc_stretch[:,0:start]=data[0,0:start]
  print in_proc_stretch
  in_proc_shrink[:,n-1]=y
  in_proc_shrink[:,0:start]=data[1,0:start]
  print in_proc_shrink
  
  sim_data = numpy.vstack((in_proc_stretch,in_proc_shrink))
  
  return sim_data


def main():
  if len(sys.argv)==3:
    infile=sys.argv[1]
    outfile=sys.argv[2]
  else:
    print 'usage {} inputfile ouptfile'.format(sys.argv[0])
    exit(1)

  data=numpy.genfromtxt(infile,delimiter=',',dtype=int)
  sim = new_data(data)
  numpy.savetxt(outfile,sim,delimiter=',',fmt='%i')
  

  
if __name__ == '__main__':
  main()
