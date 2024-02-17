# myrepos-utils

## Usage

### find
Let's say you have the following repositories configured in `~/.mrconfig`:

```
[src/github/owner1/projA]
...

[src/github/owner2/projB]
...
```

This will let you quickly switch to `~/src/github/owner1/projA`:
```
cd (mr-utils find github projA)
```

If there are multiple matches, they will be printed out.

### sort
This will sort `~/.mrconfig` based on sections and write it back out
```
mr-utils sort
```
