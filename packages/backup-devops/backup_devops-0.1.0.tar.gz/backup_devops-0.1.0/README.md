# Azure devops backup
> A tool to make a backup of an azure devops organization

---

# Installation

```
poetry install
```

## Run the backup process

Configure the environment variables to specify the azure devops organization to backup:
- `AZDEVOPS_BACKUP_TARGET_ORGA`
- `AZDEVOPS_BACKUP_PAT_TARGET_ORGA`

Configure the environment variables for where to host the backup (a target azure devops organization):
- `AZDEVOPS_BACKUP_TARGET_ORGA`
- `AZDEVOPS_BACKUP_PAT_TARGET_ORGA`

```
poetry shell
```

## What is backed up

- source code following the original hierarchy (project, repository)
- work items and comments