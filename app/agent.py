import os
from app import app
import logging
import nest_asyncio

from xml.etree.ElementTree import tostring
from xml.dom.minidom import parseString

from llama_index.core import Settings
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool

from app.index import init_openai, get_index

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nest_asyncio.apply()


def save_string_into_xml_file(xml_string, procedure_name):
    # Pretty print XML
    parsed_xml = parseString(xml_string)
    pretty_xml_str = parsed_xml.toprettyxml(indent="  ")

    # Save XML to file
    file_path = f'{app.config["OUTPUT_DIR"]}\\{procedure_name}.bpmn'

    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

    with open(file_path, 'w') as f:
        f.write(pretty_xml_str)

    return pretty_xml_str


def get_agent():
    from llama_index.core.tools import QueryEngineTool
    init_openai()
    index = get_index()
    procedure_tool = QueryEngineTool.from_defaults(
        query_engine=index.as_query_engine(),
        name="procedure_tool",
        description=(
            f"Provide information about 'Préparer les plats' procedure of my restaurant"
            f"Provide about BPMN 2.0 specification of the Object Management Group (OMG)"
        ),
    )

    llm = Settings.llm
    save_string_into_xml_file_tool = FunctionTool.from_defaults(fn=save_string_into_xml_file)
    agent = OpenAIAgent.from_tools(tools=[save_string_into_xml_file_tool, procedure_tool], llm=llm, verbose=True)
    return agent
