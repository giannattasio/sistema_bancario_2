def menu():
    menu = """\n
    ================ MENU ================
    [d]   Depositar
    [s]   Sacar
    [e]   Extrato
    [nvc] Nova conta
    [c]   Listar contas
    [nvu] Novo usuário
    [q]   Sair
    => """
    return input(menu)


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n== Depósito realizado! ==")
    else:
        print("\n Operação falhou! Por favor, informe um valor valido.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques > limite_saques

    if excedeu_saldo:
        print("\n Saldo insuficiente!. ")

    elif excedeu_limite:
        print("\n O valor do saque excede o limite. Tente novamente! ")

    elif excedeu_saques:
        print("\n Número máximo de saques diarios excedido. "
              "Tente novamente amanha!")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = int(input("Informe o CPF (somente número): "))
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n CPF já existente! ")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço "
                     "(logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,
                     "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios
                          if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = int(input("Informe o CPF do usuário: "))
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta,
                "usuario": usuario}

    print("\n@@@ Usuário não encontrado, "
          "fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print((linha))


def listar_usuarios(usuarios):
    for usuario in usuarios:
        linha = f"""\
            Nome:\t{usuario['nome']}
            Cpf:\t{usuario['cpf']}
        """
        print("=" * 100)
        print((linha))


def main():
    mock_user = {
        "nome": "admin",
        "data_nascimento": "10/10/2010",
        "cpf": 12345678,
        "endereco": "rua dos arvoredos"}
    LIMITE_SAQUES = 2
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = [mock_user]
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            numero_saques += 1
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nvu":
            criar_usuario(usuarios)

        elif opcao == "nvc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "c":
            listar_contas(contas)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, "
                  "por favor selecione novamente a operação desejada.")


main()
