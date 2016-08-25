# Resource-Allocator
Resource Allocator in Python

Run as script:
--------------
Give the input in command line

Use as module:
--------------
Call `get_costs` method with the following arguments

```
  ResourceAllocator.get_costs(zdict,hours,cores,price)
```

Input
-----

* Instances - Zone information in dict format
* hours - Number of hours
* cpus - Minimum number of CPUs
* price - Maximum price user is able to pay
