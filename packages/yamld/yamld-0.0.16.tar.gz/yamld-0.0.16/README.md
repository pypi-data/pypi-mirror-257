# YAML-D

**YAMLd** is a tiny subset of *YAML* designed specifically for representing tabular data (*CSV* or *spreadsheets*). It is particularly useful for datasets with numerous features or lengthy sequences that are hard to read. The D stands for data!

 It is mainly used for reading *Pandas* dataframes, but it comes with extra command line tools.

**Note:** It is still experimental, use it with caution.
## Convert CSV to YAMLd and vice versa:
```console
csv2yamld <your-csv-file>
```

```console
yamld2csv <your-yamld-file>
```

For more details use `csv2yamld -h` or `yamld2csv -h`.

## Open CSV files with VIM/NVIM
Reading *CSV* can be annoying, here is a simple solution:

```console
csv2yamld <your-csv-file> --stdout | nvim -c 'set filetype=yaml' -
```

Of course, you can edit it, save it, and convert it back to *CSV* using `yamld2csv`.


## Setup
```console 
pip install -U yamld
```

To install without virtual environments, you can use [*pipx*](https://github.com/pypa/pipx). Another option is to pass `--break-system-packages` to *pip*, but it's not advisable.
