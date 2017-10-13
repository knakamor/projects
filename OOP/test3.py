
#args: lst

def my_args(x, *args):
    print x
    for i in args:
        print '*' , i

my_args(10,20,40)

x=[]
my_args(*x)

#** Kwargs: dict

def my_kwargs(y, **kwards):
    for key in kwards:
        value =kwards[key]

h={}
my_kwargs(**h)

def my_args_kwargs(a, *args, **kwargs):
    for arg in args:
        print '*', arg
    for key in kwargs:
        value=kwargs[key]
        print '->', key, '=', value

my_args_kwargs(1,2,3, x=1,y=2,z=3)
