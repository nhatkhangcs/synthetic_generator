# DOCUMENT FOR DEVELOPERS

---

<!-- TOC -->
* [DOCUMENT FOR DEVELOPERS](#document-for-developers)
  * [Document](#document)
    * [`make` command](#make-command)
    * [Compiling `.tex` to `.pdf`](#compiling-tex-to-pdf)
    * [Cleaning all unnecessary files](#cleaning-all-unnecessary-files)
<!-- TOC -->
## Document

---

### `make` command

Run the following command script to see all `make` command.

```shell
make help
```

### Compiling `.tex` to `.pdf`

This command will compile `.tex` file. Make sure `pdflatex` already install on your machine.

```shell
make latex
```

### Cleaning all unnecessary files

This command will remove all unnecessary files generated while compiling `.tex`.

```shell
make clean
```
