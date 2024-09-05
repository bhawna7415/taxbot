import pytest
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import DATABASE_HOST,DATABASE_NAME,DATABASE_PASSWORD,DATABASE_PORT,COLLECTION_NAME,DATABASE_USER

# Replace 'your_module' with the actual name of the module where ChatBot is defined
from vectorstore.chatbot import ChatBot
@pytest.fixture
def mock_connection():
    db_user =  DATABASE_USER
    db_password = DATABASE_PASSWORD
    db_host = DATABASE_HOST
    db_port = DATABASE_PORT
    db_name = DATABASE_NAME
    return Mock(db_name=db_name, db_host=db_host, db_password=db_password,
                db_port=db_port, db_user=db_user)

@pytest.mark.unit
def test_chatbot_initialization(mock_connection):
    chatbot = ChatBot(mock_connection)
    assert chatbot.vector_store is not None
    assert chatbot.storage_context is not None
    assert chatbot.index is not None

@patch('llama_index.SimpleDirectoryReader.load_data')
@patch('llama_index.ingestion.IngestionPipeline.run')
@pytest.mark.unit
def test_insert_vector_data(mock_run, mock_load_data, mock_connection):
    mock_load_data.return_value = ["mock_document1", "mock_document2"]
    mock_run.return_value = ["mock_node1", "mock_node2"]
    chatbot = ChatBot(mock_connection)
    result = chatbot.insert_vector_data()
    assert result is True
    mock_load_data.assert_called_once()
    mock_run.assert_called_once_with(documents=["mock_document1", "mock_document2"])


@patch('llama_index.retrievers.VectorIndexRetriever')
@patch('llama_index.get_response_synthesizer')
@patch('llama_index.query_engine.RetrieverQueryEngine')
@pytest.mark.unit
def test_chat_response(mock_query_engine, mock_response_synthesizer, mock_retriever, mock_connection):
    mock_retriever_instance = mock_retriever.return_value
    mock_query_engine_instance = mock_query_engine.return_value
    mock_response_synthesizer_instance = mock_response_synthesizer.return_value
    mock_retriever_instance.query.return_value = "mock_response"
    mock_response_synthesizer_instance.query.return_value = "mock_final_response"
    chatbot = ChatBot(mock_connection)
    result = chatbot.chat_response("sample_query")
    assert result