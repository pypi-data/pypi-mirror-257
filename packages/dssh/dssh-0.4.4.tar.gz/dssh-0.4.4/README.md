# Connect Dev SSH

Simple and elegant python module that helps you to manage your ssh server based on environment. Like DEV, UAT, PRE-PROD etc.
You can customize your environments/servers config as per your requirements.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```
pip install dssh
```

## Usage

### Add new environment

```
$ dssh addenv
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
└────────────────────────┘
New Environment name: DEV
```

### Add new server to an environment

```
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

```
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

### Modify config of a server

```
$ dssh modserver
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
│ DEV                    │
└────────────────────────┘
Select an environment: DEV
┏━━━━━━━━━━━━━━━━━━━┓
┃ Availbale Servers ┃
┡━━━━━━━━━━━━━━━━━━━┩
│ Server1           │
└───────────────────┘
Select a server: Server1
Current Username - user Hostname - host
New Username(Press enter if no change): nuser
New Hostname(Press enter if no change): nhost
Success! 💥
```

### Remove a server

```
$ dssh dlserver
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
│ DEV                    │
└────────────────────────┘
Select an environment: DEV
┏━━━━━━━━━━━━━━━━━━━┓
┃ Availbale Servers ┃
┡━━━━━━━━━━━━━━━━━━━┩
│ Server1           │
└───────────────────┘
Select a server: Server1
Success! 💥
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
