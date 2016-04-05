call pathogen#infect()
set background=dark
highlight Normal guibg=Black guifg=White
set guifont=Droid\ Sans\ Mono\ Dotted\ for\ Powerline\ 10
if has("gui_running")
	colorscheme solarized
else
	colorscheme noctu
endif

set mouse=
set nocompatible
syntax on
filetype indent plugin on
set encoding=utf-8
set cursorline
set autoindent
set showcmd
set incsearch hlsearch
set wildmenu wildmode=list:longest
set backspace=2
set cmdheight=2
set tabstop=4 shiftwidth=4
set ignorecase smartcase
set ffs=unix,dos,mac
set dir=~/.vim-tmp/
set list listchars=tab:>\ ,trail:+,precedes:<,extends:>
set number
set autochdir
set whichwrap+=h,l
set scrolloff=7
set nowrap

set shell=zsh

let g:airline_powerline_fonts = 1
let g:SuperTabDefaultCompletionType="<c-x><c-u>"
let g:SuperTabNoCompleteAfter=['^', '\t']
set completeopt+=longest

vnoremap . :norm.<CR>
nnoremap gV `[v`]
nnoremap <C-L> :nohl<CR><C-L>

autocmd FileType java setlocal formatexpr=eclim#java#src#Format(v:lnum,v:lnum+v:count-1)
