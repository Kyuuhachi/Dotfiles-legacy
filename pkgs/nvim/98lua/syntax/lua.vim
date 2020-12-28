if exists("b:current_syntax")
	finish
endif

syn sync fromstart

syn cluster luaExpr0   contains=luaCommentA0,luaConstant0,luaNumber0,luaString0,luaBuiltin0,luaTable0,luaOperator0,luaEllipsis0,luaFunc0,luaError0,luaWord0,luaUnop0,luaParen0
syn cluster luaExpr1   contains=luaCommentA1,luaConstant1,luaNumber1,luaString1,luaBuiltin1,luaTable1,luaOperator1,luaEllipsis1,luaFunc1,luaError1,luaWord1,luaUnop1,luaParen1
syn cluster luaExpr2   contains=luaCommentA2,luaConstant2,luaNumber2,luaString2,luaBuiltin2,luaTable2,luaOperator2,luaEllipsis2,luaFunc2,luaError2,luaWord2,luaUnop2,luaParen2
syn cluster luaExpr3   contains=luaCommentA3,luaConstant3,luaNumber3,luaString3,luaBuiltin3,luaTable3,luaOperator3,luaEllipsis3,luaFunc3,luaError3,luaWord3,luaUnop3,luaParen3
syn cluster luaExpr4   contains=luaCommentA4,luaConstant4,luaNumber4,luaString4,luaBuiltin4,luaTable4,luaOperator4,luaEllipsis4,luaFunc4,luaError4,luaWord4,luaUnop4,luaParen4
syn cluster luaExpr5   contains=luaCommentA5,luaConstant5,luaNumber5,luaString5,luaBuiltin5,luaTable5,luaOperator5,luaEllipsis5,luaFunc5,luaError5,luaWord5,luaUnop5,luaParen5
syn cluster luaStmt0   contains=luaCommentB0,@luaExpr0,luaIf0,luaDo0,luaLoop0,luaLabel0,luaLocal0,luaStmt0,luaSemi0
syn cluster luaStmt1   contains=luaCommentB1,@luaExpr1,luaIf1,luaDo1,luaLoop1,luaLabel1,luaLocal1,luaStmt1,luaSemi1
syn cluster luaStmt2   contains=luaCommentB2,@luaExpr2,luaIf2,luaDo2,luaLoop2,luaLabel2,luaLocal2,luaStmt2,luaSemi2
syn cluster luaStmt3   contains=luaCommentB3,@luaExpr3,luaIf3,luaDo3,luaLoop3,luaLabel3,luaLocal3,luaStmt3,luaSemi3
syn cluster luaStmt4   contains=luaCommentB4,@luaExpr4,luaIf4,luaDo4,luaLoop4,luaLabel4,luaLocal4,luaStmt4,luaSemi4
syn cluster luaStmt5   contains=luaCommentB5,@luaExpr5,luaIf5,luaDo5,luaLoop5,luaLabel5,luaLocal5,luaStmt5,luaSemi5
syn cluster luaSuffix0 contains=luaCommentC0,luaDot0,luaCall0,luaStringSuf0,luaBinop0,luaIndex0
syn cluster luaSuffix1 contains=luaCommentC1,luaDot1,luaCall1,luaStringSuf1,luaBinop1,luaIndex1
syn cluster luaSuffix2 contains=luaCommentC2,luaDot2,luaCall2,luaStringSuf2,luaBinop2,luaIndex2
syn cluster luaSuffix3 contains=luaCommentC3,luaDot3,luaCall3,luaStringSuf3,luaBinop3,luaIndex3
syn cluster luaSuffix4 contains=luaCommentC4,luaDot4,luaCall4,luaStringSuf4,luaBinop4,luaIndex4
syn cluster luaSuffix5 contains=luaCommentC5,luaDot5,luaCall5,luaStringSuf5,luaBinop5,luaIndex5

syn match   luaShebang                              /\%^#!.*/

syn region  luaTable0            matchgroup=luaD0 start=/{/                  end=/}/                                    contains=@luaExpr1,luaComma0,luaTableKey1
syn region  luaTable1    contained         matchgroup=luaD1 start=/{/                  end=/}/                                    contains=@luaExpr2,luaComma1,luaTableKey2
syn region  luaTable2    contained         matchgroup=luaD2 start=/{/                  end=/}/                                    contains=@luaExpr3,luaComma2,luaTableKey3
syn region  luaTable3    contained         matchgroup=luaD3 start=/{/                  end=/}/                                    contains=@luaExpr4,luaComma3,luaTableKey4
syn region  luaTable4    contained         matchgroup=luaD4 start=/{/                  end=/}/                                    contains=@luaExpr5,luaComma4,luaTableKey5
syn region  luaTable5    contained         matchgroup=luaD5 start=/{/                  end=/}/                                    contains=@luaExpr0,luaComma5,luaTableKey0
syn match   luaTableEq0  contained                  /=/                                             skipwhite skipempty nextgroup=@luaExpr1
syn match   luaTableEq1  contained                  /=/                                             skipwhite skipempty nextgroup=@luaExpr2
syn match   luaTableEq2  contained                  /=/                                             skipwhite skipempty nextgroup=@luaExpr3
syn match   luaTableEq3  contained                  /=/                                             skipwhite skipempty nextgroup=@luaExpr4
syn match   luaTableEq4  contained                  /=/                                             skipwhite skipempty nextgroup=@luaExpr5
syn match   luaTableEq5  contained                  /=/                                             skipwhite skipempty nextgroup=@luaExpr0
syn match   luaTableKey1 contained                  /\K\k*/                                         skipwhite skipempty nextgroup=luaTableEq0
syn match   luaTableKey2 contained                  /\K\k*/                                         skipwhite skipempty nextgroup=luaTableEq1
syn match   luaTableKey3 contained                  /\K\k*/                                         skipwhite skipempty nextgroup=luaTableEq2
syn match   luaTableKey4 contained                  /\K\k*/                                         skipwhite skipempty nextgroup=luaTableEq3
syn match   luaTableKey5 contained                  /\K\k*/                                         skipwhite skipempty nextgroup=luaTableEq4
syn match   luaTableKey0 contained                  /\K\k*/                                         skipwhite skipempty nextgroup=luaTableEq5
syn region  luaTableKey1 contained matchgroup=luaD0 start=/\[/                 end=/]/              skipwhite skipempty nextgroup=luaTableEq0 contains=@luaExpr1,luaComma1
syn region  luaTableKey2 contained matchgroup=luaD1 start=/\[/                 end=/]/              skipwhite skipempty nextgroup=luaTableEq1 contains=@luaExpr2,luaComma2
syn region  luaTableKey3 contained matchgroup=luaD2 start=/\[/                 end=/]/              skipwhite skipempty nextgroup=luaTableEq2 contains=@luaExpr3,luaComma3
syn region  luaTableKey4 contained matchgroup=luaD3 start=/\[/                 end=/]/              skipwhite skipempty nextgroup=luaTableEq3 contains=@luaExpr4,luaComma4
syn region  luaTableKey5 contained matchgroup=luaD4 start=/\[/                 end=/]/              skipwhite skipempty nextgroup=luaTableEq4 contains=@luaExpr5,luaComma5
syn region  luaTableKey0 contained matchgroup=luaD5 start=/\[/                 end=/]/              skipwhite skipempty nextgroup=luaTableEq5 contains=@luaExpr0,luaComma0

