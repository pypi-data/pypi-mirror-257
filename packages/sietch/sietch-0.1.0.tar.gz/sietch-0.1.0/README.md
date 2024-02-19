# sietch
Sietch is a lightweight environment CLI tool.
It creates and manages local environments for simple projects.
It is designed to be used for small hobby projects that may share some basic environment requirements.

## Installation
```bash
pip install sietch
```

## Usage

### Create a new environment
```bash
sietch create --name MyEnv
```

### Activate an environment
Activation is not fully implemented, the command here prints the activation command.
```bash
sietch activate --name MyEnv
```

### Remove an environment
```bash
sietch remove --name MyEnv
```

### List all environments
```bash
sietch list
```