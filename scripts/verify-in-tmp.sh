#!/usr/bin/env bash
# Run aprog verify for a single slug against a temporary private repo copy so
# that compiled binaries and other pipeline artifacts never touch the real repo.
#
# Usage: verify-in-tmp.sh <slug> <abs-private> <abs-public> <aprog-bin>
set -e

SLUG=$1
PRIVATE=$2
PUBLIC=$3
APROG=$4

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/grader" "$tmp/solutions"
cp -r "$PRIVATE/grader/$SLUG"    "$tmp/grader/"
cp -r "$PRIVATE/solutions/$SLUG" "$tmp/solutions/"
if [ -d "$PRIVATE/hidden-tests/$SLUG" ]; then
    mkdir -p "$tmp/hidden-tests"
    cp -r "$PRIVATE/hidden-tests/$SLUG" "$tmp/hidden-tests/"
fi

"$APROG" verify "$SLUG" --private "$tmp" --public "$PUBLIC"
