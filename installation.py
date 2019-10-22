from pip._internal import main as pipmain

try:
  pipmain(['install', '.\packages\pandas-0.24.2-cp27-cp27m-win_amd64.whl'])
  pipmain(['install', '.\packages\PyQt4-4.11.4-cp27-cp27m-win_amd64.whl'])
  pipmain(['install', 'matplotlib'])
  pipmain(['install', 'pdfkit'])
  pipmain(['install', 'imgkit'])
  pipmain(['install', 'scipy'])
  pipmain(['install', 'scikit-learn'])

  print "Dependecies installed! You are now ready to run the Data Analyser."
except:
  print "An error occurred! Please ensure that Pip is up-to-date and try again!"
