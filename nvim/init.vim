scriptencoding utf-8
filetype off

let g:python_host_prog='/usr/bin/false'
let g:python3_host_prog='/usr/bin/python'

call plug#begin('~/.cache/nvim')
Plug 'kana/vim-textobj-user'
Plug 'lervag/vimtex'
Plug 'PotatoesMaster/i3-vim-syntax'

Plug 'sheerun/vim-polyglot'
" Plug 'itchyny/vim-haskell-indent', {'for':['haskell']}
Plug 'neovimhaskell/haskell-vim'
Plug 'Shougo/vimproc.vim', {'do' : 'make'}
Plug 'tpope/vim-abolish'
Plug 'tpope/vim-afterimage'
Plug 'tpope/vim-characterize'
Plug 'tpope/vim-commentary'
Plug 'tpope/vim-repeat'
Plug 'tpope/vim-surround'
Plug 'vim-airline/vim-airline'
Plug 'wellle/targets.vim'
" Plug 'vim-scripts/sudo.vim'
Plug 'dense-analysis/ale'
Plug 'junegunn/vim-easy-align'
Plug 'vim-scripts/JavaScript-Indent', {'for':['javascript', 'jsx']}
Plug 'mbbill/undotree'
" Plug 'Shougo/denite.nvim'
" Plug 'h1mesuke/unite-outline'
" Plug 'vito-c/jq.vim'
" Plug 'andymass/vim-matchup'
" Plug 'vim-scripts/css3-mod'

Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'Shougo/deoplete-zsh', {'for':['zsh']}
Plug 'Shougo/neco-vim', {'for':['vim']}
Plug 'Shougo/neco-syntax'
Plug 'zchee/deoplete-jedi', {'for':['python']}
Plug 'numirias/semshi', {'do': ':UpdateRemotePlugins'}

Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'

" Plug 'nvim-treesitter/nvim-treesitter'

call plug#end()

for path in glob(expand('<sfile>:p:h') . '/c98*', 1, 1)
	let &rtp =  path . ',' . &rtp
endfor

colorscheme c98color
let $NVIM_TUI_ENABLE_CURSOR_SHAPE=1
let $NVIM_TUI_ENABLE_TRUE_COLOR=1

set lazyredraw
set mouse=
syntax on
filetype indent plugin on
set cursorline
set autoindent cinoptions+=L0
set showcmd noshowmode
set incsearch hlsearch inccommand=nosplit
set wildmode=longest:list
set wildignore+=*.midi,*.pdf,*.mp3 "Lilypond
set wildignore+=*.class "Java
set wildignore+=*.o,*.hi "Haskell (also c/++)
set wildignore+=*.png,*.jpg,*.gif
set cmdheight=2

set ignorecase smartcase
set fileformats=unix,dos,mac
set list listchars=tab:⟩\ ,trail:+,precedes:<,extends:>,space:·,nbsp:░
set number
set shortmess=asWAIc
set formatoptions=crqlmM1j
set scrolloff=7 sidescrolloff=30
set nowrap linebreak
set foldmethod=marker "foldcolumn=1
set directory=/tmp/.vim-swap//
set backupdir=~/.vim-backup//
set undofile undodir=~/.vim-undo//
set updatetime=500
set notimeout
set nojoinspaces
set hidden
set signcolumn=yes
set virtualedit=block
set showtabline=2
set splitbelow splitright
set fileencodings=utf8,cp932,latin1

set shell=zsh

set paragraphs= sections=

set gdefault

set tabstop=4 softtabstop=0 shiftwidth=4 noexpandtab
autocmd FileType * setlocal formatoptions-=cro

let g:airline_powerline_fonts = 1
let g:airline_inactive_collapse = 1
let g:airline#parts#ffenc#skip_expected_string = 'utf-8[unix]'
let g:airline#extensions#whitespace#checks = []

hi LongLine ctermbg=darkgray
augroup LongLine
	au!
	au BufWinEnter * call matchadd('LongLine', '\%81v.', -1)
augroup END
augroup CursorLineOnlyInActiveWindow
	au!
	au VimEnter,WinEnter,BufWinEnter * setlocal cursorline
	au WinLeave * setlocal nocursorline
augroup END
set textwidth=80

let g:polyglot_disabled = ['lilypond']
" if !exists('g:deoplete#omni#input_patterns') | let g:deoplete#omni#input_patterns = {} | endif

command! W :write

