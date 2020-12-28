if exists("b:did_indent")
	finish
endif
let b:did_indent = 1

setlocal indentexpr=LilypondIndent()

setlocal lw+=define-public,define*-public
setlocal lw+=define*,lambda*,let-keywords*
setlocal lw+=defmacro,defmacro*,define-macro
setlocal lw+=defmacro-public,defmacro*-public
setlocal lw+=use-modules,define-module
setlocal lw+=define-method,define-class

setlocal lw+=define-markup-command,define-markup-list-command
setlocal lw+=define-safe-public,define-music-function
setlocal lw+=def-grace-function

setlocal lw+=match-let,match
setlocal lw+=define-scheme-function,interpret-markup

setlocal lw-=if
setlocal lw-=set!
