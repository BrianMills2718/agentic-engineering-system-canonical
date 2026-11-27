## Why

A configured Company Planning validator on a clean Linux account could fetch its code and read the package, but could not find the typed graph schema. Its default assumes a Representation Router checkout under the account's code2 folder. Brian requested a documented clean setup on 2026-11-27.

Plan size: small

## What changes

Give both validator callers a way to pass the upstream schema option. Use Git's existing sparse checkout for installation from a source the operator can read. The validator keeps its existing default when the option is absent.
