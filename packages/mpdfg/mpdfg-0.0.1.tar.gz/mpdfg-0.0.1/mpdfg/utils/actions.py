import tempfile
import shutil
from graphviz import Source
from mpdfg.utils.constants import MERMAID_UPPER_HTML, MERMAID_LOWER_HTML


def save_graphviz_diagram(dfg_string: str, file_path: str, format: str):
    tmp_file = tempfile.NamedTemporaryFile(suffix=".gv")
    tmp_file.close()
    src = Source(dfg_string, tmp_file.name, format=format)

    render = src.render(cleanup=True)
    shutil.copyfile(render, f"{file_path}.{format}")


def save_mermaid_diagram(dfg_string: str, file_path: str):
    diagram_string = MERMAID_UPPER_HTML + dfg_string + MERMAID_LOWER_HTML
    with open(f"{file_path}.html", "w") as f:
        f.write(diagram_string)
