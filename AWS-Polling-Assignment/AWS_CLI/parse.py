
import os, sys
import glob
import importlib
# package import 

basedir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, basedir)
resource = glob.glob(os.path.join(basedir+'/*', '*.py'))
__files__ = [ os.path.basename(fl)[:-3] for fl in resource if os.path.isfile(fl) and not fl.endswith('__init__.py')]

# import the desired method 

def callBack(methodName):
  processedRes = list()
  try:
    count =0
    for fl in __files__:
      mod = importlib.import_module('mod.'+fl)
      classname = dir(mod)[0]
      
      # execute the modal function
      if getattr(mod, classname):
        classCall = getattr(mod, classname)
        if methodName in dir(classCall):
          method = classCall.sum(3,4)
          processedRes.append(method)
          count+=1
      
        else:
          print("Method Doesn't exists in {} " .format(fl))    

    return processedRes
    
  except Exception as e:
    print(str(e))
    exit()
    

if __name__ == '__main__':
  output = callBack(methodName='sum')
  print(output)