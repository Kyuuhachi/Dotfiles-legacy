scriptencoding utf-8
filetype off

let g:python3_host_prog = '/usr/bin/python3'

let s:dir = expand('<sfile>:p:h:h') . '/pkgs/nvim'

function DoPlug()
	call plug#begin('~/.cache/nvim')
	Plug 'kana/vim-textobj-user'
	Plug 'lervag/vimtex'
	Plug 'PotatoesMaster/i3-vim-syntax'

	Plug 'sheerun/vim-polyglot'
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
	Plug 'dense-analysis/ale'
	Plug 'junegunn/vim-easy-align'
	Plug 'mbbill/undotree'

	Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
	Plug 'Shougo/deoplete-zsh'
	Plug 'Shougo/neco-vim'
	Plug 'Shougo/neco-syntax'
	Plug 'zchee/deoplete-jedi'
	Plug 'numirias/semshi', {'do': ':UpdateRemotePlugins'}

	Plug 'junegunn/fzf'
	Plug 'junegunn/fzf.vim'

	for path in glob(s:dir . '/98*', 1, 1)
		Plug path
	endfor

	call plug#end()

endfunction

exec 'source ' . s:dir . '/init.vim'

delf DoPlug
