# Compspec IOR

<p align="center">
  <img height="300" src="https://raw.githubusercontent.com/compspec/spec/main/img/compspec-circle.png">
</p>

A compspec (Composition spec) is a specification and model for comparing things. Compspec IOR is
a plugin for extraction of [IOR](https://github.com/hpc/ior) metadata from applications, and packaging in compatibility specification
artifacts. This means that we also maintain the compatibility schema here. To learn more:

 - [Compspec](https://github.com/compspec/compspec): the Python library that discovers and loads this plugin.
 - [Compatibility](https://github.com/compspec/spec/tree/main/compatibility): of container images and applications to a host environment.
 - [Compspec Go](https://github.com/compspec/compspec-go): the Go library that retrieves artifacts and makes graphs for image selection and scheduling.


## Usage

Install compspec and the plugin here:

```bash
pip install compspec
pip install compspec-ior
```

Then run an extraction with IOR. You can use defaults, or add any parameters to IOR after the plugin name "ior"

```bash
compspec extract ior ...
```

More coming soon!

## TODO

- Developer environment with IOR installed (for others and me too)
- testing, etc with pre-commit and spell checking
- implement run functionality
 - use reasonable defaults for when nothing provided
 - outputs should map to new schema.json attributes
 - main library compspec should have support for oras push, etc.

## License

HPCIC DevTools is distributed under the terms of the MIT license.
All new contributions must be made under this license.

See [LICENSE](https://github.com/converged-computing/cloud-select/blob/main/LICENSE),
[COPYRIGHT](https://github.com/converged-computing/cloud-select/blob/main/COPYRIGHT), and
[NOTICE](https://github.com/converged-computing/cloud-select/blob/main/NOTICE) for details.

SPDX-License-Identifier: (MIT)

LLNL-CODE- 842614
