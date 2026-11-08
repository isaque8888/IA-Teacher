#Imports#
import ollama
#Especificações da IA#
informacoes_IA = {'Identidade': '',
                  'Diagnostico': '',
                  'Dificuldade Iniciante': '',
                  'Dificuldade Intermediario': '',
                  'Dificuldade Avancada': ''
                  }
#Mensagens iniciais#
print(100*'-')
print()
mensagem = 'Seja bem vindo à IA Teacher!'
print(mensagem.center(100,'-'))
print('\n**Selecione 1 para proseguir e 2 para sair do programa:')
print('\n1) Iniciar diagnostico.')
print('2) Encerrar programa.')
resp = input('\nDigite aqui: ')

while resp not in ('1', '2'):
    print('\n***Erro, caractere não encontrado, digite 1 ou 2***')
    resp = input('\nDigite aqui: ')

if resp == '2':
    print()
    programa_encerrado = 'Programa encerrado'
    print(programa_encerrado.center(100, '-'))
    exit()
#Configuração da IA + Diagnostico#
resposta = ollama.chat(
    model ='qwen3.5:4b',
    messages =[
        {
            'role': 'system',
            'content': informacoes_IA['Identidade']
            }
        ]
    )
print('\nResposta da IA:')
print()
print(resposta['message']['content'])