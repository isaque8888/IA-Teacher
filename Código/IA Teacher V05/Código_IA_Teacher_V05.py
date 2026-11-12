#Imports#
import ollama
import os
#Variáveis#
numero = 0
resp = 0
IA_Atual = 'qwen3.5:4b'
regras = '''\nAqui estão as regras de pontuação que regerão seus exercícios:

**Sistema de Pontuação:**

• Não errou nenhuma tentativa = 10pts
• Errou 1ª tentativa = 7pts
• Errou 2ª tentativa = 4pts
• Errou a 3ª tentativa = 0pts

*Como são 10 questões, o máximo que você pode ter de pontos é 100 pts.*

----------------------------------------------------------------------------------------------------'''
#Especificações da IA#

def dificuldades():

    iniciante = {
        'Conteudo': [
            # 1. Variáveis e Expressões
            'Valores e tipos (int, float, str) e a função type()',
            'Variáveis e atribuição (= é atribuir, == é comparar)',
            'print() para exibir valores',
            'Nomes de variáveis, palavras reservadas e nomes significativos',
            'Comandos (exibição e atribuição) e expressões',
            'Operadores e operandos básicos',

            # 2. Estruturas Condicionais
            'Valores booleanos True/False, que diferenciam maiúsculas de minúsculas',
            'Expressões booleanas e variáveis booleanas',
            'Os 6 operadores de comparação',
            'if simples, if/else e sintaxe',
            'Bloco (suíte) de comandos e indentação',
            'else como cláusula, não como comando',

            # 3. Estruturas de Repetição
            'Conceito de iteração (repetição = laço)',
            'while: fluxograma e sintaxe',
            'for e range(), que começa em 0 e não inclui o final',
            'Uso de _ quando a variável do laço não é usada',

            # 4. Strings
            'String como tipo de dado composto',
            'Indexação a partir de 0 (o índice é um inteiro e retorna uma string de tamanho 1)',
            'len() e o último caractere (len - 1)',
            'Índices negativos',
            'Operadores in e not in',

            # 5. Listas e Tuplas
            'O que é uma lista: elementos ordenados, de qualquer tipo, que podem ser de tipos diferentes',
            'Criação com [ ], lista vazia e list(range())',
            'Acesso por índice e índices negativos',
            'IndexError e TypeError por índice inválido',
            'len() e in/not in',
            'Alteração de um elemento',

            # 6. Funções
            'O que é uma função e por que ela ajuda (abstração)',
            'Sintaxe do def: nome, parâmetros e corpo indentado',
            'Argumentos (abs, pow, max) e função sem argumento',
            'Funções que retornam valores com return, usados em variáveis ou expressões',

            # 7. Dicionários
            'Conceito: tipo mapeado (vetor associativo), com chave imutável e valor de qualquer tipo',
            'Criação com { } vazio e inserção de pares',
            'Criação com a lista de pares chave: valor',
            'Busca de valor pela chave',
            'A ordem dos pares não importa, e o dicionário nunca é indexado por inteiros'
        ]
    }

    intermediario = {
        'Conteudo': [
            # 1. Variáveis e Expressões
            'Divisão / x divisão inteira //',
            'Conversão de tipos com int(), float() e str(), incluindo o ValueError',
            'Ordem das operações (PEMDAS)',
            'Strings com + (concatenação) e * (repetição)',
            'input() com conversão e split() para ler vários valores',
            'Composição de expressões',
            'Operador módulo %',
            'Papéis das variáveis: valor fixo, contador, somador, sinalizador, etc.',

            # 2. Estruturas Condicionais
            'Operadores lógicos and, or, not',
            'Tabelas verdade de and, or e not',
            'if/elif/else encadeado, sem limite de encadeamento',
            'Comparação de strings (igualdade e ordem alfabética)',
            'Fluxogramas de if/else e de condicionais encadeadas',

            # 3. Estruturas de Repetição
            'while quando não se sabe quantas repetições serão feitas (soma até digitar um negativo)',
            'for com a variável do laço e f-string',
            'Papéis das variáveis em laços: contador, somador, armazenador do valor mais esperado, sinalizador',
            'break e continue',
            'Exercício do “fim”: a diferença entre and e or na condição e o uso de .lower()',
            'Exercícios de média da turma e média de 20 números',

            # 4. Strings
            'Fatiamento [a:b], [:n] e [n:]',
            'Imutabilidade e criação de uma nova string por concatenação',
            'Marcação de strings com find() e etiquetas',
            'Formatação: .format(), operador % e f-string (a mais usada no curso)',
            'Caracteres de conversão (d, f, e, s, etc.) e modificadores (largura, alinhamento, zeros, casas decimais)',

            # 5. Listas e Tuplas
            'Operadores + e * com listas',
            'Fatiamento',
            'Mutabilidade: alterar, remover e inserir elementos por fatia',
            'Comando del',
            'Tuplas: sintaxe (parênteses opcionais, vírgula na tupla de 1 elemento), imutabilidade e fatiamento',
            'split() e join() entre strings e listas',

            # 6. Funções
            'Dicas de retorno: variável temporária, evitar código morto, garantir return em todos os caminhos (senão retorna None)',
            'Tuplas como valor de retorno (exemplo da equação do 2º grau)',
            'Função chamando outra função (area_retangulo e area_quadrado)',
            'Fluxo de execução: definir antes de chamar',
            'Funções booleanas (eh_divisivel)',
            'Documentação com docstrings e help()',

            # 7. Dicionários
            'Hashing: por que dicionários são rápidos e listas de tuplas são lentas',
            'Remoção com del',
            'Alteração e inserção de valor (exemplo do estoque de bananas)',
            'len() e in/not in (testam as chaves)',
            'Métodos: sintaxe objeto.método e os métodos keys(), values() e items()'
        ]
    }

    avancado = {
        'Conteudo': [
            # 1. Variáveis e Expressões
            'Como o computador representa dados: binário, ASCII, ISO-Latin 1, Unicode/UTF-8',
            'Exceção do **, que associa da direita para a esquerda (2**3**2 = 512)',
            '% e // em conversões: segundos para dias/horas/min/s, e a comparação entre 1 milhão e 1 bilhão de segundos',
            '% para divisibilidade, par/ímpar e extração de dígitos',
            'Limites da composição (o lado esquerdo da atribuição precisa ser uma variável)',
            'Outros papéis: temporária, organizador, container, atravessador',
            'Problema aplicado: média aritmética',

            # 2. Estruturas Condicionais
            'Condicionais aninhadas e como simplificá-las (0 < x < 10)',
            'Regras de simplificação da álgebra booleana',
            'Opostos lógicos para evitar o not',
            'Leis de Morgan',
            'Exercícios: loja de informática (promoção e forma de pagamento), duração do jogo (virada de dia) e maior subsequência incomum',

            # 3. Estruturas de Repetição
            'Rastreamento (tracing) manual para achar o erro no fatorial',
            'Exercícios de chuva: maior quantidade e dia que mais choveu',
            'Revisão de algoritmo (sequência finita, não ambígua e mecânica)',
            'Integral por retângulos: mais retângulos dão mais precisão',
            'Para casa: área sob x² em [0, 5] e algoritmo adaptativo com erro de 0,01',

            # 4. Strings
            'Problema 1: converter frase para CamelCase e SnakeCase',
            'Problema 2: extrair item, unidade e preço de uma string com etiquetas (retorna produto e preço, ou None e None)',
            'Problema 3: cifra de César, para criptografar e decifrar, e a discussão sobre a melhor forma de construir a função',
            'Integração de strings com listas, tuplas e funções',

            # 5. Listas e Tuplas
            'Objetos, referências e id()',
            'Aliasing (apelidos) e clonagem com a[:]',
            'Listas aninhadas e matrizes (m[1][2])',
            'Atribuição com tuplas, empacotamento e desempacotamento',
            'Composição de estruturas (lista de tuplas que contêm listas)',
            'List comprehension',
            'Exercícios: multiplicação de matrizes e sistema de controle de estoque',

            # 6. Funções
            'Variáveis locais x globais: tempo de vida, pilha de execução, e por que só globais mantêm informação entre chamadas',
            'Funções que manipulam strings: len, find e o módulo string (ascii_letters, digits)',
            'Desenvolvimento incremental (distância entre dois pontos, em 5 passos)',
            'Pensamento computacional: decomposição de problemas em funções',
            'Questões do CodeRunner: função com print x função com retorno',
            'Problema da decomposição do atraso na aula',

            # 7. Dicionários
            'Apelidar (aliasing) x clonar (copy()), com verificação por id()',
            'Matrizes esparsas com tuplas (linha, coluna) como chave',
            'KeyError ao buscar uma chave inexistente',
            'Método get(chave, padrão) para evitar esse erro'
        ]
    }

    return iniciante, intermediario, avancado

