# `file-to-unicode-base64-data-uri`

A simple, efficient utility for converting files to Unicode base64-encoded data URIs.

## Features

- 📄 Auto-detects the MIME type.
- ♻️ Streaming/generator interface so your program never loads the file fully into memory except for the output string.
- ✅ Python 2 and 3 compatible.

## Install

```bash
pip install file-to-unicode-base64-data-uri
```

## Usage

```python
from __future__ import print_function
from codecs import open
from file_to_unicode_base64_data_uri import file_to_unicode_base64_data_uri 

# Get a single string (data URI)
data_url = file_to_unicode_base64_data_uri('example.png')
print(data_url[:80] + u'...')

# Stream out in chunks (memory efficient for huge files)
from file_to_unicode_base64_data_uri import file_to_unicode_base64_data_uri_fragments_generator

with open('output.txt', 'w', 'utf-8') as out:
    for fragment in file_to_unicode_base64_data_uri_fragments_generator('large_video.mp4'):
        out.write(fragment)
```

## Why?

Many libraries read the entire file into memory before encoding or require third-party dependencies. This utility is pure Python, efficient, and works everywhere, even for large files.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).