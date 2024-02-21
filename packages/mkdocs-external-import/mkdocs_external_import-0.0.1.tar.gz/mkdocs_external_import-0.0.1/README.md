# MKDocs External Import

Import external markdown files into your documentation site.

## Usage

Install `mkdocs-external-import`:

- `pip install mkdocs-external-import`
- `poetry add mkdocs-external-import`

Add to `mkdocs.yml`:

```yaml
plugins:
  - external-import
```

Reference an external Markdown file in a codeblock:

````markdown
```import-external-content
https://raw.githubusercontent.com/acodeninja/mkdocs-external-import/main/README.md
```
````

Build your docs, or run a local development server:

- `mkdocs build`
- `mkdocs serve`

The logs will show the following output:

```console
INFO    -  mkdocs_external_import: Importing external content from: https://raw.githubusercontent.com/acodeninja/mkdocs-external-import/main/README.md
```
