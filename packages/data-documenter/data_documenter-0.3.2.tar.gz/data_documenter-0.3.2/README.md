# Data Documenter

A package to generate documentation from [pandera](https://pandera.readthedocs.io/en/stable/) schema using [mkdocs material](https://squidfunk.github.io/mkdocs-material/).

## Installation

```sh
pip install data-documenter
```

## Quick start

1. Create schema using `pandera`
```py
from pandera import DataFrameSchema, Column

schema = DataFrameSchema(
    title="Title of dataset",
    description="Description of dataset",
    columns={
        "COLUMN_NAME": Column(
            dtype="str",
            nullable=False,
            unique=True,
            description="Description of column",
            title="Column Name"
        ),
    },
)
```
2. Create documentation using schema
```py
from data_documenter.pandera_plugin import create_documentation

docs = create_documentation(
    schema, 
    docs_path = 'docs_folder', 
    title = 'page title',
    filename = 'index.md'
)
```

3. Run server
```py
docs.run()
```

4. Stop server
```py
docs.stop()
```

It is better to use `mkdocs` command instead of `run`, `stop` for better control of processes. See alternative usage.
```sh
cd path/to/folder
mkdocs serve
```

5. Build and deploy documentation  
See `mkdocs` [documentation](https://squidfunk.github.io/mkdocs-material/getting-started/).

## Alternative usage

1. Create new folder for documentation server.
```py
from data_documenter.metadocs import MetaDocs

docs = MetaDocs(docs_path = 'my_docs')
docs.new()
```
This will simply run `mkdocs new my_docs` and replace `mkdocs.yml` file.

2. Save documentation for schema in a markdown file.
```py
text_markdown = pandera_to_markdown(schema)
docs.save_markdown(text_markdown, filename = 'index.md')
```

3. See documentation.
```
cd my_docs
mkdocs serve
```

4. Build and deploy  
See `mkdocs` [documentation](https://squidfunk.github.io/mkdocs-material/getting-started/).
