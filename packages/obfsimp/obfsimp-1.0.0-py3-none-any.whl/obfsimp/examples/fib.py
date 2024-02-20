__all__=["fib"]
def fib(x):
  if x==0:
    return 0
  if x==1:
    return 1
  return fib(x-2)+fib(x-1)
if __name__=="__main__":
    x=int(input("Fibonacci: ")) # Comment
    print(fib(x=x))