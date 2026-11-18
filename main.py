from datetime import datetime
import random

#manipulação do arquivo 
def salvar_arquivo():
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("cofre_dados.txt", "w", encoding="utf-8") as arquivo:
        for cred in credenciais:
        
         arquivo.write(f"Serviço: {cred['servico']} | Usuario: {cred['usuario']} | Senha: {cred['senha']} | Categoria: {cred['categoria']} | Observacoes: {cred['observacoes']} | Atualizado: {cred['data_atualizacao']}\n" )

def carregar_arquivo():
    try:
        with open("cofre_dados.txt", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip([])
                if not linha:
                    continue

                partes = [parte.strip() for parte in linha.split(“|”)]

                credencial = {
                    "servico": partes[0].split(": ", 1)[1],
                    "usuario": partes[1].split(": ", 1)[1],
                    "senha": partes[2].split(": ", 1)[1],
                    "categoria": partes[3].split(": ", 1)[1],
                    "observacoes": partes[4].split(": ", 1)[1],
                    "data_atualizacao": partes[5].split(": ", 1)[1]
                }
                credenciais.append(credencial)
    except FileNotFoundError:
        pass

    
# Registro no arquivo de auditoria
def registrar_log(operacao, servico):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    arquivo = open("auditoria.log", "a", encoding="utf-8")
    arquivo.write(
        f"{data_hora} | Operação: {operacao} | Serviço: {servico}\n"
    )
    arquivo.close()

# Consulta de logs:
def consultar_logs():
    try:
        arquivo = open("auditoria.log", "r", encoding="utf-8")

        print("\n---------- LOG DE AUDITORIA ----------")

        vazio = True
        for linha in arquivo:
            print(linha.strip())
            vazio = False

        if vazio:
            print("Nenhum registro encontrado.")

        arquivo.close()

    except FileNotFoundError:
        print("Nenhum log foi gerado ainda.")


credenciais = []
categorias = [
    "Rede Social", 
    "Banco",
    "E-mail",
    "Lojas virtuais",
    "Plataformas de estudo", 
    "Streaming", 
    "Jogos", 
    "Outros"
]

# Análise de senha
def carregar_senhas_comuns():
    senhas_comuns = []

    try:
        arquivo = open("senhas_comuns.txt", "r")
        for linha in arquivo:
            senhas_comuns.append(linha.strip())
        arquivo.close()
    except:
        print("Arquivo de senhas comuns não encontrado.")
    return senhas_comuns

def verificar_senha_comum(senha):
    senhas_comuns = carregar_senhas_comuns()
    if senha in senhas_comuns:
        return True
    else:
        return False

def analisar_senha(senha, categoria):
    motivos = []

    maiusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    minusculas = "abcdefghijklmnopqrstuvwxyz"
    numeros = "0123456789"
    simbolos = "!@#$%&*()-_+=.;:?"
    
    tem_maiuscula = False
    tem_minuscula = False
    tem_numero = False
    tem_simbolo = False

    for letra in senha:
        if letra in maiusculas:
            tem_maiuscula = True
        elif letra in minusculas:
            tem_minuscula = True
        elif letra in numeros:
            tem_numero = True
        elif letra in simbolos:
            tem_simbolo = True

    if len(senha) >= 8:
        motivos.append("A senha possui pelo menos 8 caracteres.")
    else:
        motivos.append("A senha possui menos de 8 caracteres.")

    if tem_maiuscula:
        motivos.append("A senha possui letras maiúsculas.")
    else:
        motivos.append("A senha não possui letras maiúsculas.")

    if tem_minuscula:
        motivos.append("A senha possui letras minúsculas.")
    else:
        motivos.append("A senha não possui letras minúsculas.")

    if tem_numero:
        motivos.append("A senha possui números.")
    else:
        motivos.append("A senha não possui números.")

    if tem_simbolo:
        motivos.append("A senha possui símbolos especiais.")
    else:
        motivos.append("A senha não possui símbolos especiais.")

    tipos_caracteres = 0

    if tem_maiuscula:
        tipos_caracteres +=1
    if tem_minuscula:
        tipos_caracteres +=1
    if tem_numero:
        tipos_caracteres +=1
    if tem_simbolo:
        tipos_caracteres +=1

    if len(senha) < 8 or tipos_caracteres <=1:
        classificacao = "Fraca"
        motivos.append("A senha não atende aos requisitos mínimos de segurança")
    elif (len(senha) > 8 and tem_maiuscula and tem_minuscula and tem_numero and tem_simbolo):
        classificacao = "Forte"
        motivos.append("A senha atende a todos os critérios de uma senha forte.")
    else: 
        classificacao = "Média"
        motivos.append("A senha atende a alguns critérios de segurança, mas não a todos os requisitos de uma senha forte.")
    

    if verificar_senha_comum(senha):
        classificacao = "Fraca"
        motivos.append("Essa senha está na lista de senhas comuns e, por segurança, foi classificada como fraca")

    return classificacao, motivos

def exibir_analise_senha(senha, categoria):
    classificacao, motivos = analisar_senha(senha, categoria)
    print("\n---------- ANÁLISE DA SENHA ----------")
    print("Categoria:", categoria)
    print("Classificação:", classificacao)
    print("\nMotivos da classificação:")
    for motivo in motivos:
        print("-", motivo)
def gerar_senha_forte():
    maiusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    minusculas = "abcdefghijklmnopqrstuvwxyz"
    numeros = "0123456789"
    simbolos = "!@#$%&*()-_+=.;:?"

    senha = random.choice(maiusculas)
    senha += random.choice(minusculas)
    senha += random.choice(numeros)
    senha += random.choice(simbolos)

    todos_caracteres = maiusculas + minusculas + numeros + simbolos

    for i in range(8):
        senha += random.choice(todos_caracteres)
    senha_lista = list(senha)
    random.shuffle(senha_lista)
    senha = "".join(senha_lista)

    return senha

# Detecção de risco (senha repetida)
def verificar_senha_repetida(credencial_atual):
    servicos_repetidos = []

    for credencial in credenciais:
        if credencial is not credencial_atual and credencial["senha"] == credencial_atual["senha"]:
            servicos_repetidos.append(credencial["servico"])

    if len(servicos_repetidos) > 0:
        print("\n! ALERTA DE RISCO !")
        print("Essa senha também é usada em outros serviços:")
        for servico in servicos_repetidos:
            print("-", servico)
        print("Se um deles vazar, todos os outros ficam expostos. Troque as senhas!")

        # Registrar no log:
        registrar_log("Alerta de senha repetida", credencial_atual["servico"])


# Detecção de risco (todas as senhas repetidas)
def verificar_todas_senhas_repetidas():
    grupos = {}

    for credencial in credenciais:
        senha = credencial["senha"]
        if senha in grupos:
            grupos[senha].append(credencial["servico"])
        else:
            grupos[senha] = [credencial["servico"]]

    print("\n---------- DETECÇÃO DE RISCO ----------")
    encontrou_risco = False

    for senha in grupos:
        if len(grupos[senha]) > 1:
            encontrou_risco = True
            print("\nSenha repetida em", len(grupos[senha]), "serviços:")
            for servico in grupos[senha]:
                print("-", servico)

    if encontrou_risco == False:
        print("Nenhuma senha repetida encontrada.")
    else:
        # Registrar no log:
        registrar_log("Verificação de risco", "! Senhas repetidas encontradas !")


# Cadastro
def cadastrar_credenciais():
    servico = input("Digite o nome do serviço: ")
    usuario = input("Digite o nome do usuário: ")
    print("\n Como deseja criar sua senha?")
    print("1 - Gerar uma senha forte automaticamente")
    print("2 - Digitar minha própria senha")

    opcao_senha = input("Escolha uma opção: ")

    if opcao_senha == "1": 
        senha = gerar_senha_forte()
        print("\nSenha sugerida:", senha)
    elif opcao_senha == "2":
        senha = input("Digite sua senha: ")
    else:
        print("Opção inválida! Cadastro cancelado.")
        return

    
    print("\nCategorias disponíveis:")
    visualizar_categorias()

    categoria = input("Digite a categoria: ")
    observacoes = input("Digite as observações: ")
    
    data_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M")

    nova_credencial = {
        "servico": servico,
        "usuario": usuario,
        "senha": senha,
        "categoria": categoria,
        "observacoes": observacoes,
        "data_atualizacao": data_atualizacao
    }

    credenciais.append(nova_credencial)
    salvar_arquivo()
    print("\nSenha salva com sucesso!")
# Registrar no log:
    registrar_log("Cadastro de credencial", servico)

    print("Cadastro confirmado!")
    exibir_analise_senha(senha, categoria)
    verificar_senha_repetida(nova_credencial)


# Visualização
def visualizar_credenciais():
    if len(credenciais) == 0:
        print("Não existem cadastros.")
    else:
        for credencial in credenciais:

# Registrar no log:
            registrar_log(
                "Visualização de credencial",
                credencial["servico"]
            )
            
            senha_oculta = credencial["senha"][:2] + "*" * max(0, len(credencial["senha"]) - 2)

            print("\n---------- CREDENCIAL ----------")
            print(f"Serviço: {credencial['servico']}")
            print(f"Usuário: {credencial['usuario']}")
            print(f"Senha: {senha_oculta}")
            print(f"Categoria: {credencial['categoria']}")
            print(f"Observações: {credencial['observacoes']}")
            print(f"Último cadastro/alteração: {credencial['data_atualizacao']}")


# Revelar senha
def revelar_senha():
    servico_revelar = input("Digite o nome do serviço: ")
    encontrado = False

    for credencial in credenciais:
        if credencial["servico"] == servico_revelar:
            print("Senha:", credencial["senha"])
            # Registrar no log:
            registrar_log("Revelação de senha", servico_revelar)
            encontrado = True
            break

    if encontrado == False:
        print("Serviço não encontrado.")


# Edição
def editar_credenciais():
    servico_editar = input("Qual serviço deseja editar? ")
    encontrado = False

    for credencial in credenciais:
        if credencial["servico"] == servico_editar:
            nova_senha = input("Qual será a senha nova? ")

            credencial["senha"] = nova_senha
            credencial[“data_atualizacao”] = datetime.now().strftime(“%d/%m/%Y %H:%M”)
            salvar_arquivo()
            # Registrar no log:
            registrar_log("Alteração de senha", servico_editar)
            credencial["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")

            encontrado = True
            print("Senha alterada!")

            exibir_analise_senha(
                nova_senha,
                credencial["categoria"]
            )
            verificar_senha_repetida(credencial)
            break

    if encontrado == False:
        print("Serviço não encontrado.")


# Exclusão
def excluir_credenciais():
    servico_excluir = input("Qual serviço deseja excluir? ")
    encontrado = False

    for credencial in credenciais:
        if credencial["servico"] == servico_excluir:
            credenciais.remove(credencial)
            salvar_arquivo()
            # Registro no log:
            registrar_log("Exclusão de credencial", servico_excluir)
            encontrado = True
            print("Credencial excluída!")
            break

    if encontrado == False:
        print("Serviço não encontrado.")


# Cadastro de categorias
def cadastrar_categoria():
    nome = input("Digite o nome da categoria: ").strip()

    if nome == "":
        print("Nome inválido.")
        return

    for categoria in categorias:
        if categoria.lower() == nome.lower():
            print("Essa categoria já existe.")
            return

    categorias.append(nome)
    # Registro no log:
    registrar_log("Cadastro de categoria", nome)
    print("Categoria cadastrada com sucesso!")
    


# Consulta de categorias
def visualizar_categorias():
    print("\n---------- CATEGORIAS ----------")

    for categoria in categorias:
        print(f"{categoria}")

#relatorio de segurança

def relatorio_seguranca():
    print("\n---------- RELATÓRIO DE SEGURANÇA ----------")

    total = len(credenciais)

    if total == 0:
        print("Nenhuma credencial cadastrada.")
        return

    fortes = 0
    medias = 0
    fracas = 0
    repetidas = 0
    antigas = 0

    senhas_encontradas = []

    for credencial in credenciais:
        senha = credencial["senha"]
        categoria = credencial["categoria"]

        classificacao, motivos = analisar_senha(senha, categoria)

        if classificacao == "Forte":
            fortes += 1
        elif classificacao == "Média":
            medias += 1
        else:
            fracas += 1

        if senha in senhas_encontradas:
            repetidas += 1
        else:
            senhas_encontradas.append(senha)

        data = datetime.strptime(
            credencial["data_atualizacao"],
            "%d/%m/%Y %H:%M"
        )

        dias = (datetime.now() - data).days

        if dias > 90:
            antigas += 1

    porcentagem_fracas = (fracas / total) * 100

    print("Total de credenciais:", total)
    print("Senhas fortes:", fortes)
    print("Senhas médias:", medias)
    print("Senhas fracas:", fracas)
    print("Senhas repetidas:", repetidas)
    print("Senhas com mais de 90 dias:", antigas)
    print(f"Porcentagem de senhas fracas: {porcentagem_fracas:.1f}%")

    print("\n---------- RECOMENDAÇÕES ----------")

    if fracas > 0:
        print("- Melhore as senhas classificadas como fracas.")

    if repetidas > 0:
        print("- Evite utilizar a mesma senha em serviços diferentes.")

    if antigas > 0:
        print("- Revise as senhas que não são alteradas há mais de 90 dias.")

    if fracas == 0 and repetidas == 0 and antigas == 0:
        print("- Nenhum problema identificado pelos critérios do relatório.")

    registrar_log("Consulta de relatório de segurança", "CofreSeguro")


# Perguntar se o usuário deseja continuar
def deseja_continuar():
    while True:
        resposta = input("\nDeseja continuar ou encerrar o programa? (1 - continuar / 2 - encerrar): ").strip()

        if resposta == "1":
            return True
        elif resposta == "2":
            return False
        else:
            print("Opção inválida. Digite 1 para continuar ou 2 para encerrar.")

carregar_arquivo()
# Menu
while True:
    print("\n--------- COFRESEGURO ---------")
    print("1 - Cadastrar Credencial")
    print("2 - Visualizar Credenciais")
    print("3 - Editar Credencial")
    print("4 - Excluir Credencial")
    print("5 - Revelar Senha")
    print("6 - Cadastrar Categoria")
    print("7 - Consultar Categorias")
    print("8 - Consultar Log de Auditoria")
    print("9 - Verificar Senhas Repetidas")
    print("10 - Relatório de Segurança")
    print("11 - Sair")
    opcao = input("Digite a opção: ")

    if opcao == "1":
        cadastrar_credenciais()

    elif opcao == "2":
        visualizar_credenciais()

    elif opcao == "3":
        editar_credenciais()

    elif opcao == "4":
        excluir_credenciais()

    elif opcao == "5":
        revelar_senha()

    elif opcao == "6":
        cadastrar_categoria()

    elif opcao == "7":
        visualizar_categorias()

    elif opcao == "8":
        consultar_logs()

    elif opcao == "9":
        verificar_todas_senhas_repetidas()

    elif opcao == "10":
        relatorio_seguranca()

    elif opcao == "11":
        print("Encerrando o CofreSeguro...")
        break

    else:
        print("Opção inválida!")

    if not deseja_continuar():
        print("Encerrando o CofreSeguro...")
        break
