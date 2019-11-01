if exists("b:current_syntax")
	finish
endif

syn sync fromstart

syn cluster luaExpr←   contains=luaCommentA←,luaConstant←,luaNumber←,luaString←,luaBuiltin←,luaTable←,luaOperator←,luaEllipsis←,luaFunc←,luaError←,luaWord←,luaUnop←,luaParen←
syn cluster luaStmt←   contains=luaCommentB←,@luaExpr←,luaIf←,luaDo←,luaLoop←,luaLabel←,luaLocal←,luaStmt←,luaSemi←
syn cluster luaSuffix← contains=luaCommentC←,luaDot←,luaCall←,luaStringSuf←,luaBinop←,luaIndex←

syn match   luaShebang                              /\%^#!.*/

syn region  luaTable←    ↑         matchgroup=luaD← start=/{/                  end=/}/                                    contains=@luaExpr→,luaComma←,luaTableKey→
syn match   luaTableEq←  contained                  /=/                                             nextgroup=@luaExpr→
syn match   luaTableKey→ contained                  /\K\k*/                                         nextgroup=luaTableEq←
syn region  luaTableKey→ contained matchgroup=luaD← start=/\[/                 end=/]/              nextgroup=luaTableEq← contains=@luaExpr→,luaComma→

syn match   luaWord←     ↑                          /\K\k*/                                         nextgroup=@luaSuffix←
syn region  luaParen←    ↑         matchgroup=luaD← start=/(/                  end=/)/              nextgroup=@luaSuffix← contains=@luaExpr→,luaComma←
syn match   luaDot←      contained                  /./                                             nextgroup=luaWord←
syn match   luaDot←      contained                  /::\@!/                                         nextgroup=luaWord←
syn region  luaIndex←    contained matchgroup=luaD← start=/\[/                 end=/\]/             nextgroup=@luaSuffix← contains=@luaExpr→,luaComma→
syn region  luaCall←     contained matchgroup=luaD← start=/(/                  end=/)/              nextgroup=@luaSuffix← contains=@luaExpr→,luaComma←
syn region  luaCall←     contained matchgroup=luaD← start=/{/                  end=/}/              nextgroup=@luaSuffix← contains=@luaExpr→,luaComma←,luaTableKey→
syn match   luaUnop←     ↑                          /[#~-]\|\<not\>/                                nextgroup=@luaExpr←,luaComma→
syn match   luaBinop←    contained                  /[<>=~^&|*/%+-]/                                nextgroup=@luaExpr←,luaComma→
syn match   luaBinop←    contained                  ://\|>>\|<<\|\.\.\|[<>=~]=:                     nextgroup=@luaExpr←,luaComma→
syn match   luaBinop←    contained                  /\<and\>\|\<or\>/                               nextgroup=@luaExpr←,luaComma→

syn keyword luaConstant← ↑                          nil true false                                  nextgroup=@luaSuffix←
syn keyword luaBuiltin←  ↑                          _ENV self                                       nextgroup=@luaSuffix←

syn region  luaString←   ↑                          start=/\[\z(=*\)\[/        end=/\]\z1\]/        nextgroup=@luaSuffix←
syn region  luaString←   ↑                          start=/'/                  end=/'/              nextgroup=@luaSuffix← contains=luaEscape
syn region  luaString←   ↑                          start=/"/                  end=/"/              nextgroup=@luaSuffix← contains=luaEscape
syn match   luaEscape    contained                  /\\[\\abfnrtvz'"]/
syn match   luaEscape    contained                  /\\x\x\x/
syn match   luaEscape    contained                  /\\\d\{1,3}/

syn match   luaNumber←   ↑                            /\v\c%(<\d+%(\.\d*)?|\.\d+)%(e[-+]?\d+)?/     nextgroup=@luaSuffix←
syn match   luaNumber←   ↑                          /\v\c<0x%(\x+%(\.\x*)?|\.\x+)%(p[-+]?\d+)?/     nextgroup=@luaSuffix←

syn match   luaError←    ↑                          /[]}).:]/
syn match   luaError←    ↑                          /\<\%(end\|else\|elseif\|then\|until\|in\)\>/

syn match   luaComma←    ↑                          /,/
syn match   luaSemi←     ↑                          /;/
syn match   luaEllipsis← ↑                          /\.\.\./

syn match   luaCommentA← ↑                          /--.*$/                                         nextgroup=@luaExpr←,luaComma→   contains=luaTodo
syn region  luaCommentA← ↑                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        nextgroup=@luaExpr←,luaComma→   contains=luaTodo
syn match   luaCommentB← ↑                          /--.*$/                                         nextgroup=@luaStmt←   contains=luaTodo
syn region  luaCommentB← ↑                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        nextgroup=@luaStmt←   contains=luaTodo
syn match   luaCommentC← ↑                          /--.*$/                                         nextgroup=@luaSuffix← contains=luaTodo
syn region  luaCommentC← ↑                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        nextgroup=@luaSuffix← contains=luaTodo
syn keyword luaTodo      contained                  TODO FIXME XXX

