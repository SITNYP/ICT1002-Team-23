import subprocess
import sys

def installWheel(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])
    
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", "-r", package])

try:
    
    installWheel('.\packages\pandas-0.24.2-cp27-cp27m-win_amd64.whl')
    installWheel('.\packages\PyQt4-4.11.4-cp27-cp27m-win_amd64.whl')
    install('requirements.txt')
    

    print "Dependecies installed! You are now ready to run the Data Analyser."
except:
    print "An error occurred! Please ensure that Pip is up-to-date and try again!"