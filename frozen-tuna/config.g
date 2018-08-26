start: "\n"* (line "\n"+)* line?
line: cond "->" command -> plaincmd
    | cond "=>" shcommand -> shcmd

?cond: cond_or
?cond_or: cond_and ("|" cond_and)*
?cond_and: cond_base ("&" cond_base)*
?cond_base: "(" cond ")"
          | WORD "/" WORD -> cond_mime
          | WORD "/" "*" -> cond_mime2
          | "=" WORD -> cond_parent
          | "@" WORD -> cond_icon
          | WORD ":" -> cond_scheme
          | HOST -> cond_host
          | "else" -> cond_else

WORD: ("a".."z"|"0".."9"|"-")+
HOST: WORD ("." WORD)+
CMDWORD: /\S+/

command: CMDWORD+
shcommand: /\S.*/

%ignore ("\t"|" "|"\f"|"\r")+
%ignore "\\" "\n"
%ignore /#[^\n]*/