syn region  luaFunc←     ↑         matchgroup=luaD← start=/\<function\>/       end=/\<end\>/                              contains=@luaStmt→,luaFuncSig←
syn region  luaFuncSig←  contained transparent      start=/\%(\<function\>\)\@<=/ end=/)/                                 contains=luaFuncId→,luaFuncArgs← keepend
syn match   luaFuncId←   contained                  /[^(]*(\@=/
syn region  luaFuncArgs← contained matchgroup=luaD← start=/(/                  end=/)/                                    contains=luaArg→,luaComma←,luaEllipsis→
syn match   luaArg←      contained                  /\K\k*/
" TODO highlight _ENV, self, and errors

syn region  luaIf←       ↑         matchgroup=luaD← start=/\<if\>/             end=/\ze\<then\>/    nextgroup=luaIfBody←  contains=@luaExpr→,luaComma→
syn region  luaIfBody←   contained matchgroup=luaD← start=/\<then\>/           end=/\<end\>/                              contains=@luaStmt→,luaElse←
syn region  luaElse←     contained matchgroup=luaD← start=/\<elseif\>/         end=/\<then\>/                             contains=@luaExpr→,luaComma→
syn region  luaElse←     contained matchgroup=luaD← start=/\<else\>/           end=/\>/

syn region  luaLoop←     ↑         matchgroup=luaD← start=/\<while\>/          end=/\ze\<do\>/      nextgroup=luaDo←      contains=@luaExpr→,luaComma→
syn region  luaLoop←     ↑         matchgroup=luaD← start=/\<for\>/            end=/\ze\<do\>/      nextgroup=luaDo←      contains=@luaExpr→,luaIn←
syn region  luaDo←       ↑         matchgroup=luaD← start=/\<do\>/             end=/\<end\>/                              contains=@luaStmt→,luaComma→
syn match   luaIn→       contained                  /\<in\>\|,\|=/

syn region  luaLoop←     ↑         matchgroup=luaD← start=/\<repeat\>/         end=/\<until\>/      nextgroup=@luaExpr→,luaComma→   contains=@luaStmt→

syn keyword luaStmt←     ↑                          goto                                            nextgroup=luaGotoL←
syn keyword luaStmt←     ↑                          local
syn match   luaGotoL←    contained                  /\K\k*/
syn match   luaLabel←    ↑                          /::\K\k*::/                                                           contains=luaLabelD←
syn match   luaLabelD←   contained                  /:/
syn keyword luaStmt←     ↑                          break return

hi def link luaBuiltin←    Special
hi def link luaShebang     Special
hi def link luaCommentA←   Comment
hi def link luaCommentB←   Comment
hi def link luaCommentC←   Comment
hi def link luaTodo        Todo
hi def link luaConstant←   Constant
hi def link luaEllipsis←   Special
hi def link luaError←      Error
hi def link luaNumber←     Number
hi def link luaString←     String
hi def link luaEscape      SpecialChar

hi def link luaBinop←      luaD←
hi def link luaComma←      luaD←
hi def link luaDot←        luaD←
hi def link luaElse←       luaD←
hi def link luaIn←         luaD←
hi def link luaKwd←        luaD←
hi def link luaLabelD←     luaD←
hi def link luaOperator←   luaD←
hi def link luaSemi←       luaD←
hi def link luaStmt←       luaD←
hi def link luaTableEq←    luaD←
hi def link luaUnop←       luaD←

hi def link luaArg←        luaT←
hi def link luaDelim←      luaT←
hi def link luaDo←         luaT←
hi def link luaFuncId←     luaT←
hi def link luaFunc←       luaT←
hi def link luaGotoL←      luaT←
hi def link luaIfBody←     luaT←
hi def link luaIf←         luaT←
hi def link luaLabel←      luaT←
hi def link luaSuffix←     luaT←
hi def link luaTableKey←   luaT←
hi def link luaWord←       luaT←

if 1
	hi def luaT0 ctermfg=224
	hi def luaT1 ctermfg=230
	hi def luaT2 ctermfg=194
	hi def luaT3 ctermfg=195
	hi def luaT4 ctermfg=189
	hi def luaT5 ctermfg=225
	hi def luaD0 ctermfg=203
	hi def luaD1 ctermfg=220
	hi def luaD2 ctermfg=083
	hi def luaD3 ctermfg=087
	hi def luaD4 ctermfg=075
	hi def luaD5 ctermfg=213
else
	hi def luaT0 ctermfg=203
	hi def luaT1 ctermfg=220
	hi def luaT2 ctermfg=083
	hi def luaT3 ctermfg=087
	hi def luaT4 ctermfg=075
	hi def luaT5 ctermfg=213
	hi def luaD0 ctermfg=203 cterm=bold
	hi def luaD1 ctermfg=220 cterm=bold
	hi def luaD2 ctermfg=083 cterm=bold
	hi def luaD3 ctermfg=087 cterm=bold
	hi def luaD4 ctermfg=075 cterm=bold
	hi def luaD5 ctermfg=213 cterm=bold
endif

let b:current_syntax = "lua"
" vim: colorcolumn=13,26,36,53,80,101,123
