
from profiler import profile, Profiler
import time


# Define a couple of functions to be profiled

@profile
def mult(x, y):
    time.sleep(0.01) # sleep for 1/100th of a second
    return x * y


@profile
def table(m, n):
    for i in range(m):
        for j in range(n):
            prod = mult(i,j)
            print(i, j, prod)




class MyClass:
    def __init__(self):
        pass

    @profile
    def run_tables(self, m, n):
        table(m, n)
        table(n, m)



# Run some code

def main():

    mc = MyClass()

    mc.run_tables(10, 10)

    Profiler.report()

if __name__ == '__main__':
    main()



