let s:dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

function! s:TexSync()
	if !exists('b:vimtex') | return | end
	let l:pdffile = b:vimtex['viewer']['out']()
	let l:cursorpos = getcurpos()
	call jobstart(["python3", s:dir.'/v2e.py', l:pdffile, l:cursorpos[1], l:cursorpos[2], expand("%:p")])
endfunction
command! TexSync call s:TexSync()


if exists('g:evinceSyncDaemonJob')
	silent! call jobstop(g:evinceSyncDaemonJob)
	silent! call jobwait(g:evinceSyncDaemonJob)
end

let g:evinceSyncDaemonJob = jobstart(["python3", s:dir."/e2v.py", "SyncTexGoto"], { "rpc": v:true })