let g:vimade = {}
let g:vimade.fadelevel = 0.7
let g:vimade.enablesigns = 1

" let g:airline_powerline_fonts = 1
" let g:airline_inactive_collapse = 1
" let g:airline#parts#ffenc#skip_expected_string = 'utf-8[unix]'
" let g:airline#extensions#whitespace#checks = ['trailing']
" let g:airline#extensions#whitespace#trailing_format = 'Trailing@%s'

set completeopt=menu,menuone,preview,noselect,noinsert
let g:deoplete#enable_at_startup = 1
map <NUL> <C-Space>
map! <NUL> <C-Space>
inoremap <c-c> <ESC>
" inoremap <expr> <C-Space> deoplete#mappings#manual_complete()
" let g:deoplete#auto_complete_start_length = 1
let g:deoplete#on_insert_enter = v:false
inoremap <expr> <CR> (pumvisible() && v:completed_item == {} ? '<C-e><CR>' : '<CR>')
inoremap <expr> <Up> (pumvisible() ? '<C-e><Up>' : '<Up>')
inoremap <expr> <Down> (pumvisible() ? '<C-e><Down>' : '<Down>')
inoremap <expr> <PageUp> (pumvisible() ? '<C-e><PageUp>' : '<PageUp>')
inoremap <expr> <PageDown> (pumvisible() ? '<C-e><PageDown>' : '<PageDown>')

map <expr> H ['^', 'g^'][&wrap]
map <expr> L ['$', 'g$'][&wrap]
map K kJ
" This above mapping does not work with counts
map gK kgJ
nnoremap <silent> <C-L> :nohl<CR><C-L>
nnoremap <expr> n 'Nn'[v:searchforward]
nnoremap <expr> N 'nN'[v:searchforward]
nnoremap <c-w><c-w> <NUL>

nnoremap ,cc :call setreg(v:register, getreg(), 'c')<CR>
nnoremap ,cl :call setreg(v:register, getreg(), 'l')<CR>
nnoremap ,cb :call setreg(v:register, getreg(), 'b')<CR>

nnoremap ,b :Buffers<CR>
nnoremap ,f :Files<CR>
nnoremap ,g :GFiles<CR>

nnoremap ,, <C-^>

nnoremap gs :call <SID>SynStack()<CR>
function! <SID>SynStack()
	echo map(synstack(line('.'), col('.')), 'synIDattr(v:val, ''name'')')
endfunc

nnoremap <silent>  * :let @/='\C\<' . expand('<cword>') . '\>'<CR>:let v:searchforward=1<CR>n
nnoremap <silent>  # :let @/='\C\<' . expand('<cword>') . '\>'<CR>:let v:searchforward=0<CR>n
nnoremap <silent> g* :let @/='\C'   . expand('<cword>')       <CR>:let v:searchforward=1<CR>n
nnoremap <silent> g# :let @/='\C'   . expand('<cword>')       <CR>:let v:searchforward=0<CR>n

noremap ] :call search('\n\zs\n\n\|\%$', 'Ws')<CR>
noremap [ :call search('\n\n\zs\n\|\%^', 'bWs')<CR>


autocmd User targets#mappings#user call targets#mappings#extend(
\	{ 'a': {'argument':
\		[ {'o': '[', 'c': ']', 's': '[,;]'}
\		, {'o': '{', 'c': '}', 's': '[,;]'}
\		, {'o': '(', 'c': ')', 's': '[,;]'}
\	]} })

map <silent> <C-k> <Plug>(ale_previous_wrap)
map <silent> <C-j> <Plug>(ale_next_wrap)
let g:ale_completion_enabled = 1
let g:ale_fixers = {'*': ['remove_trailing_lines', 'trim_whitespace']}
let g:ale_linters = {}
let g:ale_sign_column_always = 1
let g:ale_echo_msg_error_str = 'E'
let g:ale_echo_msg_warning_str = 'W'
let g:ale_echo_msg_format = '[%linter%:%severity%] %s'
let g:ale_lint_on_text_changed = 'normal'
let g:ale_lint_on_insert_leave = 1

let g:ale_linters.tex = []
let g:ale_tex_chktex_options = '-n 38' " 38: punc inside quote
call add(g:polyglot_disabled, 'latex')
let g:vimtex_imaps_enabled = 0
" let g:deoplete#omni#input_patterns.tex = g:vimtex#re#deoplete
let g:tex_flavor = "latex"
let g:vimtex_indent_on_ampersands = 0
let g:tex_no_error = 1
let g:tex_stylish = 1
let g:livepreview_engine = 'lualatex'


