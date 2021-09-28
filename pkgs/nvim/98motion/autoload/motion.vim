function motion#preserve(...)
	try
		let view = winsaveview()
		let search = getreg('/')
		let val = v:null
		for Fn in a:000
			if type(Fn) == v:t_func
				let val = Fn()
			elseif type(Fn) == v:t_string
				let val = execute(Fn)
			else
				throw 'invalid value'
			endif
		endfor
	finally
		call winrestview(view)
		call setreg('/', search)
	endtry
	return val
endfun

let s:EMPTY = 9999999

func motion#get_indent(ln)
	let [st, en] = motion#preserve('normal! '.a:ln.'G^', {->[virtcol('.'), virtcol('$')]})
	if st == en
		return s:EMPTY
	else
		return st
	endif
endfun

func motion#find_indent(start, end)
	let depth = v:count1
	let sline = line('.')
	let ind = s:EMPTY
	while sline > 0
		let ind2 = motion#get_indent(sline)
		if ind2 < ind
			let ind = ind2
			let depth = depth-1
		endif
		if depth == -1 || ind == 1
			break
		endif
		let sline = sline - 1
	endwhile

	let eline = line('.')
	let lastline = line('$')
	while eline < lastline && motion#get_indent(eline+1) > ind
		let eline = eline + 1
	endwhile

	if a:start
		while sline > 0 && motion#get_indent(sline-1) == s:EMPTY
			let sline = sline - 1
		endwhile
	elseif motion#get_indent(line('.')) != 1
		let sline = sline + 1
	endif

	if a:end
		let eline = eline + 1
	else
		while eline > sline && motion#get_indent(eline) == s:EMPTY
			let eline = eline - 1
		endwhile
	endif

	return ['V',
\		[bufnr(), eline, s:EMPTY],
\		[bufnr(), sline, 0]
\	]
endfun

func motion#select_ai()
	return motion#find_indent(v:true, v:false)
endfunc

func motion#select_ii()
	return motion#find_indent(v:false, v:false)
endfunc

func motion#select_aI()
	return motion#find_indent(v:true, v:true)
endfunc
