# vqf_model

MiniZinc model for the VQF project.

## Developer notes

* Some comments and variable names are in spanish because the model was designed that way. Do not change them.
* MiniZinc does not convert bool to int directly. Because we need to sum booleans, we represent them as integers 1 (true) or 0 (false). You will find the note "bool as int" in the comments.

## Docs and resources

* Find the model in the file [Formula Orquestadorv2_junio_2022.docx](./docs/Formula%20Orquestadorv2_junio_2022.docx)
* And read the [MiniZinc Handbook](https://www.minizinc.org/doc-2.6.4/en/index.html)
