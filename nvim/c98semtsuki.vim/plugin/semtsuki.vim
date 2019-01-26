 
function s:run_semtsuki()
	echo luaeval('require("semtsuki").run(table.concat(_A, "\n"))', getline(1, '$'))
endfunction

augroup Semtsuki
	au!
	" au BufEnter * call s:run_semtsuki()
	" au VimResized * call s:run_semtsuki()
	" au CursorMoved * call s:run_semtsuki()
	" au CursorMovedI * call s:run_semtsuki()
	" au TextChanged * call s:run_semtsuki()
	" au TextChangedI * call s:run_semtsuki()
augroup END
