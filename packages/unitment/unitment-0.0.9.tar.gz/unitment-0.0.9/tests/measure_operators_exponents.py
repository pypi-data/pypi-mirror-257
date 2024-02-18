# Header
if(True):
  __doc__          = "This module contains unit tests. Passed 0.0.1"
  __version__      = "0.0.1"
  __reverse_path__ = "../"
  
  # Python Standard Imports
  import sys, os
  
  # Python Math Imports
  if(True):
    import math,cmath,random
    from decimal import *
    from numbers import Number
  
  # Logging Functions
  if(True):
    import logging, types
    
    global log
    log = logging.getLogger()
    
    def log_func(func,context,name=None):
      # Simplify Variables
      name = name if(name!=None) else func.__name__
      # Context: Extend for Non-Nested, Replace for Nested
      if(log.name == "root"): context = context  + "." + name
      else:                   context = log.name + "." + name
      context = ".".join([_.strip("_") for _ in context.split(".")])
      # Wrappers to Update Context
      def log_wrapper(*args, **kwargs):
        # Log with Context
        global log
        log = logging.getLogger(context)
        out = func(*args, **kwargs)
        log = logging.getLogger()
        return out 
      # Return Wrapped Function
      return log_wrapper
    def log_class(cls,context):
      # Add Context
      context = context + "." + cls.__name__
      # Iterate over class dict
      for name, obj in vars(cls).items():
        is_function = callable(obj) and not isinstance(obj,type)
        is_class    = callable(obj) and     isinstance(obj,type)
        if(is_function): setattr( cls, name, log_func( obj,context,name=name) )
        if(is_class):    setattr( cls, name, log_class(obj,context) )
      return cls
    def log_this(obj,context=None):
      # Initial Context
      if(context==None):context = __name__
      # Sort
      is_function = callable(obj) and not isinstance(obj,type)
      is_class    = callable(obj) and     isinstance(obj,type)
      # Return
      if(is_function): return log_func( obj,context)
      if(is_class):    return log_class(obj,context)
  
  # Repo-Script for Repo-Imports
  if(True):
    # Define Repo-Library Path.
    _file_dir_     = os.path.dirname(__file__)
    _repo_dir_     = os.path.join(_file_dir_, __reverse_path__)
    _repo_lib_dir_ = os.path.join(_repo_dir_, "src/")
    _repo_lib_dir_ = os.path.normpath(_repo_lib_dir_)
    # Add Repo-Library to Path.
    if(_repo_lib_dir_ not in sys.path): sys.path.insert(0, _repo_lib_dir_)
  
  # Additional Imports
  import pytest
  from unitment import AmbiguousUnitException,IncompatibleUnitException,UnitException,Unit,Measure
  import unitment as measure

#
class TestMeasureOperatorsExp:
  # Exponents
  def test_power(self):
    # Measure (Explicit Error) * Measure (Explicit Error) = Measure (Explicit Error)
    if(True):
      # set-up
      a = Measure("4(2)cm")
      b = Measure("6(1)cm/cm")
      three = Decimal("3")
      c = Measure("4096(13536)cm^6")
      d = Measure("64(96)cm^3")
      e = Measure("729(800)")
      # assert
      assert (a**b).approx(c)
      assert (a**three).approx(d)
      assert (three**b).approx(e)
      # Implied Uncertainty
      f = Measure("4")
      g = Measure("6")
      assert (f**g).implied == True
      assert (f**three).implied == True
      # Exceptions
      with pytest.raises(Exception):
        Measure("0")**Measure("0")
  
  def test_log(self):
    assert Measure.log(Measure("6(1)"),base=Measure("4(2)")).approx(Measure("1(2.97)"))
    assert Measure.log(Decimal("3"),   base=Measure("4(2)")).approx(Measure("1.26(43)"))
    assert Measure.log(Measure("6(1)"),base=Decimal("3")   ).approx(Measure("1.63(2)"))
    # Implied Uncertainty
    f = Measure("4")
    g = Measure("6")
    assert Measure.log(g,base=f).implied == True
    assert Measure.log(3,base=f).implied == True
    
    # Exceptions
    with pytest.raises(IncompatibleUnitException):
      Measure.log(Measure("12 mg"),base=Measure("2 mg"))
  
  def test_ln(self):
    assert -0.02 < Measure("0.99").ln() < 0
  