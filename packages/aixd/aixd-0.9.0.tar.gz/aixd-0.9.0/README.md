# AI-eXtended Design (AIXD)

## Introduction

In the current repository we collect the code for the general methodology for AI-augmented generative design. This methodology allows to invert the standard paradigm of parametric modelling, where the designer needs to tweak and tune the input parameters, iteratively or through trial and error, for achieving some desired performance values. 

Instead, this method allows to, by just specifying the requirements' values, obtain a range of designs that closely approximate those. Besides, the present methodology allows the user to explore the design space, understand how different parameters relate to each other, areas of feasible and unfeasible designs, etc.

## Documentation

A detailed documentation of the ``aixd`` library is provided [here](https://docs.gramaziokohler.arch.ethz.ch/aixd/docs/). The documentation includes detailed installation instructions, API references, a user guide, application examples and more.

## Installation

Install using `conda`:

    conda env create -f environment.yml

This creates a conda environment called `aixd` with python 3.9 and all the dependencies defined in `requirements.txt` as well as installing the `aixd` package itself in editable mode.

## Development

If you are going to develop on this repository, also install the development requirements:

    pip install -e ".[examples, dev]"

Check the [contribution guidelines](CONTRIBUTING.md) for more details.

## Folders and structure

The structure we follow on the current repo is as follows:

* `examples` : all example applications of the `aixd` toolbox
* `src` : for all source code. It can be structure following the next structures
    * `src/aixd` : source code of `aixd` toolbox

## Known issues

* Plotly image export can cause a hang of the system. This is due to a bug in Kaleido (the library
  used by Plotly for image export) reported in [here](https://github.com/plotly/Kaleido/issues/134). A workaround is to
  downgrade Kaleido to version `0.1.0.post1`, which can be done by running `pip install kaleido==0.1.0.post1`. 

