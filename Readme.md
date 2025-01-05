# YouTube Transcript MCP Server

A Model Context Protocol (MCP) server that provides YouTube video transcript retrieval capabilities using the `youtube_transcript_api` library.

## Features

- Fetch transcripts from any YouTube video using its video ID
- Support for multiple language transcripts
- MCP-compliant server implementation
- Error handling and logging
- Configurable through environment variables

## Prerequisites

- Python 3.x
- UV package manager

## Installation

1. Clone the repository:
```bash
git clone git@github.com:shahshrey/youtube_transcript_mcp.git
cd youtube_transcript_server
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
uv pip install -r requirements.txt
```

## API

### Resources

- None currently implemented

### Tools

- **get_transcript**
  - Retrieves the transcript of a YouTube video
  - Input:
    - `video_id` (string, required): YouTube video ID
    - `languages` (string[], optional): Preferred language codes
  - Returns:
    - Text content of the transcript with timestamps removed
    - Error details if the operation fails

**Example Request:**
```json
{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "get_transcript",
        "arguments": {
            "video_id": "dQw4w9WgXcQ",
            "languages": ["en"]
        }
    },
    "id": 1
}
```

**Example Response:**
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "content": [
            {
                "type": "text",
                "text": "First line of transcript\nSecond line of transcript\n..."
            }
        ]
    }
}
```

## Server Capabilities

- Protocol Version: Compatible with client's protocol version
- Tools Available: Yes
- Resources Available: No
- Resource Templates Available: No

## Error Handling

The server implements robust error handling for:
- Invalid video IDs
- Unavailable transcripts
- Language availability
- Network issues
- Invalid requests

**Example Error Response:**
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32000,
        "message": "Error getting transcript: Video id dQw4w9WgXcQ does not exist"
    }
}
```

## Development

The server is built with a focus on:
- Clean separation of concerns
- Comprehensive logging
- Type hints for better code maintainability
- Error handling with informative messages

## Configuration

### Environment Variables

- `PYTHONUNBUFFERED`: Set to '1' to disable output buffering
- `LOGGING_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "youtube_transcript": {
      "command": "path_to_your_python_executable or python",
      "args": [
        "path_to_ /youtube_transcript_server.py"
      ]
    }
  }
}
```

## Testing

Run the test suite using:
```bash
python -m pytest test_transcript.py
```

## Build

To build and package the server:

```bash
python -m build
```

## License

MIT License

Copyright (c) 2023 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the existing coding style.
