# Lipid Traffic Analysis

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/lipidta)](https://pypi.org/project/gtexquery/)
[![Python Versions](https://shields.io/pypi/pyversions/lipidta)](https://shields.io/pypi/pyversions/lipidta)
[![CI/CD](https://github.com/IMS-Bio2Core-Facility/lta/actions/workflows/cicd.yaml/badge.svg)](https://github.com/IMS-Bio2Core-Facility/lta/actions/workflows/cicd.yaml)
[![codecov](https://codecov.io/gh/IMS-Bio2Core-Facility/lta/branch/main/graph/badge.svg?token=2TGYX69U3N)](https://codecov.io/gh/IMS-Bio2Core-Facility/lta)
[![Documentation Status](https://readthedocs.org/projects/lta/badge/?version=latest)](https://lta.readthedocs.io/en/latest/?badge=latest)
[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Codestyle: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

**aka LTA, aka LipidTA**

A python commandline interface for analysing lipidomics data.

The source code lives on [github][github].

The documentation lives at [ReadTheDocs][readthedocs].

The project can be installed from [PyPI][pypi].

## Abstract

Lipid Traffic Analysis (LTA) is a tool for using lipidomics data to test hypotheses about how metabolism is controlled.
Lipidomics data from several, metabolically connected tissues from control and experimental groups
can be used to plot the spatial or temporal distribution of lipids.
These distributions identify where changes in lipid metabolism occur and in which lipid pathways,
indicating the locus and biochemical alterations that occur in a given group.
LTA was conceived in two parts.
One is an Abundance Analysis,
in which the error-normalised fold change (ENFC) for the control and given group group is calculated.
Because the ratio of the control and experimental values is scaled by the error,
the ENFCs are easy to plot and compare between compartments.
The second part is a Switch Analysis.
This computes the presence of variables across the network.
Current development is focused on developing the technique for complex networks and on the rate of lipid transport.

### On Version Numbers

```{admonition} TLDR
Prior to version 3,
the Python implementation version **does not** correlate to the academic versions.
From version 3,
the Python and academic versions are the same.
```

LTA was developed initially in R,
producing [LTA v1.0][lta_v1].
This was used for the LTA in the first study to use the analysis,
based on the hypothesis that differing carbohydrate intakes by fathers
influenced their children's and grandchildren's lipid metabolism.
See [Furse et al 2021][paper_1].
The code was developed further in R to improve convenience for the user,
and features such as the 0s threshold
(the number of samples in which there is a non-zero value for abundance for it to count as present)
was added for LTA v2.3.
This version has been used in three subsequent studies.
Please see [here][paper_2],
[here][paper_3],
and [here][paper_4].
A desire to add more features and move to a more stable platform led us to move to Python for LTA v3.0.

The Python implementation of LTA has strictly used automated semantic versioning over the course of its development.
Thus,
prior to version 3,
**the version numbers of the Python inplementation and past R implementations have no correlation.**
By convenient coincidence,
the semantic versioning release of LipidTA v3 brings
the python versioning and the academic versioning in-line.

## Using LTA from the command line

### Installation

Any installation of this tool requires Python.
How to install Python correctly is beyond this scope,
but there are some excellent resources available
[here][realpython]
and [here][psf].
If you are planning to have multiple versions of python installed,
you might want to consider [pyenv][pyenv].

```{warning}
We only support Python {math}`>=` 3.7.1
```

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
pip install -U LipidTA
```

```{note}
Our pip package is `LipidTA`.
Unfortunately,
`lta` was "too similar to existing package names",
so PyPi wouldn't let us use it.
```

If you want to install a specific version,
then change the last line in the previous code block to:

```shell
pip install LipidTA==1.0.0
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

(data)=

### The Data

The input should be a csv containing the lipidomics results.
Though we strive to be as flexible as possible,
we must make some assumptions about the data to be able to use it.
Firstly,
the first 3 columns must be the multiindex for the lipids,
and include the lipid name,
category,
and m/z, respectively.
Secondly,
the values must be numeric.

The analysis depends on a number of key metadata variables,
namely:

- Mode: the lipidomics mode
- Sample ID: a unique sample identifier
- Group: the experimental condition
- Compartment: the comartment of origin for the sample

These rows should be in the first {math}`n` rows of your data file,
where n is specified with the option `--n-rows-metadata`.
You can name these metadata rows whatever you want in the data file,
and tell `lta` where to find them with the appropriate flags.
We've done our best to choose sane defaults
(please see the section on [default values](defaults)),
and you can see the section on [customising your run](customising)
for more details.
However,
if these data are not present,
the tool will not run,
as the analysis only makes sense in the context of these variables.

```{important}
Should we make any changes to data format expectations,
it will be well documented and will only occur in a major/breaking releas.
```

### Running the analysis

Once you've installed the tool and activated your virtual environment,
running the analysis **can** be as simple as:

```shell
lta data.csv results
```

The first argument is path to the combined input file.
If the file doesn't exist,
is a directory,
or doesn't contain any data files,
the command will error with an apropriate message.
The secont argument identifies a folder in which the results will be saved.
It will be created if it doesn't exist.

```{important}
To help get you up and running,
a minimum dataset and configuration file are provided [here][examples].
```

(defaults)=

#### The Defaults

To keep it as simple as above,
you will need to use the defaults,
outlined in the below table:

| Parameter | Description | Default |
| :--- | :---: | ---: |
| threshold | The fraction of samples in which a lipid is 0 before it is dropped | 0.3 |
| boot-reps | The number of bootstrap repetitions used to calculate probability | 1000 |
| n-rows-metadata | The number of rows of metadata at the beginning of the data file| 11 |
| group | The metadata row containing experimental conditions | Group |
| control | The "control" condition, used as reference for fold change | control |
| comartment | The metadata row containing the compartment of origin for each sample | Compartment |
| mode | The metadata row containing the lipidomics mode | Mode |
| sample-id | The metadata ro containing unique sample identifiers | SampleID |

Don't worry if it looks intimidating!
You can check out the section on [customising your run](customising)
for further details,
and help can always be found at our [documentation][readthedocs]
or from the command line with:

```shell
lta -h
```

(customising)=

#### Customising

While it can be that simple,
you'll likely have to customise some options for your run.
In that case,
it will likely look a bit more like:

```shell
lta --n-rows-metadata 11 \
--group Group \
--control lean \
--compartment Compartment \
--sample-id mouse
```

Alternatively,
you might prefer to use a configuration file to keep things simple.
In that case,
see the section on [configuration](configuration)
for more information.

There are a few options that can be customised for any given run.
The statistics are calculated using a bootstrapping approach,
which (by definition) involves repeated replicates.
To control the number of replicates,
pass the ``-b/--boot-reps`` flag with a number.
Generally, more reps improves the accuracy of the estimates,
though I find little improvement beyond 20,000 reps.
1000 (the default number) seems to provide a good balance between speed and accuracy.

A critical step of the analysis is binarizing the lipid expression.
A lipid is classed as 0 in a compartment/condition if
the lipid is **not** detected in more than a particular fraction of samples.
The default values is 0.2 (one-fifth of the samples).
If you want to change it,
pass the ``-t/--threshold`` flag with a decimal between 0 and 1.
This value can have a significant impact on the analysis,
so explore how it impacts your data!

Many calculations are dependent on knowing where certain metadata is stored.
Namely, the experimental conditions (specified with ``--group``)
the compartment of origin (specified with ``--compartment``),
the sample ID (specified with ``--sample-id``),
and the lipidomics mode (specified with ``--mode``).
If these are not passed,
then they default to "Group", "Compartment", "SampleID", and "Mode" respectively.
To find these rows,
we also need to know the number of lines in your column metadata.
This is specified with ``--n-rows-metadata``.
Please the section on [expected data file structure](data) for more information.

The error-normalised fold change (ENFC) calculation must know the labels for
experimental and control group.
Without this knowledge,
the concept of fold change is meaningless.
To specify, pass ``--control control``.
Every condition specified in ``Group`` will then be divided by ``control``
to calculate the ENFC for all conditions.

```shell
lta data results --control lean
```

(configuration)=

#### Configuration files

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

The output folder will contain 2 files and 2 directories.
For each type of lipid, you should see the following:

1. `switch_individual_lipid.csv` - a table of lipids and their A/B/U/N classification.
1. `switch_lipid_classes.csv` - a table counting the frequency of each lipid class within the A/B/U/N classification.
1. `jaccard` - the Jaccard similarity and p-value for each lipid class.
1. `enfc` - a folder containing the ENFC results.

Within the ENFC folder,
you should see 2 files per group:

1. `GROUP_by_CONTROL_individual_lipids.csv` - the ENFC results for each lipid.
1. `GROUP_by_CONTROL_lipid_classes.csv` - the mean and St.Dev. of ENFC, grouped by lipid class.

Withing the Jaccard folder,
you should see 1 file per group:

1. `GROUP_by_CONTROL_jaccard_similarity.csv` - the Jaccard similarity and p-value
for each lipid class

A few notes!
Fold change will **always** be {math}`group / control`.
The Jaccard similarities are calculated between conditions specified in ``--group``
across both compartments and lipid classes.
The p-values for these similarities are calculated using the method outlined by
[N. Chung, et. al.][jaccard].
For ENFC,
fold change is only meaningful if both values are non-0.
Where this is *not* true,
NaN has been substituted,
leaving an empty cell in the output.

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

## Future Developments

- [x] Improve Github actions to use caching for poetry and Nox
- [x] Allow for multiple ENFC calculations in 1 run
- [x] Provide example configuration and data
- [ ] Increase test coverage
- [ ] Automate plotting

## Citations

If you use LTA in your work,
please cite the following manuscripts:

1. Furse, S., _et al._ Lipid Traffic Analysis reveals the impact of high paternal carbohydrate intake on offsprings’ lipid metabolism. _Commun Biol_ **4**, 163 (2021). [https://doi.org/10.1038/s42003-021-01686-1][paper_1]
1. Furse, S.[^eq], Fernandez-Twinn, D.S.[^eq], _et al._ Lipid metabolism is dysregulated before, during and after pregnancy in a mouse model of gestational diabetes. _Int. J. Mol. Sci._ **22**, 7452 (2021). [https://doi.org/10.3390/ijms22147452][paper_2]
1. Furse, S., _et al._ Paternal nutritional programming of lipid metabolism is propagated by sperm and seminal plasma. _Metabolomics_ **2022**, [https://doi.org/10.17863/CAM.79565][paper_3]
1. Furse, S., _et al._ A mouse model of gestational diabetes shows dysregulated lipid metabolism post-weaning, after return to euglycaemia.  _Nutrition & Diabetes_ **2022**, [_In Press_][paper_4]

[^eq]: These authors contributed equally to this work.

[github]: https://github.com/IMS-Bio2Core-Facility/lta "LTA Source Code"
[readthedocs]: http://lta.readthedocs.io/ "LTA Documentation"
[pypi]: https://pypi.org/project/gtexquery/ "LTA PyPI Package"
[realpython]: https://realpython.com/installing-python/ "RealPython Install Python"
[psf]: https://wiki.python.org/moin/BeginnersGuide/Download "PSF Install Python"
[pyenv]: https://github.com/pyenv/pyenv "PyEnv"
[pipx]: https://pypa.github.io/pipx/ "pipx"
[venv]: https://docs.python.org/3/tutorial/venv.html "Python venv"
[tags]: https://github.com/IMS-Bio2Core-Facility/lta/releases "LTA releases"
[issues]: https://github.com/IMS-Bio2Core-Facility/lta/issues "LTA issues"
[examples]: https://github.com/IMS-Bio2Core-Facility/lta/tree/main/examples "Examples"
[jaccard]: https://doi.org/10.1186/s12859-019-3118-5 "Jaccard Probabilities"
[lta_v1]: https://doi.org/10.5281/zenodo.4309347 " LTA, R version 1"
[paper_1]: https://www.nature.com/articles/s42003-021-01686-1 "LTA citation 1"
[paper_2]: https://www.mdpi.com/1422-0067/22/14/7452 "LTA citation 2"
[paper_3]: https://doi.org/10.17863/CAM.79565 "LTA citation 3"
[paper_4]: https://www.repository.cam.ac.uk/handle/1810/332691 "LTA citation 4"
