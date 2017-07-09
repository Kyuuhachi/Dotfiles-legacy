scriptencoding utf-8
filetype off

let s:bund = '~/.config/nvim/bundle'
execute 'set rtp+='.s:bund.'/Vundle.vim'
call vundle#begin(s:bund)
Plugin 'VundleVim/Vundle.vim'
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
Plugin 'wellle/targets.vim'
Plugin 'xuhdev/vim-latex-live-preview'
Plugin 'vim-scripts/sudo.vim'
Plugin 'w0rp/ale'
Plugin 'junegunn/vim-easy-align'
Plugin 'vim-scripts/JavaScript-Indent'
Plugin 'mbbill/undotree'
Plugin 'Vimjas/vim-python-pep8-indent'
Plugin 'Shougo/deoplete.nvim'
Plugin 'Shougo/denite.nvim'
Plugin 'h1mesuke/unite-outline'
Plugin 'Shougo/deoplete-zsh'
Plugin 'Shougo/neco-vim'
Plugin 'Shougo/neco-syntax'
Plugin 'zchee/deoplete-jedi'
Plugin 'Caagr98/c98color.vim'
Plugin 'Caagr98/c98ibus.vim'
Plugin 'Caagr98/c98tabbar.vim'
Plugin 'Caagr98/c98lilypond.vim'
call vundle#end()

colorscheme c98color
let $NVIM_TUI_ENABLE_CURSOR_SHAPE=1
let $NVIM_TUI_ENABLE_TRUE_COLOR=1

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
set nojoinspaces

set shell=zsh

let g:polyglot_disabled = ['latex']

let g:splitjoin_split_mapping = ''
let g:splitjoin_join_mapping = ''
nmap <leader>j :SplitjoinJoin<cr>
nmap <leader>s :SplitjoinSplit<cr>

let g:airline_powerline_fonts = 1
let g:airline_inactive_collapse = 1
let g:airline#parts#ffenc#skip_expected_string = 'utf-8[unix]'
let g:airline#extensions#eclim#enabled = 1
let g:airline#extensions#whitespace#checks = ['mixed-indent-file', 'trailing']
let g:airline#extensions#whitespace#trailing_format = 'Trailing@%s'
let g:airline#extensions#whitespace#mixed_indent_file_format = 'Wrong indent@%s'

function! s:getSearchPos()
	let curpos = getcurpos()
	call setpos('.', [0, 0, 0, 0, 1])
	let searches = []
	while 1
		let [l, c] = searchpos(@/, 'W'.(len(searches) == 0 ? 'c' : ''))
		if l != 0
			let searches += [[l, c]]
		else
			break
		endif
	endwhile
	call setpos('.', curpos)
	let idx = index(searches, getcurpos()[1:2]) + 1
	return [idx, len(searches)]
endfunction

function! GetSearchPos()
	let [n, N] = s:getSearchPos()
	return n.'/'.N
endfunction

function! ShowSearchPos()
	let [n, N] = s:getSearchPos()
	return n != 0
endfunction

call airline#parts#define_function('searchpos', 'GetSearchPos')
call airline#parts#define_condition('searchpos', 'ShowSearchPos()')
let g:airline_section_x = airline#section#create_right(['searchpos', 'filetype'])

set showtabline=2

set completeopt=menu,menuone,preview,noselect
set splitbelow splitright
let g:deoplete#enable_at_startup = 1
inoremap <expr> <TAB> pumvisible() ? "<C-n>" : "<TAB>"
inoremap <expr> <Down> pumvisible() ? "<C-n>" : "<Down>"
inoremap <expr> <S-TAB> pumvisible() ? "<C-p>" : "<S-TAB>"
inoremap <expr> <Up> pumvisible() ? "<C-p>" : "<Up>"
inoremap <expr> <CR> pumvisible() ? "<C-y>" : "<CR>"
imap <NUL> <C-Space>
inoremap <expr> <C-Space> deoplete#mappings#manual_complete()
let g:deoplete#sources#jedi#show_docstring = 1
let g:deoplete#auto_complete_start_length = 1
let g:deoplete#ignore_sources = {'_': ['buffer', 'file', 'around']}

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
let g:ale_python_flake8_args = '--ignore=E101,E201,E202,E221,E222,E225,E226,E227,E228,E231,E241,E251,E261,E262,E265,E265,E271,E272,E301,E302,E303,E305,E306,E402,E501,E701,E702,E704,E722,E741,E742,E743,W191,W291,W292,W293,W503,F731'
" E101                Mixed space and tab
" E201 E202           Whitespace inside parens
" E221 E222           Multiple spaces around operator
" E225 E226 E227 E228 No spaces around operator
" E231                No space after [,;:]
" E241                Multiple spaces after [,]
" E251                Spaces around kwargs [=]
" E261                Require two spaces before comment
" E262 E265           Require space after [#]
" E265                Multiple [#]
" E271 E272           Multiple spaces around keyword
" E301 E302 E303 E305 E306 Blank line
" E402                Import not at top
" E501                Line length
" E701 E702 E704      Multiple statements on one line
" E722                No omni-except
" E741 E742 E743      No stuff named [lOI]
" W191                Indentation contains tab
" W291 W292 W293      Whitespace (Vim handles that just fine)
" W503                Line break before bin-op
" F731                Assign lambda to variable

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
