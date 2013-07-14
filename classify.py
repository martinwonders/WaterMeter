import sys
import numpy
import sklearn
import configC
from ConfigParser import SafeConfigParser;
from sklearn import neighbors
from sklearn import svm


def train_knn(X,y,k):
  knn_model = neighbors.KNeighborsClassifier(k)
  knn_model.fit(X,y)
  return knn_model

def train_svm(X,y,penalty,coef):
  svm_model = svm.SVC(kernel='rbf',C=penalty,gamma=coef)
  svm_model.fit(X,y)
  return svm_model

def classify(event,model,room):
  parser=SafeConfigParser()
  con = configC.config('wm_config.ini',parser)
  return con.getClassLabel(room,int(model.predict(event)))

def test_model(model,X,y):
  correct=0
  count=0
  pred=[]
  for i,e in enumerate(X):
    if model.predict(X[i])==y[i]:
        correct = correct+1
    count=i

  return (correct/float(count))*100
  
  
  
  return accuracy

def get_data(csv_file_train):
  data=numpy.genfromtxt(csv_file_train,delimiter=',')
  X_train = data[:,0:100]
  y_train = data[:,100]

  return X_train,y_train

def main():
  if len(sys.argv)==3:
    csv_file_train = sys.arg[1]
    csv_file_train = sys.arg[2]
  else:
    csv_file_train = 'Allsimulated.csv'
    csv_file_test = 'water_labelled_train.csv'

  print 'gathering data...','\n'
  X_train,y_train = get_data(csv_file_train)
  X_test,y_test = get_data(csv_file_test)

  knn_model = train_knn(X_train,y_train,1)
  svm_model = train_svm(X_train,y_train)
   
  print 'testing knn..','\n'
  print 'knn model accuracy=', test_model(knn_model,X_test,y_test),'%\n'
  print 'testing svm..','\n'
  print 'svm model accuracy=', test_model(svm_model,X_test,y_test),'%\n'

def resize_event(data,width):
  n = len(data)
  window = numpy.zeros(width)
  while n > width:
    m,q = stats.mode(data)
    ind = data.index(m[0])
    del data[ind]
    n=len(data)

  if len(data)<=width:
    n=len(data)-1
    window[0:n]= data[0:n]
    data = window

  return data


if __name__ == '__main__':
  main()