iniciante, intermediario, avancado = dificuldades()

informacoes_IA = {'Identidade': '''***Isto é apenas sua definição, o que você é, não apresente nada disso em nenhuma resposta, quero apenas que você entenda seus objetivos***

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

***(Nome do enunciado, algo como um tópico, tipo Variáveis, Repetições, etc) - (Nível de dificuldade de acordo com a 'mensagem')***

*História:

-(Especificação da questão, algo mostrando a história, o contexto).

*Comando:

-(O que deve ser feito a partir do que foi apresentado na história, o que tem que ser feito para resolver este problema usando o Python):

---Exemplos---

(3 Exemplos de Entradas e Saidas de um modo que fique centralizado e esteticamente bonito, não é para entregar nenhum código, é apenas para mostrar exemplos de entrada e saida. Faça algo assim:

          Entrada-----------------------------Saida
1 - alguma coisa de entrada ---------- alguma coisa de saida
2 - alguma coisa de entrada ---------- alguma coisa de saida
3 - alguma coisa de entrada ---------- alguma coisa de saida)'''
                  }
#Mensagens iniciais#
print(100*'-')
print()
titulo = 'Seja bem vindo à IA Teacher!'
print(titulo.center(100,'-'))
while resp != '1':
    print('\n**Selecione 1 para proseguir, 2 para trocar o modelo de IA e 3 para sair do programa:')
    print('\n1) Iniciar diagnostico.')
    print('2) Trocar modelo de IA.')
    print('3) Encerrar programa.')
    resp = input('\nDigite aqui: ')

    while resp not in ('1', '2', '3'):
        print('\n***Erro, caractere não encontrado, digite 1 ou 2***')
        resp = input('\nDigite aqui: ')

    if resp == '3':
        print()
        titulo = 'Programa encerrado'
        print(titulo.center(100, '-'))
        exit()
    elif resp == '2':
        print()
        titulo = 'Alteração da IA'
        print(titulo.center(100, '-'))
        print(f'\n**Para alterar a IA atual: {IA_Atual} siga as seguintes regras abaixo**\n')
        print('1) Instale o modelo desejado dentro da lista de modelos do Ollama no seguinte link: https://ollama.com/search')
        print('''2) Digite o nome da IA, sua versão e a quantidade de parâmetros na mesma linha sem espaços. Siga o exemplo abaixo:

----------------------------------------
- Nome da IA: qwen
- Versão: 3.5
- Quantidade de parâmetros: 4b

*Como deve escrever: qwen3.5:4b
----------------------------------------\n''')
        IA_Atual = input('Digite o modelo escolhido aqui: ')
        print()
        ia_alterada = 'IA alterada com sucesso'
        print(ia_alterada.center(100, '-'))
        
