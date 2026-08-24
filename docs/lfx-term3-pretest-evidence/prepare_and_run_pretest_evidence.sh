#!/bin/sh
set -eu

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "usage: $0 /path/to/ianvs [python-command]" >&2
    exit 2
fi

repo=$1
python_command=${2:-python3}
review_root=$(mktemp -d /tmp/ianvs-pretest.XXXXXX)

add_pr_worktree() {
    number=$1
    expected_sha=$2
    destination=$3
    git -C "$repo" fetch origin "pull/$number/head"
    actual_sha=$(git -C "$repo" rev-parse FETCH_HEAD)
    if [ "$actual_sha" != "$expected_sha" ]; then
        echo "PR #$number moved: expected $expected_sha, got $actual_sha" >&2
        exit 1
    fi
    git -C "$repo" worktree add --detach "$review_root/$destination" "$actual_sha"
}

add_base_worktree() {
    sha=$1
    destination=$2
    git -C "$repo" cat-file -e "$sha^{commit}"
    git -C "$repo" worktree add --detach "$review_root/$destination" "$sha"
}

add_pr_worktree 566 176fad4cc863f8df28e6a880488d2da757661b43 pr566
add_pr_worktree 705 b07ca3872a3fb26b238f5e40d903f4ae2a8155a7 pr705
add_pr_worktree 736 67b59e2b38ebaf10d70d40a40d8071f5bde694d4 pr736
add_pr_worktree 649 c24707654c5f765affceaf78936f9432465d6ad0 pr649
add_pr_worktree 770 13d0ebeb53b505eacc069800a9d0c2a9d6ca9b5a pr770
add_pr_worktree 721 5b3b9978c5fe37324eb0e03b132ed5a79560e949 pr721

add_base_worktree bf0f59680cea87bd5ff32283183a61ec4cf34d00 pr566-base
add_base_worktree 36ec0087c0919989ca305eb593c739bb1e97509d pr736-base

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
IANVS_PRETEST_REVIEW_ROOT="$review_root" \
    "$python_command" "$script_dir/pretest_contract_reproductions.py"

for destination in pr566 pr705 pr736 pr649 pr770 pr721; do
    git -C "$review_root/$destination" diff --check
done

echo "review worktrees retained at: $review_root"
