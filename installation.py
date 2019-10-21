from pip._internal import main as pipmain

pipmain(['install', 'pandas'])
pipmain(['install', '.\pyqt4 package\PyQt4-4.11.4-cp27-cp27m-win_amd64.whl'])
pipmain(['install', 'matplotlib'])
pipmain(['install', 'pdfkit'])
pipmain(['install', 'imgkit'])
pipmain(['install', 'sklearn'])

print "Dependecies installed! You are now ready to run the Data Analyser."