#Configuração da IA + Diagnostico#
for _ in range(10):
    numero += 1
    if numero < 6:
        mensagem = f"\nDificuldade Iniciante:\n{iniciante['Conteudo']}"
    elif 5 < numero < 9:
        mensagem = f"\nDificuldade Intermediário:\n{intermediario['Conteudo']}"
    elif numero > 8:
        mensagem = f"\nDificuldade Avançado:\n{avancado['Conteudo']}"
    resposta = ollama.chat(
        model = IA_Atual ,
        messages =[
            {
                'role': 'system',
                'content': informacoes_IA['Identidade'] +
                informacoes_IA['Exemplo de Exercicio'] +
                mensagem
                }
            ],
        options={
            "temperature": 0,
            }
        )
    print()
    titulo = (f'Questão nº{numero}:')
    print(titulo.center(100, '-'))
    if numero == 1:
        print(regras)
    print()
    print(resposta['message']['content'])
    os.startfile('Questão.py')
    print('\n**Digite sua resposta no arquivo Questão.py aberto, dentro dele você pode realizar seus testes e verificar se o programa está funcionando de acordo com o comando da questão.**\n')
    resp = input('- Digite 1 para apresentar sua resposta para a IA: ')
    while resp != '1':
        print('\n***Erro, caractere não encontrado, digite 1 para prosseguir***')
        resp = input('\nDigite aqui: ')
    titulo = (f'Resposta da questão nº{numero}:')
    print(titulo.center(100, '-'))
    respostas = open('Questão.py', 'r', encoding = 'utf-8')
    conteudo = respostas.read()
    print(f'\n{conteudo}\n')
    respostas.close()