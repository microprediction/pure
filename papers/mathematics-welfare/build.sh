#!/bin/sh
# Build the PDF. Run from this directory.
set -e
pdflatex -interaction=nonstopmode mathematics-welfare.tex >/dev/null
pdflatex -interaction=nonstopmode mathematics-welfare.tex | grep -E "^!|Output written"
cp mathematics-welfare.pdf ../../docs/mathematics-welfare.pdf
