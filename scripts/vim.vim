set nocompatible
syntax on
set t_Co=256
"set background=dark
let html_ignore_folding = 1
let html_use_css = 1
set ft=tex
set nu
colorscheme prmths
runtime! syntax/2html.vim
w! tmp/syntax-tex.html
q!
q!
