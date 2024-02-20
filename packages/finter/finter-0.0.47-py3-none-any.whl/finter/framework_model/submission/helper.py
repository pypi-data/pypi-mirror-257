import os

import nbformat
from nbconvert import ScriptExporter
from finter.settings import logger

def extract_and_convert_notebook(
    cell_indices, notebook_name, model_name, model_type="alpha"
):
    """
    Extracts specific cells from a notebook and converts them into a Python script.

    Parameters:
    - cell_indices (list of int): Indices of the notebook cells to extract.
    - notebook_name (str): Name of the notebook file (without .ipynb extension).
    - model_name (str): Directory to save the converted Python script.

    Returns:
    - bool: True if the conversion was successful, False otherwise.
    """
    file_map = {"alpha": "am.py", "portfolio": "pf.py"}

    current_directory = os.getcwd()

    notebook_path = f"{notebook_name}.ipynb"
    output_path = os.path.join(model_name, file_map[model_type])

    # Ensure cell_indices is a list
    if isinstance(cell_indices, int):
        cell_indices = [cell_indices]

    # Log directory
    logger.info(f"Current directory: {current_directory}")
    logger.info(f"Notebook path: {notebook_path}")
    logger.info(f"Output path: {output_path}")

    # Ensure the output directory exists
    os.makedirs(model_name, exist_ok=True)

    # Load the notebook
    try:
        with open(notebook_path, "r", encoding="utf-8") as notebook_file:
            notebook = nbformat.read(notebook_file, as_version=4)
    except IOError:
        print(f"Error: Could not find {notebook_path}.")
        return False

    # Extract specified cells
    try:
        extracted_notebook = nbformat.v4.new_notebook()
        extracted_notebook.cells = [notebook.cells[i] for i in cell_indices]
    except IndexError as e:
        print(f"Error: Cell index out of range. {e}")
        return False

    # Convert the notebook to a Python script
    return convert_notebook_to_script(extracted_notebook, output_path)


def convert_notebook_to_script(notebook, output_path):
    """
    Converts a notebook object into a Python script and saves it to the specified path.

    Parameters:
    - notebook: Notebook object to convert.
    - output_path (str): Path to save the converted script.

    Returns:
    - bool: True if the conversion was successful, False otherwise.
    """
    exporter = ScriptExporter()

    try:
        body, resources = exporter.from_notebook_node(notebook)

        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(body)
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

    return True
