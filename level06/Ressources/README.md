Level 6

Le programme nous demande un login & mot de passe.

Il va hasher le login et le comparer a notre mot de passe.

Notre objectif est d'aller recuperer la valeur lors de la comparaison au moment ou elle se fait : ```=> 0x08048866 <+286>:   cmp    -0x10(%ebp),%eax```

Notre probleme c'est qu'un call de ptrace est fait et fin le programme. Il faut donc avec gdb mettre ub breakpoint avant ptrace et jump apres le retour de celui-ci : 
```
   0x080487b5 <+109>:   call   0x80485f0 <ptrace@plt>
   0x080487ba <+114>:   cmp    $0xffffffff,%eax
   0x080487bd <+117>:   jne    0x80487ed <auth+165>
   0x080487bf <+119>:   movl   $0x8048a68,(%esp)
   0x080487c6 <+126>:   call   0x8048590 <puts@plt>
   0x080487cb <+131>:   movl   $0x8048a8c,(%esp)
   0x080487d2 <+138>:   call   0x8048590 <puts@plt>
   0x080487d7 <+143>:   movl   $0x8048ab0,(%esp)
   0x080487de <+150>:   call   0x8048590 <puts@plt>
   0x080487e3 <+155>:   mov    $0x1,%eax
   0x080487e8 <+160>:   jmp    0x8048877 <auth+303>
   0x080487ed <+165>:   mov    0x8(%ebp),%eax
```

```
gdb ./level06
(gdb) b *0x080487b5
Breakpoint 1 at 0x80487b5
(gdb) b *0x08048866
Breakpoint 2 at 0x8048866
(gdb) r
Starting program: /home/users/level06/level06
***********************************
*               level06           *
***********************************
-> Enter Login: viporten
***********************************
***** NEW ACCOUNT DETECTED ********
***********************************
-> Enter Serial: t

Breakpoint 1, 0x080487b5 in auth ()
(gdb) jump *0x080487ed
Continuing at 0x80487ed.

Breakpoint 2, 0x08048866 in auth ()
(gdb) p *(int *)($ebp - 0x10)
$1 = 6234504
```

Resultat :
```
level06@OverRide:~$ ./level06 
***********************************
*               level06           *
***********************************
-> Enter Login: viporten
***********************************
***** NEW ACCOUNT DETECTED ********
***********************************
-> Enter Serial: 6234504
Authenticated!
$ whoami
level07
$ cat /home/users/level07/.pass
GbcPDRgsFK77LNnnuh7QyFYA2942Gp8yKj9KrWD8
```