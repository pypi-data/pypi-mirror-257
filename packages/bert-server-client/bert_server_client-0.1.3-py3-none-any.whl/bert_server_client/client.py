import zmq

from typing import Optional
from bert_server_client.schema.embedding import Embedding, EmbeddingRequest, EmbeddingResponse


class BertClient:
    def __init__(self, host: str):
        """
        Initializes a new instance of the BertClient.

        Args:
            host (str): The address of the BERT server to connect to.
        """
        self.host = host
        self.context = None
        self.socket = None
        self.initialize_client()

    def __del__(self):
        """
        Destructor to ensure proper cleanup. It's called when the instance is being destroyed.
        """
        self.close()

    def initialize_client(self):
        """
        Sets up the ZMQ context and socket for communication with the BERT server.
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.host)

    def close(self):
        """
        Closes the ZMQ socket and terminates the context, releasing any system resources used.
        """
        if self.socket:
            self.socket.close()
        if self.context:
            self.context.term()

    def send_request(self, request: EmbeddingRequest) -> Optional[EmbeddingResponse]:
        """
        Sends an embedding request to the BERT server and waits for a response.

        Args:
            request (EmbeddingRequest): The request object containing the data for embedding.

        Returns:
            Optional[Embedding]: The embedding response from the BERT server.
            None if an exception occurs during the request.

        Raises:
            ValueError: If the provided request is not of type EmbeddingRequest.
            Exception: For any network-related errors or data packing/unpacking issues.
        """
        if not isinstance(request, EmbeddingRequest):
            raise ValueError("Invalid request type provided")

        try:
            if isinstance(request.input, str):
                request.input = [request.input]
            self.socket.send(request.msgpack_pack())
            response = self.socket.recv()
            return EmbeddingResponse.msgpack_unpack(response)
        except Exception as e:
            self.initialize_client()
            raise e
