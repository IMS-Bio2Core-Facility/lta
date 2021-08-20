# Lipid Trafficking Analysis

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/IMS-Bio2Core-Facility/lta/actions/workflows/cicd.yaml/badge.svg)](https://github.com/IMS-Bio2Core-Facility/lta/actions/workflows/cicd.yaml)
[![codecov](https://codecov.io/gh/IMS-Bio2Core-Facility/lta/branch/main/graph/badge.svg?token=2TGYX69U3N)](https://codecov.io/gh/IMS-Bio2Core-Facility/lta)
[![Project Status: WIP](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![Codestyle: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A python commandline interface for analysing lipidomics data.

The source code lives on [github][github].

The documentation lives at [ReadTheDocs][readthedocs].

The project can be installed from [PyPI][pypi].

## Abstract

Lipid Traffic Analysis (LTA) is a tool for using lipidomics data to test hypotheses about how metabolism is controlled.
Lipidomics data from several, metabolically connected tissues from control and experimental groups
can be used to plot the spatial or temporal distribution of lipids.
These distributions identify where changes in lipid metabolism occur and in which lipid pathways,
indicating the locus and biochemical alterations that occur in a given phenotype.
LTA was conceived in two parts.
One is an Abundance Analysis,
in which the error-normalised fold change (ENFC) for the control and given phenotype group is calculated.
Because the ratio of the control and experimental values is scaled by the error,
the ENFCs are easy to plot and compare between compartments.
The second part is a Switch Analysis.
This computes the presence of variables across the network.
Current development is focused on developing the technique for complex networks and on the rate of lipid transport.

## Using LTA from the command line

### Installation

#### Installing from PyPI

This is the most straightforward way to set up the tool.
When installing from PyPI,
we strongly reccomend using a virtual environment.
There are many ways to do this!
If you already have a preferred method -
I use [pipx][pipx] for command line tools -
feel free to use that.
Otherwise,
use the builtin Python module [venv][venv].
The exact instructions are OS-specific and detailed at the above link.
Instructions for installing the most recent version of LTA on MacOS are given below:

```shell
# Make a directory for the project
mkdir lta && cd lta
# Create the virtual environment
python3 -m venv .venv
# Activate the environment
source .venv/bin/activate
# Install lta
pip install -U lta
```

If you want to install a specific version,
then change the last line in the previous code block to:

```shell
pip install lta==0.5.0
```

replacing the version number with the version number you want.
A list of all released versions can be found at our [tags][tags].

#### Installing from Source

```{important}
Most users **will not need** these instructions.
```

If you need to customise the code in some manner,
you'll need to install from source.
To do that,
either clone the repository from github,
or download one of our releases.
For full instructions,
please see our guide on [contributing](./contributing.md).

### The Data

These should be CSV files where the first 11 rows contain sample data
and the first 3 columns contain the lipid metadata.
Within the sample metadata,
rows 4-9 should contain the:

- Sample ID
- Phenotype (*ie.* lean vs obese)
- Generation (*ie.* F1 vs F2)
- Tissue (*ie.* heart)
- Handling (any notes about sample prep)
- Mode (*ie.* -ve vs +ve)

respectively.
In order to read the data,
some assumptions about the format must be made.
Should we make any changes to data format expectations,
it will be well documented and will only occur in a major/breaking releas.

```{note}
We hope to generalise file reading in future releases to improve usability
in a future release.
```

### Running the analysis

Once you've installed the tool and activated your virtual environment,
running the analysis is as simple as:

```shell
lta data results
```

The first argument is the folder containing the raw data files.
If the folder doesn't exist,
or doesn't contain any data files,
the command will error with an apropriate message.
The secont argument identifies a folder in which the results will be saved.
It will be create if it doesn't exist.

If you ever have any questions about the tool,
you can access a condensed help menu by running:

```shell
lta -h
```

#### Customising

There are a few options that can be customised for any given run.
The statistics are calculated using a bootstrapping approach,
which (by definition) involves repeated replicates.
To control the number of replicates,
pass the ``-b/--boot-reps`` flag with a number.
Generally, more reps improves the accuracy of the estimates,
though I find little improvement beyond 20,000 reps
(the default number).

A critical step of the analysis is binarizing the lipid expression.
A lipid is classed as 0 in a tissue/condition if
the lipid is **not** detected in more than a particular fraction of cells.
The default values is 0.2 (one-fifth of the samples).
If you want to change it,
pass the ``-t/--threshold`` flag with a decimal between 0 and 1.
This value can have a significant impact on the analysis,
so explore how it impacts your data!

Many calculations are dependent on knowing where certain metadata is stored.
Namely, the experimental conditions (specified with ``--phenotype``)
and the tissue of origin (specified with ``--tissue``).
If these are not passed,
then they default to "Phenotype" and "Tissue", respectively.

For the fold-change calculation in ENFC to make any sense,
we need to know which group in ``phenotype`` is which.
You can specify this using the ``--order`` option like so:

```shell
lta data results --order obese lean
```

The first word following order will be treated as the experimental group,
while the second word will be treated as the control group.
In this example then,
fold-change would be give as ``obese / lean``.
If you don't specify,
this defaults to ``experimental control``.

If you find yourself regularly passing arguments via the CLI,
you might want to try a configuration file!
This is a simple text file that stores options in a simple format:

```shell
option=value
```

By default,
LTA looks for ``lta_conf.txt`` in your current directory.
However,
you can name this file whatever you want,
and let LTA know where to find it,
by passing the config flag like so:

```shell
lta -c path/to/your/config.txt data results
```

If you specify an option in the configuration file,
that will override LTA's defaults,
and specifying an option at the command line will override the configuration file!
The config file doesn't need do exist, however,
and is just a bit of sugar.

### The Output

```{warning}
Re-running the analysis overwrites existing results,
so be sure to either back up your data,
or pass a different output folder!
```

The output folder will contain a number of files.
For each type of lipid, you should see the following:

1. A csv with the lipid type and tissue (if relevant)
1. A csv ending in ``_counts.csv``
1. A csv ending in ``_jaccard.csv``

The first if a simple boolean list containing lipids that have been identified as
the relevant type in any condition found within ``--phenotype``.
The second contains these lipids counted and grouped by category.
Finally,
the third contains the Jaccard **distances** and a p-value,
calculated using the method outlined by [N. Chung, et. al.][jaccard].
If there are multiple modes within your data,
then there will be 2 of each file,
differentiated by the mode.

Additionally,
there will be two ENFC files per mode.
The firt contains the raw ENFC for each lipid,
grouped by tissue.
The second contains the mean and standard deviation of the ENFC,
grouped by lipid Category and split by tissue.
NaN/empty values mean that the lipid was a 0-lipid in that tissue.

## Contributing

Open-source software is only open-source becaues of the excellent community,
so we welcome any and all contributions!
If you think you have found a bug,
please log a report in our [issues][issues].
If you think you can fix a bug,
or have an idea for a new feature,
please see our guide on [contributing](./contributing.md)
for more information on how to get started!
While here,
we request that you follow our [code of conduct](./coc.md)
to help maintain a welcoming,
respectful environment.

## Citations

If you use LTA in your work,
please cite the following manuscripts:

1. Furse, S., Watkins, A.J., Hojat, N. *et al.* Lipid Traffic Analysis reveals the impact of high paternal carbohydrate intake on offsprings’ lipid metabolism. *Commun Biol* **4**, 163 (2021). [https://doi.org/10.1038/s42003-021-01686-1][paper_1]
1. Furse, S.[^eq], Fernandez-Twinn, D.S.[^eq], *et al.* Lipid metabolism is dysregulated before, during and after pregnancy in a mouse model of gestational diabetes. *Int. J. Mol. Sci.* **22**, 7452 (2021). [https://doi.org/10.3390/ijms22147452][paper_2]

[^eq]: These authors contributed equally to this work.

[github]: https://github.com/IMS-Bio2Core-Facility/lta "LTA Source Code"
[readthedocs]: HOLDING "LTA Documentation"
[pypi]: HOLDING "LTA PyPI Package"
[pipx]: https://pypa.github.io/pipx/ "pipx"
[venv]: https://docs.python.org/3/tutorial/venv.html "Python venv"
[tags]: https://github.com/IMS-Bio2Core-Facility/lta/releases "LTA releases"
[issues]: https://github.com/IMS-Bio2Core-Facility/lta/issues "LTA issues"
[jaccard]: https://doi.org/10.1186/s12859-019-3118-5 "Jaccard Probabilities"
[paper_1]: https://www.nature.com/articles/s42003-021-01686-1 "LTA citation 1"
[paper_2]: https://www.mdpi.com/1422-0067/22/14/7452 "LTA citation 2"
