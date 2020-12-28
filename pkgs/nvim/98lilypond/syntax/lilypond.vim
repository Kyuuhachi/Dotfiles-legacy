if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

setlocal mps+=<:>

syn case match
syn sync maxlines=100


source <sfile>:p:h/lilypond_gen.vim

hi def link lilyError            Error

hi def link lilyCustomFunction   Identifier
hi def link lilyBuiltin          PreProc
hi def link lilyMusicCommand     Function
hi def link lilyDeclaration      lilyMusicCommand
hi def link lilyGrace            lilyMusicCommand
hi def link lilyArticulation     lilyMusicCommand
hi def link lilyScript           lilyMusicCommand
hi def link lilyDynamic          lilyMusicCommand
hi def link lilySpanner          lilyMusicCommand
hi def link lilyProperty         lilyMusicCommand
hi def link lilyScale            lilyMusicCommand
hi def link lilyMarkupFunction   lilyMusicCommand

hi def link lilyDuration         Number
hi def link lilyRDuration        lilyDuration
hi def link lilyDurationMul      lilyDuration
hi def link lilyNumber           Number
hi def link lilyString           String
hi def link lilyComment          Comment

hi def link lilyPitch            Operator
hi def link lilyRest             Operator
hi def link lilySymbol           Special
hi def link lilyLyric            Normal
hi def link lilyChordname        Normal
hi def link lilyDrum             lilyPitch
hi def link lilyChord            Special
hi def link lilyChordRepeat      Special
hi def link lilyFigure           Special

hi def link lilyLyricHyphen      Operator
hi def link lilyLyricExtender    Operator

hi def link lilyVar              Identifier

hi def link lilyLayout           Statement
hi def link lilyMarkup           Statement
hi def link lilyNotemode         Statement
hi def link lilyLyricmode        Statement
hi def link lilyChordmode        Statement
hi def link lilyDrummode         Statement
hi def link lilyFiguremode       Statement
hi def link lilyHeader           Statement
hi def link lilyPaper            Statement
hi def link lilyMidi             Statement
hi def link lilyContextMod       Statement
hi def link lilyWith             Statement

hi def link lilyScheme           PreProc
hi def link lilySchemeLilyStart  PreProc

hi def link lilySchemeChar Character
hi def link lilySchemeComment Comment
hi def link lilySchemeBoolean Boolean
hi def link lilySchemeString String
hi def link lilySchemeKeyword Constant
hi def link lilySchemeExtSymbol Constant
hi def link lilySchemeArray Constant
hi def link lilySchemeArrayElt Constant
hi def link lilySchemeNumber Number

hi def link lilySchemeQuote0 lilySchemeDelimiter0
hi def link lilySchemeQuote1 lilySchemeDelimiter1
hi def link lilySchemeQuote2 lilySchemeDelimiter2
hi def link lilySchemeQuote3 lilySchemeDelimiter3
hi def link lilySchemeQuote4 lilySchemeDelimiter4
hi def link lilySchemeQuote5 lilySchemeDelimiter5
hi def link lilySchemeUnquote0 lilySchemeDelimiter0
hi def link lilySchemeUnquote1 lilySchemeDelimiter1
hi def link lilySchemeUnquote2 lilySchemeDelimiter2
hi def link lilySchemeUnquote3 lilySchemeDelimiter3
hi def link lilySchemeUnquote4 lilySchemeDelimiter4
hi def link lilySchemeUnquote5 lilySchemeDelimiter5
hi def link lilySchemeQuoted0 lilySchemeStruc0
hi def link lilySchemeQuoted1 lilySchemeStruc1
hi def link lilySchemeQuoted2 lilySchemeStruc2
hi def link lilySchemeQuoted3 lilySchemeStruc3
hi def link lilySchemeQuoted4 lilySchemeStruc4
hi def link lilySchemeQuoted5 lilySchemeStruc5
hi def lilySchemeStruc0 ctermfg=224
hi def lilySchemeStruc1 ctermfg=230
hi def lilySchemeStruc2 ctermfg=194
hi def lilySchemeStruc3 ctermfg=195
hi def lilySchemeStruc4 ctermfg=189
hi def lilySchemeStruc5 ctermfg=225
hi def lilySchemeDelimiter0 ctermfg=203
hi def lilySchemeDelimiter1 ctermfg=220
hi def lilySchemeDelimiter2 ctermfg=083
hi def lilySchemeDelimiter3 ctermfg=087
hi def lilySchemeDelimiter4 ctermfg=075
hi def lilySchemeDelimiter5 ctermfg=213

hi def link lilySchemeVar Identifier
hi def link lilySchemeFunc Function
hi def link lilySchemeMacro Statement

let b:current_syntax = "lilypond"
