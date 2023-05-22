""" 
    Andrej Karpathy's Micrograd Exercises 
    Source: https://www.youtube.com/watch?v=VMj-3S1tku0
    Who: I did the exercise
    What: Micrograd exercises in review of neural networks
    When: Fen. 17th, 2023
    Why: I need to understand the ML fundamentals before building bigger projects.
    
    NOTE: Google Colab will not render on Bitbucket link, so this python file 
    is in replacement of the colab notebook contents.
"""

#---------------------------------------------------#
#------------------- Derviatives -------------------#
#---------------------------------------------------#

# here is a mathematical expression that takes 3 inputs and produces one output
from math import sin, cos

def f(a, b, c):
  return -a**3 + sin(3*b) - 1.0/c + b**2.5 - a**0.5

print(f(2, 3, 4))


# write the function df that returns the analytical gradient of f
# i.e. use your skills from calculus to take the derivative, then implement the formula
# if you do not calculus then feel free to ask wolframalpha, e.g.:
# https://www.wolframalpha.com/input?i=d%2Fda%28sin%283*a%29%29%29

# ------------------------------
# ------ START OF MY WORK ------
# ------------------------------
""" My thought process: This is manual derivation. No fancy tricks here."""
def df(a, b, c):
    -3*a**(3-1) + cos(3*b) *3 + c**(-2) + 2.5*b**(2.5 -1) - 0.5*a**(0.5 - 1)
    return [(-3*a**(3-1) -  0.5*a**(0.5 - 1)), (cos(3*b) *3 + 2.5*b**(2.5 -1)), (c**(-2))]

print(df(2, 3, 4))
# ----------------------------
# ------ END OF MY WORK ------
# ----------------------------


# RUN THIS TO TEST YOUR CODE 
def gradf(a, b, c):
    return df(a, b, c)

# expected answer is the list of 
ans = [-12.353553390593273, 10.25699027111255, 0.0625]
yours = gradf(2, 3, 4)
for dim in range(3):
  ok = 'OK' if abs(yours[dim] - ans[dim]) < 1e-5 else 'WRONG!'
  print(f"{ok} for dim {dim}: expected {ans[dim]}, yours returns {yours[dim]}")








#------------------------------------------------------#
#---------- Complete Value Class (Softmax) ------------#
#------------------------------------------------------#
from math import exp, log

# Andrej's Work
class Value:
    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
        self.label = label

    def __repr__(self):
        return f"Value(data={self.data})"
    
    def __add__(self, other): # exactly as in the video
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
    
        return out
  
    # PROMPT
    # re-implement all the other functions needed for the exercises below
    # ------------------------------
    # ------ START OF MY WORK ------
    # ------------------------------
    """
    My thought process: 
    1.) As referenced in the imported libraries above:
        - exp means natural exponent 'e'.
        - log means natural log, not log base of 10.
    2.) Make sure to convert any non-Value objects to be Value objects
    3.) Create _backward() method for each operator function to do derivations
        - Update the gradients of the value 
    4.) Account for switched ordering of data types when creating Value objects
    (e.g. (x * 2) vs. (2 * x))
    """    
    def exp(self):
        out = Value(exp(self.data), (self,), 'exp')

        def _backward():
            self.grad += out.data * out.grad
        
        out._backward = _backward
        return out 

    def log(self):
        out = Value(log(self.data), (self,), 'log')

        def _backward():
            self.grad += self.data**(-1) * out.grad

        out._backward = _backward
        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**(other), (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other - 1)) * out.grad
        
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward
        return out

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * (other**(-1))

    def __rtruediv__(self, other):
        return other * (self**(-1))

    def __neg__(self):
        return (-1) * self

    def __sub__(self, other):
        return self + (-other);

    def __rsub__(self, other):
        return other + (-self)

    def __radd__(self, other):
        return self + other

    # ----------------------------
    # ------ END OF MY WORK ------
    # ----------------------------



    # Andrej's Work
    def backward(self): # exactly as in video  
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
            for child in v._prev:
                build_topo(child)
            topo.append(v)
        build_topo(self)
        
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()
            
            
# RUN THIS TO TEST YOUR CODE 

# without referencing our code/video __too__ much, make this cell work
# you'll have to implement (in some cases re-implemented) a number of functions
# of the Value object, similar to what we've seen in the video.
# instead of the squared error loss this implements the negative log likelihood
# loss, which is very often used in classification.

# this is the softmax function
# https://en.wikipedia.org/wiki/Softmax_function
def softmax(logits):
  counts = [logit.exp() for logit in logits]
  denominator = sum(counts)
  out = [c / denominator for c in counts]
  return out

# this is the negative log likelihood loss function, pervasive in classification
logits = [Value(0.0), Value(3.0), Value(-2.0), Value(1.0)]
probs = softmax(logits)
loss = -probs[3].log() # dim 3 acts as the label for this input example
loss.backward()
print(loss.data)

ans = [0.041772570515350445, 0.8390245074625319, 0.005653302662216329, -0.8864503806400986]
for dim in range(4):
  ok = 'OK' if abs(logits[dim].grad - ans[dim]) < 1e-5 else 'WRONG!'
  print(f"{ok} for dim {dim}: expected {ans[dim]}, yours returns {logits[dim].grad}")









#-------------------------------------------------#
#----------------PyTorch Version------------------#
#-------------------------------------------------#
# PROMPT
# verify the gradient using the torch library
# torch should give you the exact same gradient

# ------------------------------
# ------ START OF MY WORK ------
# ------------------------------
"""
My thought process: 
1.) turn logits into a tensor input
2.) feed that tensor input into the softmax function, with dim=0.
We want dim=0 because we want the softmax activation to apply to the row axis. 
Softmax results should lie within the range of [0,1] and sum to 1.
3.) The output of pytorch is rounded up to 4 sigfigs, but they match the ones
calculated above from the class object
"""
import torch
logits = [0.0, 3.0, -2.0, 1.0]
input = torch.tensor(logits, dtype=torch.float64, requires_grad=True)
model = torch.nn.Softmax(input, dim=0)
out = -torch.log(model[3])
out.backward()
print(out)
# ------------------------------
# ------ END OF MY WORK ------
# ------------------------------


ans = [0.041772570515350445, 0.8390245074625319, 0.005653302662216329, -0.8864503806400986]
for dim in range(4):
  ok = 'OK' if abs(logits[dim].grad - ans[dim]) < 1e-5 else 'WRONG!'
  print(f"{ok} for dim {dim}: expected {ans[dim]}, yours returns {logits[dim].grad}")