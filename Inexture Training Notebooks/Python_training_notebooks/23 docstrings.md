# What is a Docstring?

​					A docstring is a string literal that occurs as the first statement in a module, function, class, or method definition. Such a docstring becomes the `__doc__` special attribute of that object.



​					String literals occurring elsewhere in Python code may also act as documentation. They are not recognized by the Python bytecode compiler and are not accessible as runtime object attributes (i.e. not assigned to `__doc__`), but two types of extra docstrings may be extracted by software tools:



1. String literals occurring immediately after a simple assignment at the top level of a module, class, or `__init__` method are called "attribute docstrings".
2. String literals occurring immediately after another docstring are called "additional docstrings".



For consistency, always use `"""triple double quotes"""` around docstrings. Use `r"""raw triple double quotes"""` if you use any backslashes in your docstrings. For Unicode docstrings, use `u"""Unicode triple-quoted strings"""`.



## One-line Docstrings

One-liners are for really obvious cases. They should really fit on one line. For example:

```python
def kos_root():
    """Return the pathname of the KOS root directory."""
    global _kos_root
    if _kos_root: return _kos_root
    ...
```



```python
def function(a, b):
    """Do X and return a list."""
```



## Multi-line Docstring

- Multi-line docstrings consist of a summary line just like a one-line docstring, followed by a blank line, followed by a more elaborate description.

  ```python
  def complex(real=0.0, imag=0.0):
      """Form a complex number.
  
      Keyword arguments:
      real -- the real part (default 0.0)
      imag -- the imaginary part (default 0.0)
      """
      if imag == 0.0 and real == 0.0:
          return complex_zero
      ...
  ```

