#!/usr/bin/env python3
"""
YouTube Transcript Server

A simple MCP server that listens on stdin for requests to fetch YouTube
video transcripts using the youtube_transcript_api library.
"""

import json
import sys
import logging
import os
from typing import Dict, Any

# Disable output buffering
os.environ['PYTHONUNBUFFERED'] = '1'

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logging.info(f"Python Path: {sys.path}")

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError as e:
    logging.error(f"Failed to import youtube_transcript_api: {str(e)}")
    logging.error("Please install using: uv pip install youtube-transcript-api")
    sys.exit(1)

class YouTubeTranscriptServer:
    """
    A simple MCP server that provides a tool to retrieve YouTube video
    transcripts via youtube_transcript_api. It listens for incoming JSON
    messages on stdin and writes responses to stdout.
    """

    def __init__(self) -> None:
        """
        Initialize the server and map MCP methods to their corresponding
        handler functions.
        """
        self.handlers = {
            'initialize': self.handle_initialize,
            'tools/list': self.handle_list_tools,
            'tools/call': self.handle_call_tool,
            'resources/list': self.handle_list_resources,
            'resources/templates/list': self.handle_list_resource_templates,
            'notifications/initialized': self.handle_notification,
            'cancelled': self.handle_cancelled
        }

    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the 'initialize' RPC method.

        :param params: JSON parameters from the client (which should include
                       'protocolVersion').
        :return: Server capabilities, protocol version, and server info.
        """
        client_protocol_version = params.get('protocolVersion', '0.1.0')
        
        # Example version check (commented out):
        # if client_protocol_version not in ["2024-11-05"]:
        #     raise ValueError(f"Unsupported protocol version: {client_protocol_version}")

        return {
            'protocolVersion': client_protocol_version,  # Echo the client's protocol version
            'serverInfo': {
                'name': 'youtube-transcript-server',
                'version': '0.1.0'
            },
            'capabilities': {
                'tools': {
                    'available': True
                },
                'resources': {
                    'available': False
                },
                'resourceTemplates': {
                    'available': False
                }
            }
        }

    def handle_notification(self, params: Dict[str, Any]) -> None:
        """
        Handle notification methods that do not require a response.

        :param params: JSON parameters from the client.
        :return: None
        """
        logging.debug(f"Received notification with params: {params}")
        return None

    def handle_cancelled(self, params: Dict[str, Any]) -> None:
        """
        Handle cancellation notifications.

        :param params: JSON parameters from the client.
        :return: None
        """
        logging.debug(f"Received cancellation with params: {params}")
        return None

    def handle_list_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the 'resources/list' RPC method.

        :param params: JSON parameters from the client.
        :return: An empty list of resources (as an example).
        """
        return {'resources': []}

    def handle_list_resource_templates(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the 'resources/templates/list' RPC method.

        :param params: JSON parameters from the client.
        :return: An empty list of resource templates (as an example).
        """
        return {'resourceTemplates': []}

    def handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the 'tools/list' RPC method.

        :param params: JSON parameters from the client.
        :return: A list of available tools (in this case, just 'get_transcript').
        """
        return {
            'tools': [
                {
                    'name': 'get_transcript',
                    'description': 'Get transcript for a YouTube video',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'video_id': {
                                'type': 'string',
                                'description': (
                                    'YouTube video ID (e.g., dQw4w9WgXcQ '
                                    'from youtube.com/watch?v=dQw4w9WgXcQ)'
                                )
                            },
                            'languages': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': (
                                    'List of language codes to try '
                                    '(e.g., ["en"]). Optional.'
                                )
                            }
                        },
                        'required': ['video_id']
                    }
                }
            ]
        }

    def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the 'tools/call' RPC method. Currently supports only the 
        'get_transcript' tool.

        :param params: JSON parameters from the client. Should contain 'name'
                       of the tool and 'arguments' for the tool.
        :return: The transcript data or an error if the tool or operation fails.
        """
        tool_name = params.get('name')
        if tool_name != 'get_transcript':
            logging.error(f"Unknown tool: {tool_name}")
            return {
                'error': {
                    'code': -32601,  # Method not found
                    'message': f'Unknown tool: {tool_name}'
                }
            }

        try:
            args = params.get('arguments', {})
            video_id = args['video_id']
            languages = args.get('languages')

            logging.info(f"Fetching transcript for video {video_id}")
            
            # Retrieve the transcript
            if languages:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            else:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)

            # Format transcript
            formatted_transcript = [entry['text'] for entry in transcript]
            result = '\n'.join(formatted_transcript)

            logging.info(f"Successfully formatted transcript, length: {len(result)}")
            return {
                'content': [
                    {
                        'type': 'text',
                        'text': result
                    }
                ]
            }

        except Exception as e:
            error_msg = f'Error getting transcript: {str(e)}'
            logging.error(error_msg, exc_info=True)
            return {
                'error': {
                    'code': -32000,  # Server error
                    'message': error_msg
                }
            }

    def handle_message(self, message: str) -> None:
        """
        Parse and handle a single MCP message.

        :param message: A JSON-encoded string representing the RPC request.
        :return: None
        """
        try:
            logging.debug(f"Received message: {message}")
            request = json.loads(message)
            method = request.get('method')
            logging.debug(f"Processing method: {method}")

            if method not in self.handlers:
                response = {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'error': {
                        'code': -32601,  # Method not found
                        'message': f'Unknown method: {method}'
                    }
                }
            else:
                result = self.handlers[method](request.get('params', {}))
                
                # For notifications or other handlers returning None, do not send a response
                if result is None:
                    return

                response = {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'result': result
                }

            logging.debug(f"Sending response: {response}")
            print(json.dumps(response), flush=True)

        except Exception as e:
            logging.error(f"Error handling message: {str(e)}", exc_info=True)
            error_response = {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'error': {
                    'code': -32603,  # Internal error
                    'message': str(e)
                }
            }
            print(json.dumps(error_response), flush=True)

    def run(self) -> None:
        """
        Start the server, reading lines from stdin and passing them to 
        handle_message.
        """
        # Ensure unbuffered I/O
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)

        logging.info("Starting YouTube Transcript Server")
        
        for line in sys.stdin:
            self.handle_message(line.strip())


def main() -> None:
    """
    Entry point for running the server.
    """
    server = YouTubeTranscriptServer()
    server.run()


if __name__ == '__main__':
    main()
