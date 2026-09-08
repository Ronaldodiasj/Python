def porcentagem(a, b):
    return f"{a} % {b} = {a * b / 100}"

a = input("Digite o primeiro número: ")
b = input("Digite o segundo número: ")
print(porcentagem(int(a), int(b)))