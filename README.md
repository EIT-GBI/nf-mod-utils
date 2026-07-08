# nf-mod-utils


Nextflow module for utils. Used as a git submodule by pipelines.

Image: `ghcr.io/eit-gbi/nf-mod-utils:latest`

## Processes

- `UTILS` — TODO: describe inputs/outputs

## Use as submodule
```bash
git submodule add https://github.com/eit-gbi/nf-mod-utils.git modules/utils
```

Then in your pipeline:
```
include { UTILS } from './modules/utils/main.nf'
```
