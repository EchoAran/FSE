# PDF Split and Merge

A local CLI tool for splitting, extracting, merging, and interleaving PDF files.

## Run

```bash
python -m pdfsplitmerge --help
```

## Examples

Split a file into one page per file:

```bash
python -m pdfsplitmerge split input.pdf --output outdir
```

Merge files:

```bash
python -m pdfsplitmerge merge --inputs a.pdf b.pdf --output merged.pdf
```
