# CSV image filename demo

This exercise uses pandas to generate an image filename from each product title.
Install pandas in your Python environment, then run from the repository root:

```sh
python demos/pandas-csv-newline/pandass.py
```

The script always reads the `products.csv` next to it and regenerates
`products_with_images.csv` in the same folder, regardless of your working directory.

Run the regression test against temporary files:

```sh
python -m unittest discover -s demos/pandas-csv-newline/tests -v
```
