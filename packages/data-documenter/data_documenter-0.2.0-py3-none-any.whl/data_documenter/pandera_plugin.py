from pandera import DataFrameSchema, Column
from mdutils import MdUtils
from .utils import (
    as_code,
    as_raw
)
from .metadocs import (
    MetaDocs
)

def get_title(x):
    return x.title if x.title else str(x.name)

def get_schema_properties(schema:DataFrameSchema):
    return {
        name: as_raw(getattr(schema, name)) 
        for name in ['name', 'unique', 'ordered']
        if getattr(schema, name) is not None
    }

def get_column_properties(column:Column):
    return {
        name: as_code(getattr(column, name))
        for name in ['name', 'dtype', 'nullable', 'unique', 'required']
        if getattr(column, name) is not None
    }

def get_column_metadata(column:Column):
    if column.metadata:
        return {
            name: as_raw(value) for name, value in column.metadata.items() if value
        }
    else:
        return {}

def get_description(x):
    if x.description:
        description = x.description
        description = as_raw(description)
        return description
    else:
        return ""

def column_to_markdown(
        column:Column
):
    md = MdUtils('tmp')
    md.new_line(f'???+ note \"{get_title(column)}\"')

    for line in get_description(column).splitlines():
        md.new_line(line)
    md.new_line()
    
    md.new_line('<h2>Properties<h2>')
    md.new_line()
    properties_table = ['Property', 'Value']
    for name, value in get_column_properties(column).items():
        properties_table.append(name)
        properties_table.append(str(value).replace('\n', '<br>'))
    md.new_table(2, len(properties_table) // 2, properties_table, text_align='left')
    
    if column.metadata:
        md.new_line('<h2>Metadata<h2>')
        md.new_line()
        properties_table = ['Property', 'Value']
        for name, value in get_column_metadata(column).items():
            properties_table.append(name)
            properties_table.append(str(value).replace('\n', '<br>'))
        md.new_table(2, len(properties_table) // 2, properties_table, text_align='left')

    # if column.checks:
    #     md.new_line('<h2>Checks<h2>')
    #     for check in column.checks:
    #         md.new_line(f'{check.__dict__}')

    return ('\n\t'.join(md.get_md_text().splitlines())).strip()

def pandera_to_markdown(
        schema:DataFrameSchema, 
        # file_name='test',
        title='',
        author=''
    ):
    md = MdUtils(file_name='', title=title, author=author)
    md.new_header(1, get_title(schema))
    for line in get_description(schema).splitlines():
        md.new_line(line)

    # Schema properties
    md.new_header(2, "Properties")
    properties_table = ['Property', 'Value']
    for name, value in get_schema_properties(schema).items():
        properties_table.append(name)
        properties_table.append(as_code(value))
    md.new_line()
    md.new_table(2, len(properties_table) // 2, properties_table, text_align='left')

    # Columns
    md.new_header(2, "Columns")
    for name, column in schema.columns.items():
        md.new_paragraph(column_to_markdown(column))

    return md.get_md_text()

def create_documentation(
        schema: DataFrameSchema, 
        docs_path: str, 
        title: str = '', 
        author:str = ''
        ):
    md = MetaDocs(docs_path)
    md.new()
    content = pandera_to_markdown(schema, title, author)
    md.save_markdown(content, 'index.md')
    return md
