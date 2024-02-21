# Some useful powheg scripts

## Install

To install the scripts, simply run the following command:

```bash
$ pip install powheg-tools
```

## cleanpowheg

This script is used to clean the powheg output files. It is useful to clean the output files before running the next iteration of the powheg process. The script is used as follows:

```bash
$ cleanpowheg [-p here/or/there]
```

## genpwgseeds

Generates a list of random seeds for the powheg process. The script is used as follows:

```bash
$ genpwgseeds [-n 10] [...]
```

Generates equidistante seed numbers, such that individual bad seeds can easily be increased without producing conflicting seeds or too long seeds

## geninitrwgt

Generates the initrwgt block for specific pdf and scale variations. The script is used as follows:

```bash
$ geninitrwgt cteq66
```
