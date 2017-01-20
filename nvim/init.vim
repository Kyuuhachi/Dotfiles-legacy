scriptencoding utf-8
filetype off
let s:bund = '~/.config/nvim/bundle'
execute 'set rtp+='.s:bund.'/Vundle.vim'
call vundle#begin(s:bund)
Plugin 'eagletmt/ghcmod-vim'
Plugin 'eagletmt/neco-ghc'
Plugin 'kana/vim-textobj-entire'
Plugin 'kana/vim-textobj-fold'
Plugin 'kana/vim-textobj-lastpat'
Plugin 'kana/vim-textobj-syntax'
Plugin 'kana/vim-textobj-user'
Plugin 'Konfekt/FastFold'
Plugin 'Konfekt/FoldText'
Plugin 'lervag/vimtex'
Plugin 'mh21/errormarker.vim'
Plugin 'michaeljsmith/vim-indent-object'
Plugin 'noahfrederick/vim-noctu'
Plugin 'parsonsmatt/vim2hs'
Plugin 'pbrisbin/vim-mkdir'
Plugin 'PotatoesMaster/i3-vim-syntax'
Plugin 's3rvac/AutoFenc'
Plugin 'sheerun/vim-polyglot'
Plugin 'Shougo/vimproc.vim'
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
Plugin 'vim-airline/vim-airline'
Plugin 'Valloric/YouCompleteMe'
Plugin 'VundleVim/Vundle.vim'
Plugin 'wellle/targets.vim'
Plugin 'xuhdev/vim-latex-live-preview'
Plugin 'vim-scripts/Improved-AnsiEsc'
Plugin 'w0rp/ale'
Plugin 'Caagr98/c98color.vim'
call vundle#end()

colorscheme c98color
" let $NVIM_TUI_ENABLE_CURSOR_SHAPE=1

set mouse=
syntax on
filetype indent plugin on
" set encoding=utf-8
set cursorline
set autoindent
set showcmd noshowmode
set incsearch hlsearch
set wildmenu wildmode=list:longest
set backspace=2
set cmdheight=2
set tabstop=4 shiftwidth=4
set ignorecase smartcase
set fileformats=unix,dos,mac
set list listchars=tab:⟩\ ,trail:+,precedes:<,extends:>
set number
set autochdir
set whichwrap+=h,l
set scrolloff=7
set nowrap
set foldmethod=marker
set directory=~/.vim-swap//
set backupdir=~/.vim-backup//
set undofile undodir=~/.vim-undo//

set shell=zsh

let g:polyglot_disabled = ['latex']

let g:airline_powerline_fonts = 1

set completeopt+=longest
set splitbelow splitright
let g:ycm_python_binary_path = 'python3'

map <silent> <C-k> <Plug>(ale_previous_wrap)
map <silent> <C-j> <Plug>(ale_next_wrap)
let g:ale_sign_column_always = 1

let g:textobj_entire_no_default_key_mappings = 1
omap aE <Plug>(textobj-entire-a)
omap iE <Plug>(textobj-entire-i)

let g:autofenc_ext_prog_path='uchardet'
let g:autofenc_ext_prog_args=''
let g:autofenc_ext_prog_unknown_fenc='ascii/unknown'

vnoremap . :norm.<CR>
nnoremap gV `[v`]
map H ^
map L $

nnoremap <silent> <C-L> :nohl<CR>:call <SID>NoHL()<CR><C-L>
function! <SID>NoHL()
	if exists(':GhcModTypeClear')
		GhcModTypeClear
	endif
endfunc

let g:c_gnu = 1

let g:ale_python_python_exec='python3'
let g:ale_python_flake8_args='--ignore=E128,E221,E241,E261,E301,E302,E305,E306,E501,E704,E741,E742,E743,W191'
augroup Python
	au!
	au FileType python setlocal expandtab< tabstop< softtabstop< shiftwidth<
augroup END

let g:ale_scss_scss_lint_args='--config ~/dot/nvim/scss-lint.yml'

let g:haskell_conceal = 0
let g:haskell_conceal_wide = 1 - g:haskell_conceal
let g:haskell_fold = 0
augroup Haskell
	au!
	au FileType haskell setlocal expandtab tabstop=8 softtabstop=8 shiftwidth=2
	au FileType haskell setlocal omnifunc=necoghc#omnifunc
	au FileType haskell noremap <buffer> <F1> :GhcModType<CR>
	au FileType haskell noremap <buffer> <silent> <F2> :call <SID>HS_Pointfree()<CR>
	au FileType haskell noremap <buffer> <silent> <F3> :call <SID>HS_Pointful()<CR>
	au FileType haskell noremap <buffer> <F4> :GhcModTypeInsert<CR>
augroup END

function! <SID>HS_Pointfree()
	call setline('.', split(system('pointfree '.getline('.')), '\n'))
endfunction
function! <SID>HS_Pointful()
	call setline('.', split(system('pointful '.getline('.')), '\n'))
endfunction

nnoremap gS :call <SID>SynStack()<CR>
function! <SID>SynStack()
	echo map(synstack(line('.'), col('.')), 'synIDattr(v:val, ''name'')')
endfunc
