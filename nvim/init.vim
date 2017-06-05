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
Plugin 'tpope/vim-repeat'
Plugin 'tpope/vim-scriptease'
Plugin 'tpope/vim-speeddating'
Plugin 'tpope/vim-surround'
Plugin 'vim-airline/vim-airline'
Plugin 'Valloric/YouCompleteMe'
Plugin 'VundleVim/Vundle.vim'
Plugin 'wellle/targets.vim'
Plugin 'xuhdev/vim-latex-live-preview'
Plugin 'vim-scripts/sudo.vim'
Plugin 'w0rp/ale'
Plugin 'dansomething/vim-eclim'
Plugin 'junegunn/vim-easy-align'
Plugin 'Caagr98/c98color.vim'
Plugin 'Caagr98/vim-lilypond'
call vundle#end()

colorscheme c98color
let $NVIM_TUI_ENABLE_CURSOR_SHAPE=1

set mouse=
syntax on
filetype indent plugin on
" set encoding=utf-8
set cursorline
set autoindent
set showcmd noshowmode
set incsearch hlsearch inccommand=nosplit
set wildmenu wildmode=list:longest
set cmdheight=2
set tabstop=4 softtabstop=4 shiftwidth=4 noexpandtab
set ignorecase smartcase
set fileformats=unix,dos,mac
set list listchars=tab:⟩\ ,trail:+,precedes:<,extends:>,space:·
set number
set autochdir
set scrolloff=7
set nowrap
set foldmethod=marker
set directory=~/.vim-swap//
set backupdir=~/.vim-backup//
set undofile undodir=~/.vim-undo//
set updatetime=500
set notimeout

set shell=zsh

let g:polyglot_disabled = ['latex']
let g:airline_powerline_fonts = 1

set completeopt+=longest
set splitbelow splitright
" let g:ycm_python_binary_path = '/usr/bin/python3'
let g:ycm_server_python_interpreter = '/usr/bin/python3'

map <silent> <C-k> <Plug>(ale_previous_wrap)
map <silent> <C-j> <Plug>(ale_next_wrap)

let g:textobj_entire_no_default_key_mappings = 1
omap aE <Plug>(textobj-entire-a)
omap iE <Plug>(textobj-entire-i)

let g:autofenc_ext_prog_path='uchardet'
let g:autofenc_ext_prog_args=''
let g:autofenc_ext_prog_unknown_fenc='ascii/unknown'

vnoremap . :norm.<CR>
noremap ;v `<v`>
noremap ;V `<V`>
nnoremap <silent> <C-L> :nohl<CR><C-L>
noremap <leader>a <Plug>(EasyAlign)
noremap <leader>s :%s/\s*$//<CR>
nnoremap <leader>cc :call setreg(v:register, getreg(), "c")<CR>
nnoremap <leader>cl :call setreg(v:register, getreg(), "l")<CR>
nnoremap <leader>cb :call setreg(v:register, getreg(), "b")<CR>

noremap H ^
noremap L $
noremap j gj
noremap k gk
nnoremap r gr
nnoremap r<CR> r<CR>
nnoremap R gR

nnoremap gS :call <SID>SynStack()<CR>
function! <SID>SynStack()
	echo map(synstack(line('.'), col('.')), 'synIDattr(v:val, ''name'')')
endfunc

" map <ScrollWheelUp>     <C-Y>
" map <S-ScrollWheelUp>   <C-Y>
" map <ScrollWheelDown>   <C-E>
" map <S-ScrollWheelDown> <C-E>
" map!<ScrollWheelUp>     <C-O><C-Y>
" map!<S-ScrollWheelUp>   <C-O><C-Y>
" map!<ScrollWheelDown>   <C-O><C-E>
" map!<S-ScrollWheelDown> <C-O><C-E>
map <PageUp>    <C-U>
map <PageDown>  <C-D>
map!<PageUp>   <C-O><C-U>
map!<PageDown> <C-O><C-D>

let g:c_gnu = 1

let g:ale_scss_scss_lint_args = '--config ~/dot/nvim/scss-lint.yml'
let g:ale_python_python_exec = 'python3'
let g:ale_python_flake8_args = '--ignore=E128,E201,E202,E221,E241,E261,E301,E302,E305,E306,E501,E704,E741,E742,E743,W191,E701,E225,E226,E227,E228'
let g:ale_tex_chktex_options = '-n 32'
let g:ale_sign_column_always = 1
let g:ale_linters = {
\	'java': [],
\	'tex': ['chktex'],
\}

let g:python_highlight_builtins=1
let g:python_highlight_exceptions=1
augroup Python
	au!
	au FileType python setlocal expandtab< tabstop< softtabstop< shiftwidth<
augroup END

function! <SID>EclimRefactor()
	if !eclim#project#util#IsCurrentFileInProject()
		return
	endif

	if !eclim#java#util#IsValidIdentifier(expand('<cword>'))
		call eclim#util#EchoError("Element under the cursor is not a valid java identifier.")
		return
	endif

	let response = input("Rename? ")
	if response != ''
		let g:EclimRefactorPromptDefault = 2 " Preview
		call eclim#java#refactor#Rename(response)
	endif
endfunction
let g:EclimCompletionMethod = 'omnifunc'
let g:EclimMavenPomClasspathUpdate = 0
augroup Java
	au!
	au FileType java nmap <buffer> <Leader>o :JavaImportOrganize<CR>
	au FileType java nmap <buffer> <Leader>i :JavaImport<CR>
	au FileType java nmap <buffer> <Leader>c :JavaCorrect<CR>
	au FileType java nmap <buffer> <Leader>h :JavaHierarchy<CR>
	au FileType java nmap <buffer> <Leader>H :JavaCallHierarchy<CR>
	au FileType java nmap <buffer> <Leader>r :call <SID>EclimRefactor()<CR>
	au FileType java nmap <buffer> K :JavaSearchContext<CR>
augroup END
