loadplugins '\.(js|penta)$'
group user

set titlestring=
set hlfind
set urlsep='\|'
set showtabline=multitab
set showstatuslinks=

nmap gp -ex pin!
nmap -builtin <C-L> -ex nohl
nmap -javascript y dactyl.clipboardWrite(decodeURIComponent(buffer.uri.spec), true)

nmap -count h -builtin <count>h<count>h<count>h<count>h
nmap -count j -builtin <count>j<count>j<count>j<count>j
nmap -count k -builtin <count>k<count>k<count>k<count>k
nmap -count l -builtin <count>l<count>l<count>l<count>l
nmap -count <C-S-A> ]]
nmap -count <C-S-X> [[

nmap -builtin <Left> <Pass>
nmap -builtin <Right> <Pass>
nmap -builtin <Up> <Pass>
nmap -builtin <Down> <Pass>
nmap -builtin <Space> <Pass>
nmap -builtin <CR> <Pass>
nmap -builtin <PageUp> <Pass>
nmap -builtin <PageDown> <Pass>

js <<EOF
function ffncopy() {
	urls=[];
	for(let tab of tabs.visibleTabs) {
		tabs.select(tab);
		if(buffer.URL.host == "www.fanfiction.net" && buffer.URL.path.startsWith("/s/"))
			urls.push(buffer.URL.path.split("/")[2]);
	}
	dactyl.echo(urls.join(" "))
}
EOF
command! -js ffncopy ffncopy()
command! rc source ~/.pentadactylrc

Imap -builtin <C-`> <Pass>
Imap -builtin <C-1> <Pass>
Imap -builtin <C-2> <Pass>
Imap -builtin <C-3> <Pass>
Imap -builtin <C-4> <Pass>
Imap -builtin <C-5> <Pass>
Imap -builtin <C-6> <Pass>
Imap -builtin <C-7> <Pass>
Imap -builtin <C-8> <Pass>
Imap -builtin <C-9> <Pass>
Imap -builtin <C-0> <Pass>
Imap -builtin <C--> <Pass>
Imap -builtin <C-=> <Pass>

Imap -builtin <C-q> <Pass>
" Imap -builtin <C-w> <Pass>
Imap -builtin <C-e> <Pass>
Imap -builtin <C-r> <Pass>
Imap -builtin <C-t> <Pass>
Imap -builtin <C-y> <Pass>
Imap -builtin <C-u> <Pass>
Imap -builtin <C-i> <Pass>
Imap -builtin <C-o> <Pass>
Imap -builtin <C-p> <Pass>
Imap -builtin <C-[> <Pass>
Imap -builtin <C-]> <Pass>

Imap -builtin <C-a> <Pass>
Imap -builtin <C-s> <Pass>
Imap -builtin <C-d> <Pass>
Imap -builtin <C-f> <Pass>
Imap -builtin <C-g> <Pass>
Imap -builtin <C-h> <Pass>
Imap -builtin <C-j> <Pass>
Imap -builtin <C-k> <Pass>
Imap -builtin <C-l> <Pass>
Imap -builtin <C-;> <Pass>
" Imap -builtin <C-'> <Pass>
Imap -builtin <C-\> <Pass>

Imap -builtin <C-z> <Pass>
Imap -builtin <C-x> <Pass>
Imap -builtin <C-c> <Pass>
Imap -builtin <C-v> <Pass>
Imap -builtin <C-b> <Pass>
Imap -builtin <C-n> <Pass>
Imap -builtin <C-m> <Pass>
Imap -builtin <C-,> <Pass>
Imap -builtin <C-.> <Pass>
Imap -builtin <C-/> <Pass>

" vim: ft=vim
