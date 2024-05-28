import os
from xml.etree.ElementTree import Element, tostring
from xml.dom.minidom import parseString
from app.agent import save_string_into_xml_file
from app import app


def test_save_string_into_xml_file():
    # Create a simple XML string
    root = Element('root')
    child = Element('child')
    root.append(child)
    xml_string = tostring(root, 'utf-8')

    # Define a procedure name
    procedure_name = 'test_procedure'

    # Call the function
    result = save_string_into_xml_file(xml_string, procedure_name)

    # Check if the file was created
    file_path = f'{app.config["OUTPUT_DIR"]}\\{procedure_name}.bpmn'
    print(f"File is being created at: {file_path}")
    assert os.path.exists(file_path), f"File {file_path} does not exist"

    # Check if the file content matches the result
    with open(file_path, 'r') as f:
        file_content = f.read()
    assert file_content == result, "File content does not match the result"

    print("Test passed")


# Run the test
test_save_string_into_xml_file()
