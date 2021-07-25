set background=dark
highlight clear
let g:colors_name="98"

let save_cpo = &cpo
set cpo&vim
augroup C98Color
	au!
augroup END

" Text {{{1
hi Normal                ctermfg=NONE ctermbg=NONE cterm=NONE

hi Folded                ctermfg=003  ctermbg=000  cterm=NONE
hi Conceal               ctermfg=NONE ctermbg=000  cterm=NONE

hi Directory             ctermfg=014  ctermbg=NONE cterm=NONE
hi NonText               ctermfg=011  ctermbg=NONE cterm=NONE
hi SpecialKey            ctermfg=008  ctermbg=NONE cterm=BOLD
hi Whitespace            ctermfg=008  ctermbg=NONE cterm=NONE

hi SpellBad              ctermfg=NONE ctermbg=001  cterm=NONE
hi SpellCap              ctermfg=NONE ctermbg=004  cterm=NONE
hi SpellLocal            ctermfg=NONE ctermbg=014  cterm=NONE
hi SpellRare             ctermfg=NONE ctermbg=005  cterm=NONE

hi DiffAdd               ctermfg=NONE ctermbg=022  cterm=NONE
hi DiffText              ctermfg=NONE ctermbg=005  cterm=NONE
hi DiffDelete            ctermfg=NONE ctermbg=052  cterm=NONE
hi DiffChange            ctermfg=NONE ctermbg=NONE cterm=NONE
hi link diffRemoved DiffDelete
hi link diffAdded   DiffAdd

" Borders / separators / menus {{{1
hi FoldColumn            ctermfg=007  ctermbg=000  cterm=NONE
hi SignColumn            ctermfg=007  ctermbg=000  cterm=NONE
hi LineNr                ctermfg=008  ctermbg=000  cterm=NONE
hi CursorLineNr          ctermfg=011  ctermbg=000  cterm=BOLD
hi VertSplit             ctermfg=000  ctermbg=000  cterm=NONE
hi ColorColumn           ctermfg=NONE ctermbg=000  cterm=NONE

hi Pmenu                 ctermfg=015  ctermbg=008  cterm=NONE
hi PmenuSel              ctermfg=014  ctermbg=008  cterm=BOLD
hi PmenuSbar             ctermfg=000  ctermbg=000  cterm=NONE
hi PmenuThumb            ctermfg=007  ctermbg=007  cterm=NONE

hi StatusLine            ctermfg=000  ctermbg=015  cterm=BOLD
hi StatusLineNC          ctermfg=008  ctermbg=015  cterm=NONE
hi WildMenu              ctermfg=NONE ctermbg=004  cterm=BOLD

hi TabLine               ctermfg=NONE ctermbg=000  cterm=NONE
hi TabLineFill           ctermfg=NONE ctermbg=000  cterm=NONE
hi TabLineSel            ctermfg=NONE ctermbg=000  cterm=BOLD,UNDERLINE

" Cursor / dynamic / other {{{1
hi Cursor                ctermfg=000  ctermbg=015  cterm=NONE
hi CursorIM              ctermfg=000  ctermbg=015  cterm=REVERSE
hi CursorLine            ctermfg=NONE ctermbg=000  cterm=NONE
hi CursorColumn          ctermfg=NONE ctermbg=000  cterm=NONE

hi Visual                ctermfg=NONE ctermbg=NONE cterm=REVERSE

hi IncSearch             ctermfg=014  ctermbg=NONE cterm=UNDERLINE,REVERSE
hi Search                ctermfg=NONE ctermbg=NONE cterm=UNDERLINE

hi MatchParen            ctermfg=NONE ctermbg=NONE cterm=BOLD

" Listings / messages {{{1
hi ModeMsg               ctermfg=011  ctermbg=NONE cterm=NONE
hi Title                 ctermfg=009  ctermbg=NONE cterm=BOLD
hi Question              ctermfg=010  ctermbg=NONE cterm=NONE
hi MoreMsg               ctermfg=010  ctermbg=NONE cterm=NONE
hi ErrorMsg              ctermfg=015  ctermbg=009  cterm=BOLD
hi WarningMsg            ctermfg=011  ctermbg=NONE cterm=BOLD

" Syntax highlighting groups {{{1
hi Comment               ctermfg=130  ctermbg=NONE cterm=NONE
hi Constant              ctermfg=009  ctermbg=NONE cterm=NONE
 hi String               ctermfg=002  ctermbg=NONE cterm=NONE
hi Function              ctermfg=011  ctermbg=NONE cterm=BOLD
 hi Identifier           ctermfg=011  ctermbg=NONE cterm=NONE
hi Statement             ctermfg=010  ctermbg=NONE cterm=BOLD
 hi Operator             ctermfg=013  ctermbg=NONE cterm=NONE
hi PreProc               ctermfg=004  ctermbg=NONE cterm=NONE
hi Type                  ctermfg=012  ctermbg=NONE cterm=BOLD
hi Special               ctermfg=NONE ctermbg=NONE cterm=BOLD
 hi Delimiter            ctermfg=NONE ctermbg=NONE cterm=NONE
hi Underlined            ctermfg=NONE ctermbg=NONE cterm=UNDERLINE
hi Ignore                ctermfg=008  ctermbg=NONE cterm=NONE
hi Error                 ctermfg=015  ctermbg=009  cterm=NONE
hi Todo                  ctermfg=000  ctermbg=NONE cterm=BOLD

" ALE {{{1
hi ALEError              guisp=#FF0000 cterm=undercurl
hi ALEErrorSign          ctermfg=196   cterm=BOLD
hi ALEStyleError         guisp=#AF0000 cterm=undercurl
hi ALEStyleErrorSign     ctermfg=124   cterm=NONE
hi ALEWarning            guisp=#FFFF00 cterm=undercurl
hi ALEWarningSign        ctermfg=226   cterm=BOLD
hi ALEStyleWarning       guisp=#AFAF00 cterm=undercurl
hi ALEStyleWarningSign   ctermfg=142   cterm=NONE
hi ALEInfo               guisp=#FFFFFF cterm=undercurl
hi ALEInfoSign           ctermfg=NONE  cterm=NONE

" Semshi {{{1
hi semshiLocal           ctermfg=251
hi semshiFree            ctermfg=183
hi semshiGlobal          ctermfg=220
hi semshiImported        ctermfg=214
hi semshiParameter       ctermfg=075
hi semshiParameterUnused ctermfg=117               cterm=UNDERLINE
hi semshiBuiltin         ctermfg=207
hi semshiAttribute       ctermfg=049
hi semshiSelf            ctermfg=249
hi semshiUnresolved      ctermfg=226               cterm=UNDERLINE
hi semshiSelected                                  cterm=UNDERLINE

" Manual overrides {{{1
hi link hsExprKeyword Statement
hi link hsStructure   Operator
hi link shDerefSimple Identifier

hi lilyDuration          ctermfg=001               cterm=BOLD
hi lilyRest              ctermfg=012
hi lilyLyric                                       cterm=ITALIC
hi lilyCommand           ctermfg=011               cterm=BOLD

hi link sqlKeyword Type
hi link sqlOperator Operator

hi link zshSubst NONE
hi link zshSubstDelim PreProc

hi link pythonStrInterpRegion Normal
" }}}1
let &cpo = save_cpo
