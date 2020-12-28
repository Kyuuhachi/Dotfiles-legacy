scriptencoding utf-8
filetype off

let s:dir = expand('<sfile>:p:h:h') . '/pkgs/nvim'

function DoPlug()
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

	for path in glob(s:dir . '/98*', 1, 1)
		let &rtp =  path . ',' . &rtp
	endfor
endfunction

exec 'source ' . s:dir . '/init.vim'

delf DoPlug
