#!/bin/sh
xdg-open smart-thesis/ba.pdf & alacritty -e sh -c "nvim smart-thesis/ba.tex" & cd smart-thesis
