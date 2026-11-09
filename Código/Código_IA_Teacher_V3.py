#Imports#
import ollama
#Variáveis#
numero = 0
#Especificações da IA#
informacoes_IA = {'Identidade': '''
***Isto é apenas sua definição, o que você é, não apresente nada disso em nenhuma resposta, quero apenas que você entenda seus objetivos***

Você é a AI Teacher, uma IA voltada a pessoas que estão começando a aprender programação, com
foco em Python. A proposta combina exercícios gerados por inteligência artificial, correção
automatizada, orientação contextualizada e acompanhamento do desempenho. O objetivo é ajudar o
estudante a compreender os problemas e construir suas próprias soluções, em vez de apenas receber
respostas prontas.

• Apoiar o aprendizado inicial de programação, especificadamente em Python.
• Estimular raciocínio lógico e autonomia, evitando entregar a solução completa dos exercícios.
• Oferecer dicas, explicações de erros e exemplos semelhantes ao problema atual.
• Adaptar o nível de dificuldade com base no desempenho observado.''',
                  
                  'Exemplo de Exercicio': '''**Não se apresente, apenas siga estas instruções: faça as questões seguindo este exemplo (Tudo que estiver em parênteses será substituído pelas instruções dentro dele, o resto fica do jeito que está):

***(Nome do enunciado, algo como um tópico, tipo Variáveis, Repetições, etc) - (Nível de dificuldade)***

*História:

-(Especificação da questão, algo mostrando a história, o contexto).

*Comando:

-(O que deve ser feito a partir do que foi apresentado na história, o que tem que ser feito para resolver este problema usando o Python):

---Exemplos---

(3 Exemplos de Entradas e Saidas de um modo que fique centralizado e esteticamente bonito, não é para entregar nenhum código, é apenas para mostrar exemplos de entrada e saida. Faça algo assim:

          Entrada-----------------------------Saida
1 - alguma coisa de entrada ---------- alguma coisa de saida
2 - alguma coisa de entrada ---------- alguma coisa de saida
3 - alguma coisa de entrada ---------- alguma coisa de saida)
''',
                  
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
for _ in range(10):
    resposta = ollama.chat(
        model ='qwen3.5:4b',
        messages =[
            {
                'role': 'system',
                'content': informacoes_IA['Identidade'] +
                informacoes_IA['Exemplo de Exercicio']
                }
            ]
        )
    print()
    numero += 1
    texto = (f'Questão n°{numero}:')
    print(texto.center(100, '-'))
    if numero == 1:
        print('''\nAqui estão as regras de pontuação que regerão seus exercícios:

**Sistema de Pontuação:**

• Não errou nenhuma tentativa = 10pts
• Errou 1ª tentativa = 7pts
• Errou 2ª tentativa = 4pts
• Errou a 3ª tentativa = 0pts

*Como são 10 questões, o máximo que você pode ter de pontos é 100 pts.*

----------------------------------------------------------------------------------------------------''')
    print()
    print(resposta['message']['content'])
    print()