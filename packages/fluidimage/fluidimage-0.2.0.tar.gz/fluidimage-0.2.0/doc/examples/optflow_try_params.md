# How to find good optical flow parameters?

Asynchronous topologies are not very convenient to look for the best parameters
for a computation. It is better to use the optical flow work directly as in
this example:

```{literalinclude} optflow_try_params.py
```

We see that we have to define an object `SeriesOfArrays` and to select one
serie (which represents here a couple of images). It is also what is done
internally in the topology. Have a look at [our tutorial](https://fluiddyn.readthedocs.io/en/latest/ipynb/tuto_serieofarrays.html) to
discover how to use this powerful tool!
