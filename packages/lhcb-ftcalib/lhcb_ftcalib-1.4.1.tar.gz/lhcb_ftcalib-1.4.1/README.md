# lhcb_ftcalib
[![pipeline status](https://gitlab.cern.ch/lhcb-ft/lhcb_ftcalib/badges/master/pipeline.svg)](https://gitlab.cern.ch/lhcb-ft/lhcb_ftcalib/-/commits/master)
### LHCb Flavour Tagging calibration software

At high-energy proton-proton collider experiments, the production flavour of neutral B mesons needs to be reconstructed from particle charges
from hadronisation processes in the associated event, i.e. from additional hadronisations on the signal meson side, as well as
hadronisation and decays of the partner B hadron. This is commonly done with ML techniques like (recurrent) neural networks or boosted decision trees.
The mistag probability estimates of these models (probability that predicted production flavour is wrong) usually need to have the property of probabilities.
This calibration tool optimizes a GLM function to predict the mistag probabilities and takes into account the fact that neutral mesons can undergo
oscillation before they decay. In addition, it provides helper functions to measure the performance and correlations of these models.

**Documentation:** [Read the Docs](https://lhcb-ftcalib.readthedocs.io/en/latest/)

## Installation
```
pip install lhcb_ftcalib
```

## Command Line Interface Examples
Run `ftcalib --help` for a list of all options or [read the docs](https://lhcb-ftcalib.readthedocs.io/en/latest/)

**1. Calibrating opposite side taggers in a sample and saving result**
```
ftcalib file:tree -OS VtxCh Charm OSElectronLatest OSMuonLatest OSKaonLatest \
        -mode Bd -tau B_tau -id B_ID -op calibrate -out output
```
**2. Calibrating both tagging sides, combining them inidividually, and calibrating+saving the results**
```
ftcalib file:tree -OS VtxCh Charm OSElectronLatest OSMuonLatest OSKaonLatest \
        -SS SSPion SSProton \
        -mode Bd -tau B_tau -id B_ID -op calibrate combine calibrate -out output
```
**Note:** The command line interface is by design not feature complete. Use the API to fine tune the calibration settings.

## Requirements
* uproot >= 4
* iminuit >= 2.3.0
* pandas < 1.5
* numpy <= 1.21
* scipy
* matplotlib
* numba == 0.53.1

### For developers
#### Testing multiple python versions via tox
<details>
<summary>Click to expand</summary>

To test lhcb_ftcalib in different python environments, interpreters for each
version need to be installed. Multiple python versions can be installed with `pyenv`:
```bash
CC=clang pyenv install 3.6.15
pyenv install 3.7.13
pyenv install 3.8.13
pyenv install 3.9.13
pyenv install 3.10.5
pyenv install 3.11.8
pyenv install 3.12.2
```
Whereby only missing versions need to be installed! Note that python 3.6 has
issues with pip throwing segfaults if not built with clang. To make the newly
installed versions globally available run
```bash
pyenv global 3.6.15 3.7.13 3.8.13 3.9.13 3.10.5 3.11.8 3.12.2
```
and add `$HOME/.pyenv/shims` to your `PATH`.
To run the basic tests, execute
```bash
tox
```
in the lhcb_ftcalib directory
</details>

