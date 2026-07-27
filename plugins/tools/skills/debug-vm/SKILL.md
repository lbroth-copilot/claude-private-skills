---
name: debug-vm
description: Find and connect to IONOS Cloud debugging VMs provisioned with the debug-vm tool. Use when the user wants to deploy to, test on, SSH into, or check status of their debug VMs. Triggers on references to "debug VM", "my VM", "test server", "deploy to VM", or when needing a remote Linux machine for testing.
version: 1.0.0
author: Lukas Benjamin Roth <lukasbenjamin.roth@strato.de>
license: proprietary
---

# debug-vm

IONOS Cloud debugging VM provisioner. VMs are created via interactive TUI (`debug-vm`), but read-only queries work non-interactively.

## CLI read-only flags

```bash
debug-vm --list              # JSON array of all created servers
debug-vm --ip                # IP of most recently created server
debug-vm --ip vm-luroth      # IP of a specific server by name
debug-vm --ssh               # SSH into most recent server (exec)
debug-vm --ssh vm-luroth     # SSH into specific server
```

## Direct config access

Config file: `~/.config/debug-vm/config.json` (respects `$XDG_CONFIG_HOME`).

Server entries in `.created_servers[]`:
```json
{
  "server_id": "uuid",
  "name": "vm-username",
  "datacenter_id": "uuid",
  "ip_address": "1.2.3.4",
  "created_by": "username",
  "created_date": "2025-01-15T10:30:00Z"
}
```

## Connecting to VMs

All VMs accept SSH as root:
```bash
ssh root@$(debug-vm --ip)
```

To run commands remotely:
```bash
ssh root@$(debug-vm --ip) 'docker ps'
```

To copy files:
```bash
scp -r ./dist root@$(debug-vm --ip):/opt/app/
```

## Installed tools on VMs

VMs are provisioned with: Docker, kubectl, k9s, helm, terraform, ionosctl, aws-cli, trivy, cosign, clamav, Go, oras, git, jq, python3, wireshark-cli, screen.
