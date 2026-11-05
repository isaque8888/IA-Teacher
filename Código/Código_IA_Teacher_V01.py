#Mensagens iniciais#
print(100*'-')
print()
mensagem = 'Seja bem vindo à IA Teacher!'
print(mensagem.center(100,'-'))
print()
print('**Selecione 1 para proseguir e 2 para sair do programa:')
print()
print('1) Iniciar diagnostico.')
print('2) Encerrar programa.')
print()
resp = input('Digite aqui: ')
print()

while resp not in ('1', '2'):
    print('***Erro, caractere não encontrado, digite 1 ou 2***')
    resp = input('Digite aqui: ')
    print()

if resp == '2':
    programa_encerrado = 'Programa encerrado'
    print(programa_encerrado.center(100, '-'))
    exit()
#Fim das mensagens iniciais#


    