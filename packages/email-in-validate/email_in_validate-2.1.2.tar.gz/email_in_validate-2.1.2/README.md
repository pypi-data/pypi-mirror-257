# Email Input Validator 

This is a command-line interface (CLI) tool that validates email addresses. It checks if an email address matches the regular expression for a valid email address and then prints a message indicating whether the email address is valid or not.

## Installation

You can install this tool from PyPI:

```shell
pip install email_in_validate
```

## Usage

### CLI Usage

You can use this tool in your terminal like this:

```shell
email_in_validate validate test@example.com
```

Replace `test@example.com` with the email address you want to validate.

### Usage in Login Applications

You can also use this tool in your login applications to validate user email addresses during authentication. Here's a basic example of how you can do this in a Python-based web application:

```python
from email_in_validate import validate

def login(email, password):
    if not validate(email):
        return 'Invalid email address'
    # Continue with your authentication logic...
```



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```