print("Ficha de cadastro de usuário")
nome = input("Digite seu nome completo: ").upper()
idade = input("Digite sua idade: ").upper()
cidade = input("Digite sua cidade: ").upper()
with open("Cadastro do(a) "+nome+".txt", "w") as arquivo:
    arquivo.write(f"Nome: {nome}\n")
    arquivo.write(f"Idade: {idade}\n")
    arquivo.write(f"Cidade: {cidade}\n")