syn match   luaWord0                              /\K\k*/                                         skipwhite skipempty nextgroup=@luaSuffix0
syn match   luaWord1     contained                          /\K\k*/                                         skipwhite skipempty nextgroup=@luaSuffix1
syn match   luaWord2     contained                          /\K\k*/                                         skipwhite skipempty nextgroup=@luaSuffix2
syn match   luaWord3     contained                          /\K\k*/                                         skipwhite skipempty nextgroup=@luaSuffix3
syn match   luaWord4     contained                          /\K\k*/                                         skipwhite skipempty nextgroup=@luaSuffix4
syn match   luaWord5     contained                          /\K\k*/                                         skipwhite skipempty nextgroup=@luaSuffix5
syn region  luaParen0            matchgroup=luaD0 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix0 contains=@luaExpr1,luaComma0
syn region  luaParen1    contained         matchgroup=luaD1 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix1 contains=@luaExpr2,luaComma1
syn region  luaParen2    contained         matchgroup=luaD2 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix2 contains=@luaExpr3,luaComma2
syn region  luaParen3    contained         matchgroup=luaD3 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix3 contains=@luaExpr4,luaComma3
syn region  luaParen4    contained         matchgroup=luaD4 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix4 contains=@luaExpr5,luaComma4
syn region  luaParen5    contained         matchgroup=luaD5 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix5 contains=@luaExpr0,luaComma5
syn match   luaDot0      contained                  /[.:]/                                          skipwhite skipempty nextgroup=luaWord0
syn match   luaDot1      contained                  /[.:]/                                          skipwhite skipempty nextgroup=luaWord1
syn match   luaDot2      contained                  /[.:]/                                          skipwhite skipempty nextgroup=luaWord2
syn match   luaDot3      contained                  /[.:]/                                          skipwhite skipempty nextgroup=luaWord3
syn match   luaDot4      contained                  /[.:]/                                          skipwhite skipempty nextgroup=luaWord4
syn match   luaDot5      contained                  /[.:]/                                          skipwhite skipempty nextgroup=luaWord5
syn region  luaIndex0    contained matchgroup=luaD0 start=/\[/                 end=/\]/             skipwhite skipempty nextgroup=@luaSuffix0 contains=@luaExpr1,luaComma1
syn region  luaIndex1    contained matchgroup=luaD1 start=/\[/                 end=/\]/             skipwhite skipempty nextgroup=@luaSuffix1 contains=@luaExpr2,luaComma2
syn region  luaIndex2    contained matchgroup=luaD2 start=/\[/                 end=/\]/             skipwhite skipempty nextgroup=@luaSuffix2 contains=@luaExpr3,luaComma3
syn region  luaIndex3    contained matchgroup=luaD3 start=/\[/                 end=/\]/             skipwhite skipempty nextgroup=@luaSuffix3 contains=@luaExpr4,luaComma4
syn region  luaIndex4    contained matchgroup=luaD4 start=/\[/                 end=/\]/             skipwhite skipempty nextgroup=@luaSuffix4 contains=@luaExpr5,luaComma5
syn region  luaIndex5    contained matchgroup=luaD5 start=/\[/                 end=/\]/             skipwhite skipempty nextgroup=@luaSuffix5 contains=@luaExpr0,luaComma0
syn region  luaCall0     contained matchgroup=luaD0 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix0 contains=@luaExpr1,luaComma0
syn region  luaCall1     contained matchgroup=luaD1 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix1 contains=@luaExpr2,luaComma1
syn region  luaCall2     contained matchgroup=luaD2 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix2 contains=@luaExpr3,luaComma2
syn region  luaCall3     contained matchgroup=luaD3 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix3 contains=@luaExpr4,luaComma3
syn region  luaCall4     contained matchgroup=luaD4 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix4 contains=@luaExpr5,luaComma4
syn region  luaCall5     contained matchgroup=luaD5 start=/(/                  end=/)/              skipwhite skipempty nextgroup=@luaSuffix5 contains=@luaExpr0,luaComma5
syn region  luaCall0     contained matchgroup=luaD0 start=/{/                  end=/}/              skipwhite skipempty nextgroup=@luaSuffix0 contains=@luaExpr1,luaComma0,luaTableKey1
syn region  luaCall1     contained matchgroup=luaD1 start=/{/                  end=/}/              skipwhite skipempty nextgroup=@luaSuffix1 contains=@luaExpr2,luaComma1,luaTableKey2
syn region  luaCall2     contained matchgroup=luaD2 start=/{/                  end=/}/              skipwhite skipempty nextgroup=@luaSuffix2 contains=@luaExpr3,luaComma2,luaTableKey3
syn region  luaCall3     contained matchgroup=luaD3 start=/{/                  end=/}/              skipwhite skipempty nextgroup=@luaSuffix3 contains=@luaExpr4,luaComma3,luaTableKey4
syn region  luaCall4     contained matchgroup=luaD4 start=/{/                  end=/}/              skipwhite skipempty nextgroup=@luaSuffix4 contains=@luaExpr5,luaComma4,luaTableKey5
syn region  luaCall5     contained matchgroup=luaD5 start=/{/                  end=/}/              skipwhite skipempty nextgroup=@luaSuffix5 contains=@luaExpr0,luaComma5,luaTableKey0
syn match   luaUnop0                              /[#~-]\|\<not\>/                                skipwhite skipempty nextgroup=@luaExpr0,luaComma1
syn match   luaUnop1     contained                          /[#~-]\|\<not\>/                                skipwhite skipempty nextgroup=@luaExpr1,luaComma2
syn match   luaUnop2     contained                          /[#~-]\|\<not\>/                                skipwhite skipempty nextgroup=@luaExpr2,luaComma3
syn match   luaUnop3     contained                          /[#~-]\|\<not\>/                                skipwhite skipempty nextgroup=@luaExpr3,luaComma4
syn match   luaUnop4     contained                          /[#~-]\|\<not\>/                                skipwhite skipempty nextgroup=@luaExpr4,luaComma5
syn match   luaUnop5     contained                          /[#~-]\|\<not\>/                                skipwhite skipempty nextgroup=@luaExpr5,luaComma0
syn match   luaBinop0    contained                  /[<>=~^&|*/%+-]/                                skipwhite skipempty nextgroup=@luaExpr0,luaComma1
syn match   luaBinop1    contained                  /[<>=~^&|*/%+-]/                                skipwhite skipempty nextgroup=@luaExpr1,luaComma2
syn match   luaBinop2    contained                  /[<>=~^&|*/%+-]/                                skipwhite skipempty nextgroup=@luaExpr2,luaComma3
syn match   luaBinop3    contained                  /[<>=~^&|*/%+-]/                                skipwhite skipempty nextgroup=@luaExpr3,luaComma4
syn match   luaBinop4    contained                  /[<>=~^&|*/%+-]/                                skipwhite skipempty nextgroup=@luaExpr4,luaComma5
syn match   luaBinop5    contained                  /[<>=~^&|*/%+-]/                                skipwhite skipempty nextgroup=@luaExpr5,luaComma0
syn match   luaBinop0    contained                  ://\|>>\|<<\|\.\.\|[<>=~]=:                     skipwhite skipempty nextgroup=@luaExpr0,luaComma1
syn match   luaBinop1    contained                  ://\|>>\|<<\|\.\.\|[<>=~]=:                     skipwhite skipempty nextgroup=@luaExpr1,luaComma2
syn match   luaBinop2    contained                  ://\|>>\|<<\|\.\.\|[<>=~]=:                     skipwhite skipempty nextgroup=@luaExpr2,luaComma3
syn match   luaBinop3    contained                  ://\|>>\|<<\|\.\.\|[<>=~]=:                     skipwhite skipempty nextgroup=@luaExpr3,luaComma4
syn match   luaBinop4    contained                  ://\|>>\|<<\|\.\.\|[<>=~]=:                     skipwhite skipempty nextgroup=@luaExpr4,luaComma5
syn match   luaBinop5    contained                  ://\|>>\|<<\|\.\.\|[<>=~]=:                     skipwhite skipempty nextgroup=@luaExpr5,luaComma0
syn match   luaBinop0    contained                  /\<and\>\|\<or\>/                               skipwhite skipempty nextgroup=@luaExpr0,luaComma1
syn match   luaBinop1    contained                  /\<and\>\|\<or\>/                               skipwhite skipempty nextgroup=@luaExpr1,luaComma2
syn match   luaBinop2    contained                  /\<and\>\|\<or\>/                               skipwhite skipempty nextgroup=@luaExpr2,luaComma3
syn match   luaBinop3    contained                  /\<and\>\|\<or\>/                               skipwhite skipempty nextgroup=@luaExpr3,luaComma4
syn match   luaBinop4    contained                  /\<and\>\|\<or\>/                               skipwhite skipempty nextgroup=@luaExpr4,luaComma5
syn match   luaBinop5    contained                  /\<and\>\|\<or\>/                               skipwhite skipempty nextgroup=@luaExpr5,luaComma0

syn keyword luaConstant0                          nil true false                                  skipwhite skipempty nextgroup=@luaSuffix0
syn keyword luaConstant1 contained                          nil true false                                  skipwhite skipempty nextgroup=@luaSuffix1
syn keyword luaConstant2 contained                          nil true false                                  skipwhite skipempty nextgroup=@luaSuffix2
syn keyword luaConstant3 contained                          nil true false                                  skipwhite skipempty nextgroup=@luaSuffix3
syn keyword luaConstant4 contained                          nil true false                                  skipwhite skipempty nextgroup=@luaSuffix4
syn keyword luaConstant5 contained                          nil true false                                  skipwhite skipempty nextgroup=@luaSuffix5
syn keyword luaBuiltin0                           _ENV self                                       skipwhite skipempty nextgroup=@luaSuffix0
syn keyword luaBuiltin1  contained                          _ENV self                                       skipwhite skipempty nextgroup=@luaSuffix1
syn keyword luaBuiltin2  contained                          _ENV self                                       skipwhite skipempty nextgroup=@luaSuffix2
syn keyword luaBuiltin3  contained                          _ENV self                                       skipwhite skipempty nextgroup=@luaSuffix3
syn keyword luaBuiltin4  contained                          _ENV self                                       skipwhite skipempty nextgroup=@luaSuffix4
syn keyword luaBuiltin5  contained                          _ENV self                                       skipwhite skipempty nextgroup=@luaSuffix5

syn region  luaString0                            start=/\[\z(=*\)\[/        end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix0
syn region  luaString1   contained                          start=/\[\z(=*\)\[/        end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix1
syn region  luaString2   contained                          start=/\[\z(=*\)\[/        end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix2
syn region  luaString3   contained                          start=/\[\z(=*\)\[/        end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix3
syn region  luaString4   contained                          start=/\[\z(=*\)\[/        end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix4
syn region  luaString5   contained                          start=/\[\z(=*\)\[/        end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix5
syn region  luaString0                            start=/'/                  end=/'/              skipwhite skipempty nextgroup=@luaSuffix0 contains=luaEscape
syn region  luaString1   contained                          start=/'/                  end=/'/              skipwhite skipempty nextgroup=@luaSuffix1 contains=luaEscape
syn region  luaString2   contained                          start=/'/                  end=/'/              skipwhite skipempty nextgroup=@luaSuffix2 contains=luaEscape
syn region  luaString3   contained                          start=/'/                  end=/'/              skipwhite skipempty nextgroup=@luaSuffix3 contains=luaEscape
syn region  luaString4   contained                          start=/'/                  end=/'/              skipwhite skipempty nextgroup=@luaSuffix4 contains=luaEscape
syn region  luaString5   contained                          start=/'/                  end=/'/              skipwhite skipempty nextgroup=@luaSuffix5 contains=luaEscape
syn region  luaString0                            start=/"/                  end=/"/              skipwhite skipempty nextgroup=@luaSuffix0 contains=luaEscape
syn region  luaString1   contained                          start=/"/                  end=/"/              skipwhite skipempty nextgroup=@luaSuffix1 contains=luaEscape
syn region  luaString2   contained                          start=/"/                  end=/"/              skipwhite skipempty nextgroup=@luaSuffix2 contains=luaEscape
syn region  luaString3   contained                          start=/"/                  end=/"/              skipwhite skipempty nextgroup=@luaSuffix3 contains=luaEscape
syn region  luaString4   contained                          start=/"/                  end=/"/              skipwhite skipempty nextgroup=@luaSuffix4 contains=luaEscape
syn region  luaString5   contained                          start=/"/                  end=/"/              skipwhite skipempty nextgroup=@luaSuffix5 contains=luaEscape
syn match   luaEscape    contained                  /\\[\\abfnrtvz'"]/
syn match   luaEscape    contained                  /\\x\x\x/
syn match   luaEscape    contained                  /\\\d\{1,3}/

syn match   luaNumber0                              /\v\c%(<\d+%(\.\d*)?|\.\d+)%(e[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix0
syn match   luaNumber1   contained                            /\v\c%(<\d+%(\.\d*)?|\.\d+)%(e[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix1
syn match   luaNumber2   contained                            /\v\c%(<\d+%(\.\d*)?|\.\d+)%(e[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix2
syn match   luaNumber3   contained                            /\v\c%(<\d+%(\.\d*)?|\.\d+)%(e[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix3
syn match   luaNumber4   contained                            /\v\c%(<\d+%(\.\d*)?|\.\d+)%(e[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix4
syn match   luaNumber5   contained                            /\v\c%(<\d+%(\.\d*)?|\.\d+)%(e[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix5
syn match   luaNumber0                            /\v\c<0x%(\x+%(\.\x*)?|\.\x+)%(p[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix0
syn match   luaNumber1   contained                          /\v\c<0x%(\x+%(\.\x*)?|\.\x+)%(p[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix1
syn match   luaNumber2   contained                          /\v\c<0x%(\x+%(\.\x*)?|\.\x+)%(p[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix2
syn match   luaNumber3   contained                          /\v\c<0x%(\x+%(\.\x*)?|\.\x+)%(p[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix3
syn match   luaNumber4   contained                          /\v\c<0x%(\x+%(\.\x*)?|\.\x+)%(p[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix4
syn match   luaNumber5   contained                          /\v\c<0x%(\x+%(\.\x*)?|\.\x+)%(p[-+]?\d+)?/     skipwhite skipempty nextgroup=@luaSuffix5

syn match   luaError0                             /[]}).:]/
syn match   luaError1    contained                          /[]}).:]/
syn match   luaError2    contained                          /[]}).:]/
syn match   luaError3    contained                          /[]}).:]/
syn match   luaError4    contained                          /[]}).:]/
syn match   luaError5    contained                          /[]}).:]/
syn match   luaError0                             /\<\%(end\|else\|elseif\|then\|until\|in\)\>/
syn match   luaError1    contained                          /\<\%(end\|else\|elseif\|then\|until\|in\)\>/
syn match   luaError2    contained                          /\<\%(end\|else\|elseif\|then\|until\|in\)\>/
syn match   luaError3    contained                          /\<\%(end\|else\|elseif\|then\|until\|in\)\>/
syn match   luaError4    contained                          /\<\%(end\|else\|elseif\|then\|until\|in\)\>/
syn match   luaError5    contained                          /\<\%(end\|else\|elseif\|then\|until\|in\)\>/

syn match   luaComma0                             /,/
syn match   luaComma1    contained                          /,/
syn match   luaComma2    contained                          /,/
syn match   luaComma3    contained                          /,/
syn match   luaComma4    contained                          /,/
syn match   luaComma5    contained                          /,/
syn match   luaSemi0                              /;/
syn match   luaSemi1     contained                          /;/
syn match   luaSemi2     contained                          /;/
syn match   luaSemi3     contained                          /;/
syn match   luaSemi4     contained                          /;/
syn match   luaSemi5     contained                          /;/
syn match   luaEllipsis0                          /\.\.\./
syn match   luaEllipsis1 contained                          /\.\.\./
syn match   luaEllipsis2 contained                          /\.\.\./
syn match   luaEllipsis3 contained                          /\.\.\./
syn match   luaEllipsis4 contained                          /\.\.\./
syn match   luaEllipsis5 contained                          /\.\.\./

syn match   luaCommentA0                          /--.*$/                                         skipwhite skipempty nextgroup=@luaExpr0,luaComma1   contains=luaTodo
syn match   luaCommentA1 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaExpr1,luaComma2   contains=luaTodo
syn match   luaCommentA2 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaExpr2,luaComma3   contains=luaTodo
syn match   luaCommentA3 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaExpr3,luaComma4   contains=luaTodo
syn match   luaCommentA4 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaExpr4,luaComma5   contains=luaTodo
syn match   luaCommentA5 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaExpr5,luaComma0   contains=luaTodo
syn region  luaCommentA0                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaExpr0,luaComma1   contains=luaTodo
syn region  luaCommentA1 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaExpr1,luaComma2   contains=luaTodo
syn region  luaCommentA2 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaExpr2,luaComma3   contains=luaTodo
syn region  luaCommentA3 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaExpr3,luaComma4   contains=luaTodo
syn region  luaCommentA4 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaExpr4,luaComma5   contains=luaTodo
syn region  luaCommentA5 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaExpr5,luaComma0   contains=luaTodo
syn match   luaCommentB0                          /--.*$/                                         skipwhite skipempty nextgroup=@luaStmt0   contains=luaTodo
syn match   luaCommentB1 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaStmt1   contains=luaTodo
syn match   luaCommentB2 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaStmt2   contains=luaTodo
syn match   luaCommentB3 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaStmt3   contains=luaTodo
syn match   luaCommentB4 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaStmt4   contains=luaTodo
syn match   luaCommentB5 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaStmt5   contains=luaTodo
syn region  luaCommentB0                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaStmt0   contains=luaTodo
syn region  luaCommentB1 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaStmt1   contains=luaTodo
syn region  luaCommentB2 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaStmt2   contains=luaTodo
syn region  luaCommentB3 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaStmt3   contains=luaTodo
syn region  luaCommentB4 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaStmt4   contains=luaTodo
syn region  luaCommentB5 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaStmt5   contains=luaTodo
syn match   luaCommentC0                          /--.*$/                                         skipwhite skipempty nextgroup=@luaSuffix0 contains=luaTodo
syn match   luaCommentC1 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaSuffix1 contains=luaTodo
syn match   luaCommentC2 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaSuffix2 contains=luaTodo
syn match   luaCommentC3 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaSuffix3 contains=luaTodo
syn match   luaCommentC4 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaSuffix4 contains=luaTodo
syn match   luaCommentC5 contained                          /--.*$/                                         skipwhite skipempty nextgroup=@luaSuffix5 contains=luaTodo
syn region  luaCommentC0                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix0 contains=luaTodo
syn region  luaCommentC1 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix1 contains=luaTodo
syn region  luaCommentC2 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix2 contains=luaTodo
syn region  luaCommentC3 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix3 contains=luaTodo
syn region  luaCommentC4 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix4 contains=luaTodo
syn region  luaCommentC5 contained                          start=/--\[\z(=*\)\[/      end=/\]\z1\]/        skipwhite skipempty nextgroup=@luaSuffix5 contains=luaTodo
syn keyword luaTodo      contained                  TODO FIXME XXX

syn region  luaFunc0             matchgroup=luaD0 start=/\<function\>/       end=/\<end\>/                              contains=@luaStmt1,luaFuncSig0
syn region  luaFunc1     contained         matchgroup=luaD1 start=/\<function\>/       end=/\<end\>/                              contains=@luaStmt2,luaFuncSig1
syn region  luaFunc2     contained         matchgroup=luaD2 start=/\<function\>/       end=/\<end\>/                              contains=@luaStmt3,luaFuncSig2
syn region  luaFunc3     contained         matchgroup=luaD3 start=/\<function\>/       end=/\<end\>/                              contains=@luaStmt4,luaFuncSig3
syn region  luaFunc4     contained         matchgroup=luaD4 start=/\<function\>/       end=/\<end\>/                              contains=@luaStmt5,luaFuncSig4
syn region  luaFunc5     contained         matchgroup=luaD5 start=/\<function\>/       end=/\<end\>/                              contains=@luaStmt0,luaFuncSig5
syn region  luaFuncSig0  contained transparent      start=/\%(\<function\>\)\@<=/ end=/)/                                 contains=luaFuncId1,luaFuncArgs0 keepend
syn region  luaFuncSig1  contained transparent      start=/\%(\<function\>\)\@<=/ end=/)/                                 contains=luaFuncId2,luaFuncArgs1 keepend
syn region  luaFuncSig2  contained transparent      start=/\%(\<function\>\)\@<=/ end=/)/                                 contains=luaFuncId3,luaFuncArgs2 keepend
syn region  luaFuncSig3  contained transparent      start=/\%(\<function\>\)\@<=/ end=/)/                                 contains=luaFuncId4,luaFuncArgs3 keepend
syn region  luaFuncSig4  contained transparent      start=/\%(\<function\>\)\@<=/ end=/)/                                 contains=luaFuncId5,luaFuncArgs4 keepend
syn region  luaFuncSig5  contained transparent      start=/\%(\<function\>\)\@<=/ end=/)/                                 contains=luaFuncId0,luaFuncArgs5 keepend
syn match   luaFuncId0   contained                  /[^(]*(\@=/
syn match   luaFuncId1   contained                  /[^(]*(\@=/
syn match   luaFuncId2   contained                  /[^(]*(\@=/
syn match   luaFuncId3   contained                  /[^(]*(\@=/
syn match   luaFuncId4   contained                  /[^(]*(\@=/
syn match   luaFuncId5   contained                  /[^(]*(\@=/
syn region  luaFuncArgs0 contained matchgroup=luaD0 start=/(/                  end=/)/                                    contains=luaArg1,luaComma0,luaEllipsis1
syn region  luaFuncArgs1 contained matchgroup=luaD1 start=/(/                  end=/)/                                    contains=luaArg2,luaComma1,luaEllipsis2
syn region  luaFuncArgs2 contained matchgroup=luaD2 start=/(/                  end=/)/                                    contains=luaArg3,luaComma2,luaEllipsis3
syn region  luaFuncArgs3 contained matchgroup=luaD3 start=/(/                  end=/)/                                    contains=luaArg4,luaComma3,luaEllipsis4
syn region  luaFuncArgs4 contained matchgroup=luaD4 start=/(/                  end=/)/                                    contains=luaArg5,luaComma4,luaEllipsis5
syn region  luaFuncArgs5 contained matchgroup=luaD5 start=/(/                  end=/)/                                    contains=luaArg0,luaComma5,luaEllipsis0
syn match   luaArg0      contained                  /\K\k*/
syn match   luaArg1      contained                  /\K\k*/
syn match   luaArg2      contained                  /\K\k*/
syn match   luaArg3      contained                  /\K\k*/
syn match   luaArg4      contained                  /\K\k*/
syn match   luaArg5      contained                  /\K\k*/
" TODO highlight _ENV, self, and errors

syn region  luaIf0               matchgroup=luaD0 start=/\<if\>/             end=/\ze\<then\>/    skipwhite skipempty nextgroup=luaIfBody0  contains=@luaExpr1,luaComma1
syn region  luaIf1       contained         matchgroup=luaD1 start=/\<if\>/             end=/\ze\<then\>/    skipwhite skipempty nextgroup=luaIfBody1  contains=@luaExpr2,luaComma2
syn region  luaIf2       contained         matchgroup=luaD2 start=/\<if\>/             end=/\ze\<then\>/    skipwhite skipempty nextgroup=luaIfBody2  contains=@luaExpr3,luaComma3
syn region  luaIf3       contained         matchgroup=luaD3 start=/\<if\>/             end=/\ze\<then\>/    skipwhite skipempty nextgroup=luaIfBody3  contains=@luaExpr4,luaComma4
syn region  luaIf4       contained         matchgroup=luaD4 start=/\<if\>/             end=/\ze\<then\>/    skipwhite skipempty nextgroup=luaIfBody4  contains=@luaExpr5,luaComma5
syn region  luaIf5       contained         matchgroup=luaD5 start=/\<if\>/             end=/\ze\<then\>/    skipwhite skipempty nextgroup=luaIfBody5  contains=@luaExpr0,luaComma0
syn region  luaIfBody0   contained matchgroup=luaD0 start=/\<then\>/           end=/\<end\>/                              contains=@luaStmt1,luaElse0
syn region  luaIfBody1   contained matchgroup=luaD1 start=/\<then\>/           end=/\<end\>/                              contains=@luaStmt2,luaElse1
syn region  luaIfBody2   contained matchgroup=luaD2 start=/\<then\>/           end=/\<end\>/                              contains=@luaStmt3,luaElse2
syn region  luaIfBody3   contained matchgroup=luaD3 start=/\<then\>/           end=/\<end\>/                              contains=@luaStmt4,luaElse3
syn region  luaIfBody4   contained matchgroup=luaD4 start=/\<then\>/           end=/\<end\>/                              contains=@luaStmt5,luaElse4
syn region  luaIfBody5   contained matchgroup=luaD5 start=/\<then\>/           end=/\<end\>/                              contains=@luaStmt0,luaElse5
syn region  luaElse0     contained matchgroup=luaD0 start=/\<elseif\>/         end=/\<then\>/                             contains=@luaExpr1,luaComma1
syn region  luaElse1     contained matchgroup=luaD1 start=/\<elseif\>/         end=/\<then\>/                             contains=@luaExpr2,luaComma2
syn region  luaElse2     contained matchgroup=luaD2 start=/\<elseif\>/         end=/\<then\>/                             contains=@luaExpr3,luaComma3
syn region  luaElse3     contained matchgroup=luaD3 start=/\<elseif\>/         end=/\<then\>/                             contains=@luaExpr4,luaComma4
syn region  luaElse4     contained matchgroup=luaD4 start=/\<elseif\>/         end=/\<then\>/                             contains=@luaExpr5,luaComma5
syn region  luaElse5     contained matchgroup=luaD5 start=/\<elseif\>/         end=/\<then\>/                             contains=@luaExpr0,luaComma0
syn region  luaElse0     contained matchgroup=luaD0 start=/\<else\>/           end=/\>/
syn region  luaElse1     contained matchgroup=luaD1 start=/\<else\>/           end=/\>/
syn region  luaElse2     contained matchgroup=luaD2 start=/\<else\>/           end=/\>/
syn region  luaElse3     contained matchgroup=luaD3 start=/\<else\>/           end=/\>/
syn region  luaElse4     contained matchgroup=luaD4 start=/\<else\>/           end=/\>/
syn region  luaElse5     contained matchgroup=luaD5 start=/\<else\>/           end=/\>/

syn region  luaLoop0             matchgroup=luaD0 start=/\<while\>/          end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo0      contains=@luaExpr1,luaComma1
syn region  luaLoop1     contained         matchgroup=luaD1 start=/\<while\>/          end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo1      contains=@luaExpr2,luaComma2
syn region  luaLoop2     contained         matchgroup=luaD2 start=/\<while\>/          end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo2      contains=@luaExpr3,luaComma3
syn region  luaLoop3     contained         matchgroup=luaD3 start=/\<while\>/          end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo3      contains=@luaExpr4,luaComma4
syn region  luaLoop4     contained         matchgroup=luaD4 start=/\<while\>/          end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo4      contains=@luaExpr5,luaComma5
syn region  luaLoop5     contained         matchgroup=luaD5 start=/\<while\>/          end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo5      contains=@luaExpr0,luaComma0
syn region  luaLoop0             matchgroup=luaD0 start=/\<for\>/            end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo0      contains=@luaExpr1,luaIn0
syn region  luaLoop1     contained         matchgroup=luaD1 start=/\<for\>/            end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo1      contains=@luaExpr2,luaIn1
syn region  luaLoop2     contained         matchgroup=luaD2 start=/\<for\>/            end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo2      contains=@luaExpr3,luaIn2
syn region  luaLoop3     contained         matchgroup=luaD3 start=/\<for\>/            end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo3      contains=@luaExpr4,luaIn3
syn region  luaLoop4     contained         matchgroup=luaD4 start=/\<for\>/            end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo4      contains=@luaExpr5,luaIn4
syn region  luaLoop5     contained         matchgroup=luaD5 start=/\<for\>/            end=/\ze\<do\>/      skipwhite skipempty nextgroup=luaDo5      contains=@luaExpr0,luaIn5
syn region  luaDo0               matchgroup=luaD0 start=/\<do\>/             end=/\<end\>/                              contains=@luaStmt1,luaComma1
syn region  luaDo1       contained         matchgroup=luaD1 start=/\<do\>/             end=/\<end\>/                              contains=@luaStmt2,luaComma2
syn region  luaDo2       contained         matchgroup=luaD2 start=/\<do\>/             end=/\<end\>/                              contains=@luaStmt3,luaComma3
syn region  luaDo3       contained         matchgroup=luaD3 start=/\<do\>/             end=/\<end\>/                              contains=@luaStmt4,luaComma4
syn region  luaDo4       contained         matchgroup=luaD4 start=/\<do\>/             end=/\<end\>/                              contains=@luaStmt5,luaComma5
syn region  luaDo5       contained         matchgroup=luaD5 start=/\<do\>/             end=/\<end\>/                              contains=@luaStmt0,luaComma0
syn match   luaIn1       contained                  /\<in\>\|,\|=/
syn match   luaIn2       contained                  /\<in\>\|,\|=/
syn match   luaIn3       contained                  /\<in\>\|,\|=/
syn match   luaIn4       contained                  /\<in\>\|,\|=/
syn match   luaIn5       contained                  /\<in\>\|,\|=/
syn match   luaIn0       contained                  /\<in\>\|,\|=/

syn region  luaLoop0             matchgroup=luaD0 start=/\<repeat\>/         end=/\<until\>/      skipwhite skipempty nextgroup=@luaExpr1,luaComma1   contains=@luaStmt1
syn region  luaLoop1     contained         matchgroup=luaD1 start=/\<repeat\>/         end=/\<until\>/      skipwhite skipempty nextgroup=@luaExpr2,luaComma2   contains=@luaStmt2
syn region  luaLoop2     contained         matchgroup=luaD2 start=/\<repeat\>/         end=/\<until\>/      skipwhite skipempty nextgroup=@luaExpr3,luaComma3   contains=@luaStmt3
syn region  luaLoop3     contained         matchgroup=luaD3 start=/\<repeat\>/         end=/\<until\>/      skipwhite skipempty nextgroup=@luaExpr4,luaComma4   contains=@luaStmt4
syn region  luaLoop4     contained         matchgroup=luaD4 start=/\<repeat\>/         end=/\<until\>/      skipwhite skipempty nextgroup=@luaExpr5,luaComma5   contains=@luaStmt5
syn region  luaLoop5     contained         matchgroup=luaD5 start=/\<repeat\>/         end=/\<until\>/      skipwhite skipempty nextgroup=@luaExpr0,luaComma0   contains=@luaStmt0

syn keyword luaStmt0                              goto                                            skipwhite skipempty nextgroup=luaGotoL0
syn keyword luaStmt1     contained                          goto                                            skipwhite skipempty nextgroup=luaGotoL1
syn keyword luaStmt2     contained                          goto                                            skipwhite skipempty nextgroup=luaGotoL2
syn keyword luaStmt3     contained                          goto                                            skipwhite skipempty nextgroup=luaGotoL3
syn keyword luaStmt4     contained                          goto                                            skipwhite skipempty nextgroup=luaGotoL4
syn keyword luaStmt5     contained                          goto                                            skipwhite skipempty nextgroup=luaGotoL5
syn keyword luaStmt0                              local
syn keyword luaStmt1     contained                          local
syn keyword luaStmt2     contained                          local
syn keyword luaStmt3     contained                          local
syn keyword luaStmt4     contained                          local
syn keyword luaStmt5     contained                          local
syn match   luaGotoL0    contained                  /\K\k*/
syn match   luaGotoL1    contained                  /\K\k*/
syn match   luaGotoL2    contained                  /\K\k*/
syn match   luaGotoL3    contained                  /\K\k*/
syn match   luaGotoL4    contained                  /\K\k*/
syn match   luaGotoL5    contained                  /\K\k*/
syn match   luaLabel0                             /::\K\k*::/                                                           contains=luaLabelD0
syn match   luaLabel1    contained                          /::\K\k*::/                                                           contains=luaLabelD1
syn match   luaLabel2    contained                          /::\K\k*::/                                                           contains=luaLabelD2
syn match   luaLabel3    contained                          /::\K\k*::/                                                           contains=luaLabelD3
syn match   luaLabel4    contained                          /::\K\k*::/                                                           contains=luaLabelD4
syn match   luaLabel5    contained                          /::\K\k*::/                                                           contains=luaLabelD5
syn match   luaLabelD0   contained                  /:/
syn match   luaLabelD1   contained                  /:/
syn match   luaLabelD2   contained                  /:/
syn match   luaLabelD3   contained                  /:/
syn match   luaLabelD4   contained                  /:/
syn match   luaLabelD5   contained                  /:/
syn keyword luaStmt0                              break return
syn keyword luaStmt1     contained                          break return
syn keyword luaStmt2     contained                          break return
syn keyword luaStmt3     contained                          break return
syn keyword luaStmt4     contained                          break return
syn keyword luaStmt5     contained                          break return

hi def link luaBuiltin0    Special
hi def link luaBuiltin1    Special
hi def link luaBuiltin2    Special
hi def link luaBuiltin3    Special
hi def link luaBuiltin4    Special
hi def link luaBuiltin5    Special
hi def link luaShebang     Special
hi def link luaCommentA0   Comment
hi def link luaCommentA1   Comment
hi def link luaCommentA2   Comment
hi def link luaCommentA3   Comment
hi def link luaCommentA4   Comment
hi def link luaCommentA5   Comment
hi def link luaCommentB0   Comment
hi def link luaCommentB1   Comment
hi def link luaCommentB2   Comment
hi def link luaCommentB3   Comment
hi def link luaCommentB4   Comment
hi def link luaCommentB5   Comment
hi def link luaCommentC0   Comment
hi def link luaCommentC1   Comment
hi def link luaCommentC2   Comment
hi def link luaCommentC3   Comment
hi def link luaCommentC4   Comment
hi def link luaCommentC5   Comment
hi def link luaTodo        Todo
hi def link luaConstant0   Constant
hi def link luaConstant1   Constant
hi def link luaConstant2   Constant
hi def link luaConstant3   Constant
hi def link luaConstant4   Constant
hi def link luaConstant5   Constant
hi def link luaEllipsis0   Special
hi def link luaEllipsis1   Special
hi def link luaEllipsis2   Special
hi def link luaEllipsis3   Special
hi def link luaEllipsis4   Special
hi def link luaEllipsis5   Special
hi def link luaError0      Error
hi def link luaError1      Error
hi def link luaError2      Error
hi def link luaError3      Error
hi def link luaError4      Error
hi def link luaError5      Error
hi def link luaNumber0     Number
hi def link luaNumber1     Number
hi def link luaNumber2     Number
hi def link luaNumber3     Number
hi def link luaNumber4     Number
hi def link luaNumber5     Number
hi def link luaString0     String
hi def link luaString1     String
hi def link luaString2     String
hi def link luaString3     String
hi def link luaString4     String
hi def link luaString5     String
hi def link luaEscape      SpecialChar

hi def link luaBinop0      luaD0
hi def link luaBinop1      luaD1
hi def link luaBinop2      luaD2
hi def link luaBinop3      luaD3
hi def link luaBinop4      luaD4
hi def link luaBinop5      luaD5
hi def link luaComma0      luaD0
hi def link luaComma1      luaD1
hi def link luaComma2      luaD2
hi def link luaComma3      luaD3
hi def link luaComma4      luaD4
hi def link luaComma5      luaD5
hi def link luaDot0        luaD0
hi def link luaDot1        luaD1
hi def link luaDot2        luaD2
hi def link luaDot3        luaD3
hi def link luaDot4        luaD4
hi def link luaDot5        luaD5
hi def link luaElse0       luaD0
hi def link luaElse1       luaD1
hi def link luaElse2       luaD2
hi def link luaElse3       luaD3
hi def link luaElse4       luaD4
hi def link luaElse5       luaD5
hi def link luaIn0         luaD0
hi def link luaIn1         luaD1
hi def link luaIn2         luaD2
hi def link luaIn3         luaD3
hi def link luaIn4         luaD4
hi def link luaIn5         luaD5
hi def link luaKwd0        luaD0
hi def link luaKwd1        luaD1
hi def link luaKwd2        luaD2
hi def link luaKwd3        luaD3
hi def link luaKwd4        luaD4
hi def link luaKwd5        luaD5
hi def link luaLabelD0     luaD0
hi def link luaLabelD1     luaD1
hi def link luaLabelD2     luaD2
hi def link luaLabelD3     luaD3
hi def link luaLabelD4     luaD4
hi def link luaLabelD5     luaD5
hi def link luaOperator0   luaD0
hi def link luaOperator1   luaD1
hi def link luaOperator2   luaD2
hi def link luaOperator3   luaD3
hi def link luaOperator4   luaD4
hi def link luaOperator5   luaD5
hi def link luaSemi0       luaD0
hi def link luaSemi1       luaD1
hi def link luaSemi2       luaD2
hi def link luaSemi3       luaD3
hi def link luaSemi4       luaD4
hi def link luaSemi5       luaD5
hi def link luaStmt0       luaD0
hi def link luaStmt1       luaD1
hi def link luaStmt2       luaD2
hi def link luaStmt3       luaD3
hi def link luaStmt4       luaD4
hi def link luaStmt5       luaD5
hi def link luaTableEq0    luaD0
hi def link luaTableEq1    luaD1
hi def link luaTableEq2    luaD2
hi def link luaTableEq3    luaD3
hi def link luaTableEq4    luaD4
hi def link luaTableEq5    luaD5
hi def link luaUnop0       luaD0
hi def link luaUnop1       luaD1
hi def link luaUnop2       luaD2
hi def link luaUnop3       luaD3
hi def link luaUnop4       luaD4
hi def link luaUnop5       luaD5

hi def link luaArg0        luaT0
hi def link luaArg1        luaT1
hi def link luaArg2        luaT2
hi def link luaArg3        luaT3
hi def link luaArg4        luaT4
hi def link luaArg5        luaT5
hi def link luaDelim0      luaT0
hi def link luaDelim1      luaT1
hi def link luaDelim2      luaT2
hi def link luaDelim3      luaT3
hi def link luaDelim4      luaT4
hi def link luaDelim5      luaT5
hi def link luaDo0         luaT0
hi def link luaDo1         luaT1
hi def link luaDo2         luaT2
hi def link luaDo3         luaT3
hi def link luaDo4         luaT4
hi def link luaDo5         luaT5
hi def link luaFuncId0     luaT0
hi def link luaFuncId1     luaT1
hi def link luaFuncId2     luaT2
hi def link luaFuncId3     luaT3
hi def link luaFuncId4     luaT4
hi def link luaFuncId5     luaT5
hi def link luaFunc0       luaT0
hi def link luaFunc1       luaT1
hi def link luaFunc2       luaT2
hi def link luaFunc3       luaT3
hi def link luaFunc4       luaT4
hi def link luaFunc5       luaT5
hi def link luaGotoL0      luaT0
hi def link luaGotoL1      luaT1
hi def link luaGotoL2      luaT2
hi def link luaGotoL3      luaT3
hi def link luaGotoL4      luaT4
hi def link luaGotoL5      luaT5
hi def link luaIfBody0     luaT0
hi def link luaIfBody1     luaT1
hi def link luaIfBody2     luaT2
hi def link luaIfBody3     luaT3
hi def link luaIfBody4     luaT4
hi def link luaIfBody5     luaT5
hi def link luaIf0         luaT0
hi def link luaIf1         luaT1
hi def link luaIf2         luaT2
hi def link luaIf3         luaT3
hi def link luaIf4         luaT4
hi def link luaIf5         luaT5
hi def link luaLabel0      luaT0
hi def link luaLabel1      luaT1
hi def link luaLabel2      luaT2
hi def link luaLabel3      luaT3
hi def link luaLabel4      luaT4
hi def link luaLabel5      luaT5
hi def link luaSuffix0     luaT0
hi def link luaSuffix1     luaT1
hi def link luaSuffix2     luaT2
hi def link luaSuffix3     luaT3
hi def link luaSuffix4     luaT4
hi def link luaSuffix5     luaT5
hi def link luaTableKey0   luaT0
hi def link luaTableKey1   luaT1
hi def link luaTableKey2   luaT2
hi def link luaTableKey3   luaT3
hi def link luaTableKey4   luaT4
hi def link luaTableKey5   luaT5
hi def link luaWord0       luaT0
hi def link luaWord1       luaT1
hi def link luaWord2       luaT2
hi def link luaWord3       luaT3
hi def link luaWord4       luaT4
hi def link luaWord5       luaT5

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
