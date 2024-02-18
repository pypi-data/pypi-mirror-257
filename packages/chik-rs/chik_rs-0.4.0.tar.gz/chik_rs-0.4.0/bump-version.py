#!/usr/bin/env python3

# usage:
# bump-version <new-version-string> <previous-release-tag>

import os
import re
import sys
from typing import Callable, Set

v = sys.argv[1]
tag = sys.argv[2]

our_crates = [
    "chik-bls",
    "klvm-traits",
    "chik-traits",
    "chik_py_streamable_macro",
    "chik_streamable_macro",
    "chik-protocol",
    "chik-tools",
    "klvm-utils",
    "klvm-derive",
    "chik-wallet",
    "chik-client",
    "chik-ssl",
    "fuzz",
    "chik-wallet/fuzz",
    "klvm-utils/fuzz",
]

def crates_with_changes() -> Set[str]:
    ret = set()
    for c in our_crates:
        diff = os.popen(f"git diff {tag} -- {c}").read().strip()
        if len(diff) > 0:
            ret.add(c)
    # the python wheel is the top-level build target, we always want to bump its
    # version
    ret.add("wheel")
    return ret

def update_cargo(name: str, crates: Set[str]) -> None:
    subst = ""
    with open(f"{name}/Cargo.toml") as f:
        for line in f:
            split = line.split()
            if split == []:
                subst += line
                continue

            if split[0] == "version" and name in crates:
                line = f'version = "{v}"\n'
            elif split[0] in crates:
                line = re.sub('version = "(>?=?)\d+\.\d+\.\d+"', f'version = "\\g<1>{v}"', line)
            subst += line

    with open(f"{name}/Cargo.toml", "w") as f:
        f.write(subst)


crates = crates_with_changes()
# always update the root crate (chik)
crates.add(".")
crates.add("chik")

print("bumping version of crates:")
for c in crates:
    print(f" - {c}")

for c in our_crates:
    update_cargo(c, crates)

update_cargo(".", crates)
update_cargo("wheel", crates)
