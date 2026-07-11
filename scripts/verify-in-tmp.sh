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

mkdir -p "$tmp/grader" "$tmp/solutions/assignments"
cp -r "$PRIVATE/grader/$SLUG"    "$tmp/grader/"
cp -r "$PRIVATE/solutions/assignments/$SLUG" "$tmp/solutions/assignments/"

"$APROG" verify "$SLUG" --private "$tmp" --public "$PUBLIC"
