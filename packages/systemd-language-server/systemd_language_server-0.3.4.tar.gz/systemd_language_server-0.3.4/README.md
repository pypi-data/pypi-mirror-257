# systemd-language-server

Language server for systemd unit files. Result of an exercise to learn the language server protocol.

## Supported Features

### `textDocument/completion`

Completion for

- unit file directives
- unit file sections
<!-- - values of some directives -->
![](assets/completion.gif)

### `textDocument/hover`

Documentation for directives supplied on hovering.

![](assets/hover.gif)

## Installation

```
pip install systemd-language-server
```

## Integrations

### coc.nvim

In `coc-settings.json`, under `.languageserver`:

```json
...
"systemd-language-server": {
  "command": "systemd-language-server",
  "filetypes": ["systemd"]
}
...
```
