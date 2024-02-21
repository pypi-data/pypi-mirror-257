# Connect Dev SSH

This is simple and elegant python module that helps you to manage your ssh server based on environment. Like DEV, UAT, PRE-PROD etc.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install connect-dev-ssh
```

## Usage
### Add new environment

```bash
$ dssh addenv                       
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
└────────────────────────┘
New Environment name: DEV
```

### Add new server to an environment
```bash
$ dssh addserver
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
│ DEV                    │
└────────────────────────┘
Select an environment: DEV
┏━━━━━━━━━━━━━━━━━━━┓
┃ Available Servers ┃
┡━━━━━━━━━━━━━━━━━━━┩
└───────────────────┘
New Server name: Server1
Server username: username
Server hostname: 10.10.0.1
```

### Connect to a server
```bash
$ dssh connect
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
│ DEV                    │
│ UAT                    │
└────────────────────────┘
Select an environment: DEV
┏━━━━━━━━━━━━━━━━━━━┓
┃ Availbale Servers ┃
┡━━━━━━━━━━━━━━━━━━━┩
│ Server1           │
└───────────────────┘
Select a server: Server1
Environment:DEV Server:Server1!
Connecting to username@10.10.0.1! 💥
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
