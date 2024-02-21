from dataclasses import asdict

import msgpack
import pytest
from unittest.mock import patch
from bert_server_client.client import BertClient
from bert_server_client.schema.embedding import (
    EmbeddingRequest,
    Embedding,
    EmbeddingResponse,
    EmbeddingUsage)


@pytest.fixture
def mock_zmq_context():
    with patch('zmq.Context') as mock:
        yield mock


@pytest.fixture
def bert_client(mock_zmq_context):
    return BertClient('tcp://localhost:5555')


def test_initialization(bert_client, mock_zmq_context):
    assert mock_zmq_context.called
    assert bert_client.host == 'tcp://localhost:5555'


def test_destructor(bert_client, mock_zmq_context):
    bert_client.__del__()
    assert mock_zmq_context.return_value.term.called
    assert mock_zmq_context.return_value.socket.return_value.close.called


def test_send_request_valid(bert_client, mock_zmq_context):
    mock_socket = mock_zmq_context.return_value.socket.return_value

    embedding_data = [Embedding(object='embedding', index=0, embedding=[0.1, 0.2, 0.3])]
    embedding_usage = EmbeddingUsage(prompt_tokens=5, total_tokens=10)
    embedding = EmbeddingResponse(object='response', data=embedding_data, model='test-model', usage=embedding_usage)

    valid_msgpack_encoded_embedding = msgpack.packb(asdict(embedding))

    mock_socket.recv.return_value = valid_msgpack_encoded_embedding

    request = EmbeddingRequest(input='test', model='test-model')
    response = bert_client.send_request(request)

    assert isinstance(response, EmbeddingResponse)


def test_send_request_invalid_request(bert_client):
    with pytest.raises(ValueError):
        bert_client.send_request('invalid_request')


def test_send_request_exception_handling(bert_client, mock_zmq_context):
    mock_socket = mock_zmq_context.return_value.socket.return_value
    mock_socket.send.side_effect = Exception("Network error")
    request = EmbeddingRequest(input='test', model="test-model")
    with pytest.raises(Exception) as exc_info:
        bert_client.send_request(request)
    assert 'Network error' in str(exc_info.value)
