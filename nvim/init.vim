set nocompatible
filetype off
set rtp+=~/.config/nvim/bundle/Vundle.vim
call vundle#begin("~/.config/nvim/bundle")
Plugin 'altercation/vim-colors-solarized'
Plugin 'elzr/vim-json'
Plugin 'ervandew/supertab'
Plugin 'initrc/eclim-vundle'
Plugin 'kana/vim-textobj-entire'
Plugin 'kana/vim-textobj-fold'
Plugin 'kana/vim-textobj-lastpat'
Plugin 'kana/vim-textobj-syntax'
Plugin 'kana/vim-textobj-user'
Plugin 'Konfekt/FastFold'
Plugin 'mh21/errormarker.vim'
Plugin 'michaeljsmith/vim-indent-object'
Plugin 'noahfrederick/vim-noctu'
Plugin 'othree/html5.vim'
Plugin 'pbrisbin/vim-mkdir'
Plugin 'PotatoesMaster/i3-vim-syntax'
Plugin 'sheerun/vim-polyglot'
Plugin 'spiiph/vim-space'
Plugin 'tpope/vim-abolish'
Plugin 'tpope/vim-afterimage'
Plugin 'tpope/vim-characterize'
Plugin 'tpope/vim-commentary'
Plugin 'tpope/vim-eunuch'
Plugin 'tpope/vim-repeat'
Plugin 'tpope/vim-scriptease'
Plugin 'tpope/vim-speeddating'
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-vinegar'
Plugin 'vim-airline/vim-airline'
Plugin 'VundleVim/Vundle.vim'
Plugin 'wellle/targets.vim'
call vundle#end()

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
set list listchars=tab:⟩\ ,trail:+,precedes:<,extends:>
set number
set autochdir
set whichwrap+=h,l
set scrolloff=7
set nowrap
set foldmethod=marker


set shell=zsh

let g:airline_powerline_fonts = 1
let g:SuperTabNoCompleteAfter=['^', '\t']
set completeopt+=longest

let g:c_gnu = 1

vnoremap . :norm.<CR>
nnoremap gV `[v`]
nnoremap <C-L> :nohl<CR><C-L>
nnoremap q: :q<CR>

nmap gS :call <SID>SynStack()<CR>
function! <SID>SynStack()
  if !exists("*synstack")
    return
  endif
  echo map(synstack(line('.'), col('.')), 'synIDattr(v:val, "name")')
endfunc

autocmd FileType java setlocal formatexpr=eclim#java#src#Format(v:lnum,v:lnum+v:count-1)
autocmd FileType java let l:SuperTabDefaultCompletionType="<c-x><c-u>"
autocmd FileType python set expandtab< tabstop< softtabstop< shiftwidth<
