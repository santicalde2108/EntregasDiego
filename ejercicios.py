numeros = {1, 2, 2, 3, 4, 4}
print("Set inicial:", numeros)

print("Los repetidos se eliminan automáticamente.")

numeros.add(5)
numeros.add(6)
print("Después de agregar 5 y 6:", numeros)

numeros.remove(2)
print("Después de eliminar el 2:", numeros)

print("¿Está el número 3?", 3 in numeros)

set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

print("Set A:", set_a)
print("Set B:", set_b)
print("Unión:", set_a | set_b)
print("Intersección:", set_a & set_b)
print("Diferencia de A:", set_a - set_b)
