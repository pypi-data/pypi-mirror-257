# Python connector plugin common code: v0.1.0

## Rebuild proto files

Clone NEOS-Critical/neos-int-connector-lib, and hashicorp/go-plugin to your
code directory (assumed parent of this directory)


Build the connector proto files.
```bash
inv build-proto-lib
```

Build the hashicorp go plugin files.
```bash
inv build-proto-plugin
```

Edit these files to all import `from proto import xxxx` as above command
imports `manager_pb2` etc directly despite being put in a proto module.

TODO: build these in a communal location so imports etc can be done right.

## Prerequisites

The following packages are used across python repositories. A global install of them all is *highly* recommended.

* [Poetry](https://python-poetry.org/docs/#installation)
* [Invoke](https://www.pyinvoke.org/installing.html)

## Code Quality

### Tests

```bash
invoke tests
invoke tests-coverage
```

### Linting

```bash
invoke check-format
invoke check-style
```

Alternatively run the following to automatically fix linting issues that ruff can.
```bash
ruff . --fix
```

## Releases

Release management is handled using `bump2version`. The below commands will
start a new release cycle.

```bash
$ invoke bump-patch
$ invoke bump-minor
$ invoke bump-major
> vX.Y.Z.rc0
```

Release candidates can be tested, and new builds can be triggered
using `bump-build`.

```bash
$ invoke bump-build
> vX.Y.Z.rc0 -> vX.Y.Z.rc1
```

Once a release candidate is stable, `bump-release` will move it from `rc` to
official.

```bash
$ invoke bump-release
vX.Y.Z.rc1 -> vX.Y.Z
```
