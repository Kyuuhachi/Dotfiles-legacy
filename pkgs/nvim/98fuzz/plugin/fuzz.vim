let g:fuzz_action = {
\	'ctrl-t': 'tab split',
\	'ctrl-x': 'split',
\	'ctrl-v': 'vsplit',
\}

function! Run(cmd)
	let cmd = a:cmd
	if has_key(cmd, 'sink**')
		if !has_key(cmd, 'action')
			let cmd.action = g:fuzz_action
		endif
		function cmd.sink(lines)
			let act = remove(a:lines, 0)
			let act = empty(act) ? "" : self.action[act]
			call self['sink**'](act, a:lines)
		endfun
		let cmd['sink*'] = remove(cmd, 'sink')
		call extend(cmd.options, ['--expect', join(keys(cmd.action), ',')])
	endif
	call fzf#run(fzf#wrap(cmd))
endfun


" {{{1 Files

" Those git stuffs won't really work
function! FuzzyFiles()
	call Run({
	\	'source': 'zsh -c ' . shellescape(
	\		 'if git rev-parse --is-inside-work-tree >/dev/null && ! git check-ignore . >/dev/null ; then '
	\		.'git ls-files --cached --others --exclude-standard; '
	\		.'else find \( \! -name "." -name ".*" -prune \) -o -type f,l -print | cut -c3-; fi '
	\		.'| cf'),
	\	'options': [
	\		'--tiebreak', 'length',
	\		'--ansi',
	\		'--multi',
	\		'--preview', 'view {}',
	\		'--preview-window', 'right:40%',
	\		'--prompt', 'File>'
	\	],
	\})
endfun
function! FuzzyAllFiles()
	call Run({
	\	'source': 'zsh -c ' . shellescape('find \! -name "." -type f,l -print | tail -n+2 | grep -v -e ''/\.git/'' -e ''/\.stack-work/'' | cut -c3- | cf'),
	\	'options': [
	\		'--tiebreak', 'length',
	\		'--ansi',
	\		'--multi',
	\		'--preview', 'view {}',
	\		'--preview-window', 'right:40%',
	\		'--prompt', 'File>'
	\	],
	\})
endfun

" {{{1 Buffers

function! Bufopen(method, lines)
	echom string([a:method]) string(a:lines)
	return
	if len(a:lines) < 2
		return
	endif
	let b = matchstr(a:lines[1], '\[\zs[0-9]*\ze\]')
	let cmd = s:action_for(a:lines[0])
	if !empty(cmd)
		execute 'silent' cmd
	endif
	execute 'buffer' b
endfunction

function! FormatBuffer(b)
	let name = bufname(a:b)
	let name = empty(name) ? '[No Name]' : fnamemodify(name, ":p:~:.")

	let line = getbufinfo(a:b)[0]['lnum']

	let flag = a:b == bufnr('')  ? " \x1B[34m%\x1B[m" :
	\          a:b == bufnr('#') ? " \x1B[35m#\x1B[m" :
	\                              '   '
	let modified = !getbufvar(a:b, '&modified')  ? '' : " \x1B[32m[+]\x1B[m"
	let readonly = getbufvar(a:b, '&modifiable') ? '' : " \x1B[31m[RO]\x1B[m"
	let extra = join([modified, readonly], '')

	return a:b . "\x1E" . printf("[\x1B[33m%d\x1B[m]", a:b) . flag . "\t" . name . extra
endfunction

function! BufListedSorted()
	return sort(BufListed(), {a, b -> get(g:fuzzy_buffers, a, 0) < get(g:fuzzy_buffers, b, 0) ? 1 : -1})
endfunction

function! BufListed()
	return filter(range(1, bufnr('$')), {_, v -> buflisted(v) && getbufvar(v, "&filetype") != "qf"})
endfunction

function! FuzzyBuffers()
	call Run({
	\	'source': map(BufListedSorted(), {_, v -> FormatBuffer(v)}),
	\	'sink**': funcref('Bufopen'),
	\	'options': [
	\		'--tiebreak', 'index',
	\		'--ansi',
	\		'--prompt', 'Buf>',
	\		'--delimiter', "\x1E",
	\		'--nth', '1',
	\		'--with-nth', '2',
	\		'--multi',
	\		'--header-lines', '1',
	\	],
	\})
endfun

let g:fuzzy_buffers = {}
augroup fuzzy_buffers
	autocmd!
	autocmd BufWinEnter,WinEnter * let g:fuzzy_buffers[bufnr('')] = reltimefloat(reltime())
	autocmd BufWinEnter,WinEnter * let g:fuzzy_buffers[bufnr('')] = localtime()
	autocmd BufDelete            * silent call remove(g:fuzzy_buffers, bufnr(''))
augroup END

" }}}1
nnoremap <silent> ,f :call FuzzyFiles()<CR>
nnoremap <silent> ,F :call FuzzyAllFiles()<CR>
nnoremap <silent> ,B :call FuzzyBuffers()<CR>
