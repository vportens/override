Level 3

Dans la fonction decrypt nous avons une comparaisons avec cette string :
str = "Q}|u`sfg~sf{}|a3"
(apres conversion en hex)
tmp[17]

for (int i = 0; i <= 21; i++) {
    tmp = "";
    for (int j = 0; j < 17; j++) {
        tmp[j] = str[j] ^ i;
    }
    if (strncmp("Congratulations!", tmp, 16) == 0) {
        printf("Found! The passzord is %d\n", 322424845 - i);
        break;
    }

}

Ici 2 solutions :

1 - essayer les 21 possibilte une a une ( 322424845 - i ) avec i [0-21];

2 - faire un programme pour reverse le decrypte et trouver directement la solution unique 

ici le password c'est Password:322424827

