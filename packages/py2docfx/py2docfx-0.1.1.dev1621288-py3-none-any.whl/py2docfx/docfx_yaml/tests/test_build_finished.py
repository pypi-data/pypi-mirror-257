import pytest

from translator import translator
from build_finished import build_finished

from .utils.test_utils import prepare_app_envs,load_rst_transform_to_doctree

@pytest.mark.sphinx('yaml', testroot='build-finished')
def test_build_finished(app):
    # Test data definition
    objectToGenXml = 'code_with_signature_and_docstring.TestClass'
    objectToGenXmlType = 'class'

    # Arrange
    prepare_app_envs(app, objectToGenXml)
    doctree = load_rst_transform_to_doctree(app, objectToGenXmlType, objectToGenXml)
    
    # Act
    translator(app, '', doctree)
    build_finished(app, None)

    # Assert
    target_node = app.env.docfx_yaml_classes[objectToGenXml][1]['syntax']
    parameter_node = target_node['parameters'][0]
    keyword_only_arg_node = target_node['keywordOnlyArguments'][0]
    positional_only_arg_node = target_node['positionalOnlyArguments'][0]

    assert (parameter_node['id'] == 'parameter')
    assert (parameter_node['type'] == ['<xref:str>'])
    assert (keyword_only_arg_node['id'] == 'keyword_only_arg')
    assert (keyword_only_arg_node['type'] == ['<xref:bool>'])
    assert (positional_only_arg_node['id'] == 'positional_only_arg')
    assert (positional_only_arg_node['isRequired'] == True)
