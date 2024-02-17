# myrepos-utils

## Usage

### config
Configures a new repository, checks it out by default, and configures
additional git remotes and git configurations as specified

For example:
```
$ mr-utils config centos/hyperscale/emacs "git clone -b c9s-sig-hyperscale https://git.centos.org/rpms/emacs.git" --extra-git-remotes fedora https://src.fedoraproject.org/rpms/emacs.git --git-configs user.email salimma@centosproject.org

```

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

### version
Displays the version of the current `myrepos-utils`
