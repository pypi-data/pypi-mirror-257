# filesignature

Tool that allows to search, extract, compare the signature of the files (`magic numbers`) and return the obtained information.

The purpose of this project is to check that a file is valid, i.e. the extension and the hexadecimal signature correspond.


>
> The "byte offset" refers to the position of a specific byte within a file or in a sequence of bytes.
> 11 byte offsets -> indicates that the first 11 bytes must be shifted to get the desired byte mark.
>

# Install package

```bash
pip install filesignature
```


# Usage

```python
>>> from filesignature import FileSignature
>>>
>>> f = FileSignature()
>>>
>>> bytes_data = b'\xef\xbb\xbfhello'
>>> print(f.check_bytes_type(raw_data=bytes_data, extention='txt'))
('EF BB BF', '0', 'txt')
>>>
>>> print(f.check_file_type('file.pdf'))
{'filename': 'file', 'file_extention': 'pdf', 'mimetype': 'application/pdf', 'file_signature': True}
>>>
>>> print(f.check_file_type('file.pdf', get_bool=True))
True
```