let java_ignore_javadoc = 1
let g:c_gnu = 1
au FileType cpp syn clear cppSTLfunction cppSTLfunctional cppSTLconstant cppSTLnamespace cppSTLtype cppSTLexception cppSTLiterator cppSTLiterator_tag cppSTLenum cppSTLios cppSTLcast cCustomFunc
au FileType c syn clear cCustomFunc

call add(g:polyglot_disabled, 'lua')

call add(g:polyglot_disabled, 'python')
call add(g:polyglot_disabled, 'python-indent')
let g:python_highlight_space_errors = 0
let g:semshi#error_sign = v:false
let g:ale_python_python_exec = 'python3'
let g:ale_python_flake8_options = '--select=E112,E113,E251,E303,E304,E401,E502,E703,E711,E712,E713,E714,E901,E902,E999,W391,W6,F --extend-ignore=F402'
let g:ale_python_flake8_change_directory = 0
function! s:InitSemshi()
	nmap <buffer> <silent> ,r :Semshi rename<CR>

	nmap <buffer> <silent> <Tab> :Semshi goto name next<CR>
	nmap <buffer> <silent> <S-Tab> :Semshi goto name prev<CR>
endf
au FileType python call s:InitSemshi()
let g:semshi#mark_selected_nodes = 2
let g:semshi#excluded_hl_groups = []

let g:ale_linters.haskell = ['hie', 'hlint']
let g:necoghc_enable_detailed_browse=1
let g:haskell_classic_highlighting=1
let g:haskell_enable_arrowsyntax=1
let g:haskell_enable_pattern_synonyms=1
let g:haskell_enable_quantification=1
let g:haskell_enable_recursivedo=1
let g:haskell_enable_static_pointers=1
let g:haskell_enable_typeroles=1
au FileType haskell syn match haskellFloat "\v<[0-9]+(\.[0-9]\+)?([eE][-+]?[0-9]+)?>"

fun! s:fixVimscript()
	syn clear vimCommentString
	syn clear vimCommentTitle
	syn match vimHighlight "\<hi\%[ghlight]\(\s\+def\%[ault]\>\)\?" skipwhite nextgroup=@vimHighlightCluster

	let l:colors = [
		\ ['black'], ['darkred'], ['darkgreen'], ['brown', 'darkyellow'], ['darkblue'], ['darkmagenta'], ['darkcyan'], ['lightgray', 'lightgrey', 'gray', 'grey'],
		\ ['darkgray', 'darkgrey'], ['red', 'lightred'], ['green', 'lightgreen'], ['yellow', 'lightyellow'], ['blue', 'lightblue'], ['magenta', 'lightmagenta'], ['cyan', 'lightcyan'], ['white'] ]

	syn clear vimHiCtermColor
	syn match vimHiCtermColor contained "\<color\d\{1,3}\>"
	for l:num in range(256)
		let l:bg = index([0,16,17,22,52]+range(232,236), l:num) != -1 ? '008' : '000'
		exec 'hi def vimHiCol_'.l:num.' ctermbg='.l:num.' ctermfg='.l:bg

		exec 'syn match vimHiCol_'.l:num.' /\c\<0*'.l:num.'\>/ containedin=vimHiNmbr contained'
		exec 'syn match vimHiCol_'.l:num.' /\c\<color'.l:num.'\>/ containedin=vimHiCtermColor contained'
		if l:num < 16
			for l:col in l:colors[l:num]
				exec 'syn match vimHiCtermColor contained /\c\<'.l:col.'\>/'
				exec 'syn match vimHiCol_'.l:num.' /\c\<'.l:col.'\>/ containedin=vimHiCtermColor contained'
			endfor
		endif
	endfor
endf
autocmd FileType vim call s:fixVimscript()
autocmd ColorScheme * call s:fixVimscript()

fun! s:HighlightSpace()
	syn match Whitespace /　/ containedin=ALL conceal cchar=・
endf
au FileType *    call s:HighlightSpace()
au ColorScheme * call s:HighlightSpace()

au FileType *        setlocal et< ts<  sts<  sw<
au FileType haskell  setlocal et  ts=2 sw=2
au FileType lilypond setlocal et  ts=2 sw=2
au FileType yaml     setlocal et  ts=2 sw=2

au FileType js       setlocal ft=javascript
