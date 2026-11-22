#Imports#
import ollama
import os
import random
import io
import sys
import contextlib
#Variáveis#
numero = 0
resp = 0
pontuacao = 0
pontuacao_diag = 0
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
                  
                  'Exemplo de Exercicio': '''Não se apresente. Isto é apenas um modelo de como os exercícios devem ser elaborados. Siga rigorosamente todas as instruções e a estrutura abaixo.

A resposta deverá conter três seções separadas pelos seguintes marcadores:

[ENUNCIADO]

[TESTES_PUBLICOS]

[TESTES_PRIVADOS]

Não escreva nada antes, entre ou depois dessas seções além do conteúdo solicitado.

[ENUNCIADO]

**Conteúdo:** Informe o conteúdo escolhido para o exercício.

**Nível de Dificuldade:** Informe o nível de dificuldade: Iniciante, Intermediário ou Avançado.

**História:**

Crie uma história contextualizada, preferencialmente relacionada a situações da vida real.

A história deve ter relação direta com o conteúdo escolhido e servir de contexto para o problema.

Evite histórias desnecessariamente longas ou que não contribuam para a compreensão do exercício.

**Comando:**

Explique claramente o que o estudante deverá desenvolver utilizando Python.

Especifique todas as tarefas, condições e restrições necessárias para resolver o problema.

Não deixe informações importantes implícitas.

O comando deve informar claramente:
- Quais dados o programa receberá.
- Como esses dados serão fornecidos.
- O que o programa deverá fazer com eles.
- O que deverá ser apresentado na saída.
- Quais condições e restrições deverão ser respeitadas.

Não apresente a resolução nem trechos de código que entreguem a resposta.

**Formato de entrada e saída:**

Todos os exercícios devem utilizar a entrada e a saída padrão do Python (stdin e stdout).

Estabeleça um formato de entrada simples, explícito e padronizado para cada exercício.

Regras obrigatórias:

1. Quando houver apenas um dado de entrada, informe exatamente como ele será fornecido.
2. Quando houver vários dados, estabeleça a ordem em que serão recebidos.
3. Quando houver listas ou coleções de tamanho variável, informe primeiro a quantidade de elementos e, em seguida, forneça cada elemento em uma linha separada, salvo quando outro formato for mais adequado.
4. Não utilize representações de objetos Python como entradas, por exemplo, listas escritas entre colchetes ou tuplas.
5. Não deixe o estudante depender de variáveis previamente criadas pelo sistema. Os dados devem ser recebidos pelo próprio programa.
6. Defina claramente o formato da saída, incluindo separadores, ordem dos elementos e quantidade de linhas.
7. Não exija informações que não estejam presentes nas entradas.

[TESTES_PUBLICOS]

Apresente exatamente 5 testes públicos, cada um contendo uma entrada e sua respectiva saída esperada.

Os testes públicos serão apresentados ao estudante no enunciado do exercício.

Requisitos:

- As entradas devem ser coerentes com a história e com o comando.
- As entradas devem seguir exatamente o formato estabelecido no enunciado.
- As saídas devem corresponder exatamente aos resultados esperados para cada entrada.
- Os testes devem demonstrar diferentes situações possíveis do exercício.
- Inclua casos comuns e situações específicas que permitam verificar diferentes comportamentos do programa.
- Não apresente códigos Python nos testes.
- Apresente somente os dados que serão fornecidos ao programa e os resultados que ele deverá produzir.
- Não inclua explicações ou comentários dentro das entradas e saídas.
- Certifique-se de que os testes possam ser enviados diretamente ao programa por meio da entrada padrão.

Utilize obrigatoriamente a seguinte estrutura para cada teste:

[TESTE]
Entrada:
(dados de entrada)

Saída:
(resultado esperado)

Repita essa estrutura exatamente 5 vezes.

[TESTES_PRIVADOS]

Apresente exatamente 3 testes privados, cada um contendo uma entrada e sua respectiva saída esperada.

Estes testes serão utilizados exclusivamente pelo sistema AI Teacher para avaliar o código desenvolvido pelo estudante. Portanto, não devem ser apresentados ao estudante nem incluídos na parte pública do exercício.

Requisitos:

- Os testes devem verificar situações diferentes das apresentadas nos 5 testes públicos.
- Utilize entradas que permitam identificar erros de lógica e situações que o estudante talvez não tenha considerado.
- Inclua casos especiais e situações-limite quando forem pertinentes ao problema.
- As saídas devem corresponder exatamente aos resultados esperados para cada entrada.
- Não crie testes impossíveis ou que contrariem as regras estabelecidas no comando.
- As entradas devem seguir exatamente o mesmo formato estabelecido no enunciado.
- Não apresente códigos Python nos testes.
- Garanta que os testes possam ser enviados diretamente ao programa por meio da entrada padrão.
- Não repita os mesmos casos dos testes públicos com apenas pequenas alterações.

Utilize obrigatoriamente a seguinte estrutura para cada teste:

[TESTE]
Entrada:
(dados de entrada)

Saída:
(resultado esperado)

Repita essa estrutura exatamente 3 vezes.

-- REGRAS GERAIS

- O exercício deve possuir uma solução possível e coerente com todas as instruções.
- Os 8 testes devem ser consistentes com o mesmo enunciado e as mesmas regras.
- Os testes públicos e privados devem utilizar exatamente o mesmo formato de entrada.
- Todas as entradas devem fornecer os dados necessários para a execução do programa.
- Todas as saídas devem representar exatamente o resultado esperado.
- Não inclua valores implícitos, variáveis previamente definidas ou informações que o programa não tenha como receber.
- Não apresente respostas, dicas ou trechos de código que revelem a solução.
- Não repita desnecessariamente os mesmos casos de teste.
- Não altere a quantidade de testes solicitada.
- Os testes privados devem permanecer separados dos testes públicos.
- Priorize exercícios que possam ser avaliados automaticamente, executando o código do estudante e comparando sua saída com a saída esperada.
- Evite exercícios cuja correção dependa de comparar o texto do código escrito pelo estudante. Avalie o comportamento e o resultado produzido pelo programa.

-- REGRAS DE FORMATAÇÃO ADICIONAIS

1. Utilize exatamente os marcadores [ENUNCIADO], [TESTES_PUBLICOS], [TESTES_PRIVADOS] e [TESTE].
2. Cada teste deve possuir obrigatoriamente os campos Entrada: e Saída:.
3. Nunca coloque dois testes dentro do mesmo marcador [TESTE].
4. Não coloque os marcadores [TESTES_PUBLICOS] e [TESTES_PRIVADOS] dentro de um teste.
5. Não inclua numeração, títulos adicionais ou comentários entre os testes.
6. Não utilize cercas de código Markdown nos testes.
7. Preserve as quebras de linha das entradas e saídas.
8. Não inclua textos como "Exemplo de entrada" ou "Exemplo de saída" no lugar dos marcadores obrigatórios.
9. Não coloque o enunciado dentro dos testes.
10. Garanta que cada entrada e saída estejam claramente separadas.''',
                  
                  'Revisão do Exercício': '''Após gerar o exercício, revise cuidadosamente todo o conteúdo
    antes de enviá-lo ao usuário.

    Verifique os seguintes requisitos:

    1. Estrutura:
       - Contém o marcador [ENUNCIADO].
       - Contém o marcador [TESTES_PUBLICOS].
       - Contém o marcador [TESTES_PRIVADOS].
       - Possui exatamente 5 testes públicos.
       - Possui exatamente 3 testes privados.
       - Não coloque nenhum '#' no programa.

    2. Coerência:
       - O enunciado está claro e não possui ambiguidades.
       - As entradas dos testes seguem o formato explicado.
       - As saídas esperadas correspondem ao que o enunciado solicita.
       - Todos os testes possuem entradas e saídas válidas.

    3. Dificuldade:
       - O exercício corresponde ao nível solicitado.
       - O conteúdo está relacionado ao tema escolhido.

    4. Correção:
       - Recalcule os resultados de cada teste.
       - Verifique se não existem erros matemáticos ou lógicos.
       - Confira se os testes públicos e privados são coerentes.

    Caso encontre algum problema, corrija o exercício antes de enviá-lo.
    Não apresente a revisão ao usuário, apenas o exercício corrigido.''',
                  
                  'Controle de Dificuldade': '''CONTROLE DE DIFICULDADE

O número da questão, o nível de dificuldade e o conteúdo serão fornecidos pelo sistema.

Você deve respeitar obrigatoriamente essas informações.

- Não escolha ou altere o nível de dificuldade.
- Não substitua o conteúdo informado por outro.
- Não determine a dificuldade com base na sua própria avaliação do conteúdo.
- Elabore o exercício considerando o nível recebido.

A dificuldade deve ser compatível com o nível solicitado:

**Iniciante:**
- Conceitos fundamentais de Python.
- Problemas simples e diretos.
- Poucas etapas de raciocínio.
- Utilização de estruturas básicas.

**Intermediário:**
- Combinação de diferentes conceitos.
- Problemas que exigem mais etapas de raciocínio.
- Manipulação de estruturas de dados.
- Maior necessidade de organização e lógica.

**Avançado:**
- Problemas que exigem raciocínio mais elaborado.
- Combinação de vários conceitos.
- Maior complexidade na manipulação de dados.
- Situações que exigem planejamento da solução.

O nível informado pelo sistema deve aparecer corretamente no campo "Nível de Dificuldade" do enunciado.'''
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
        nivel = 'Iniciante'
        mensagem = 'Conteudo a ser tratado: ' + random.choice(iniciante['Conteudo'])
    elif 5 < numero < 9:
        nivel = 'Intermediário'
        mensagem = 'Conteudo a ser tratado: ' + random.choice(intermediario['Conteudo'])
    elif numero > 8:
        nivel = 'Avançado'
        mensagem = 'Conteudo a ser tratado: ' + random.choice(avancado['Conteudo'])
    def verificacao_de_falha_na_geracao(mensagem):
        
        while True:
            resposta = ollama.chat(
            model = IA_Atual ,
            messages =[
                {
                    'role': 'system',
                    'content': informacoes_IA['Identidade'] +
                    informacoes_IA['Exemplo de Exercicio'] +
                    informacoes_IA['Controle de Dificuldade'] +
                    informacoes_IA['Revisão do Exercício'] +
                    mensagem +
                    nivel
                    }
                ],
            think = False,
            options={
                "temperature": 0.3,
                "num_predict": 2000,
                "num_ctx": 8192,
                'num_gpu': 999
                }
            )
            texto = resposta['message']['content']
            if ('[ENUNCIADO]' in texto and '[TESTES_PUBLICOS]' in texto and '[TESTES_PRIVADOS]' in texto and '#' not in texto and texto.count('Entrada:') == 8 and texto.count('Saída:') == 8):
                verificacao_resposta = ollama.chat(
                model = IA_Atual ,
                messages =[
                    {
                        'role': 'system',
                        'content': '''Verifique a lógica deste exercício, 
                        se ele está fazendo sentido e se as entradas e saídas estão condizentes com o que deveria ser. 
                        **Não se apresente nem diga nada além do que for solicitado: Caso o faça sentido e tudo esteja certo, digite sim, do contratio não.
                        
                        *Responda se faz sentido apresente apenas:*
                        
                        Sim
                        
                        *Responda se não faz sentido apresente apenas:*
                        
                        Não
                        ''' + 
                        texto
                    }
                ],
                think = False,
                options ={
                    'temperature': 0.3,
                    'num_predict': 10,
                    'num_ctx': 8192
                    }
                )

                if 'sim' in verificacao_resposta['message']['content'].lower():
                    return texto
                else:
                    mensagem += '''Sua geração anterior teve alguns erros de inconsistência.
                    verifique se as entradas e saidas fazem sentido de acordo com o contexto apresentato.'''
            else:
                mensagem += ''' A geração anterior ficou incompleta.
                Gere novamente o exercício contendo os três marcadores.
                Confira se as entradas e saídas dos testes estão coerentes.
                No marcador [TESTES_PUBLICOS] deve conter 5 entradas e 5 saidas esperadas.
                No marcador [TESTES_PRIVADOS] deve conter 3 entradas e 3 saidas esperadas.
                Não coloque nenhum '#' no programa.'''
    print()
    n_questao = (f'Questão nº{numero}:')
    print(n_questao.center(100, '-'))
    if numero == 1:
        print(regras)
    print()

    exercicio = verificacao_de_falha_na_geracao(mensagem)
    partes = exercicio.split('[TESTES_PUBLICOS]')
    enunciado = partes[0]
    partes_testes = partes[1].split('[TESTES_PRIVADOS]')
    testes_publicos = '[TESTES_PUBLICOS]' + partes_testes[0]
    testes_privados = '[TESTES_PRIVADOS]' + partes_testes[1]
    parte_visivel = enunciado + testes_publicos
    print(parte_visivel)
#Resposta do Usuário#
    os.startfile('Questão.py')
    print('\n**Resolva o problema acima no arquivo Questão.py. Se abrir no Thonny, salve seu código antes de apresentar sua resposta abaixo.**\n')
    resp = input('- Digite 1 para verificar sua resposta: ')
    while resp != '1':
        print('\n***Erro, caractere não encontrado, digite 1 para prosseguir***')
        resp = input('\nDigite aqui: ')
    print()
    res_questao = (f'Resposta entregue nº{numero}:')
    print(res_questao.center(100, '-'))
    respostas = open('Questão.py', 'r', encoding = 'utf-8')
    conteudo = respostas.read()
    print(f'\n{conteudo}\n')
    respostas.close()
#Histórico#
    guardar = open('Histórico.txt', 'a', encoding = 'utf-8')
    historico = guardar.write(n_questao.center(100, '-') +'\n' +parte_visivel +'\n' +res_questao.center(100, '-') +'\n' +conteudo +'\n')
    guardar.close()

# Separando as Entradas e Saídas #
    teste = (testes_publicos.replace('[TESTES_PUBLICOS]', '') + '\n' + testes_privados.replace('[TESTES_PRIVADOS]', ''))
    lista_testes = teste.split('[TESTE]')

    for i in range (1, 5):
            if i == 1:
                pontos = 10
            elif i == 2:
                pontos = 7
            elif i == 3:
                pontos = 4
            else:
                pontos = 0
            if 1 < i < 4:
                print()
                teste_falhou = f'Código incorreto - Teste nº{i}'
                print(teste_falhou.center(100, '-'))
    
                os.startfile('Questão.py')
                respostas = open('Questão.py', 'r', encoding = 'utf-8')
                conteudo = respostas.read()

                print('\n**Revise seu código à procura de erros.**\n')
                resp = input('- Digite 1 para verificar sua resposta: ')
                while resp != '1':
                    print('\n***Erro, caractere não encontrado, digite 1 para prosseguir***')
                    resp = input('\nDigite aqui: ')

                print(f'\n{conteudo}\n')
                respostas.close()

                guardar = open('Histórico.txt', 'a', encoding = 'utf-8')
                historico += guardar.write('\n' + teste_falhou.center(100, '-') + conteudo + '\n')

            elif i == 4:
                pontuacao += pontos
                print()
                max_tentativas = 'Limite de tentativas atingido - 3/3'
                print(max_tentativas.center(100, '='))
                print()

                respostas = open('Questão.py', 'w', encoding = 'utf-8')
                respostas.close()

                guardar = open('Histórico.txt', 'a', encoding = 'utf-8')
                historico += guardar.write('\n' + max_tentativas.center(100, '=') + '\n')
                break
# Verificando Respostas #
            acertos = 0
            n = 0
            falha = ''
            print()
            detalhes = 'Detalhes da resposta'
            print(detalhes.center(100, '-'))
            print()

            for teste in lista_testes:

                if teste.strip() == '':
                    continue

                n += 1

                entradas_saidas = teste.split('Saída:', 1)

                entrada = entradas_saidas[0].replace('Entrada:', '', 1).strip()
                saida_esperada = entradas_saidas[1].strip()

                saida_questao = io.StringIO()
                entrada_original = sys.stdin
                saida_original = sys.stdout

                try:
                    sys.stdin = io.StringIO(entrada + '\n')
                    sys.stdout = saida_questao

                    exec(conteudo, {})

                    erro = None

                except Exception as erro_execucao:
                    erro = erro_execucao

                finally:
                    sys.stdin = entrada_original
                    sys.stdout = saida_original

                resposta_entregue = saida_questao.getvalue().strip()

                if erro is None and resposta_entregue == saida_esperada:

                    acertos += 1
                    print(f'Teste {n}: ACERTOU!')

                else:

                    print(f'Teste {n}: ERROU!')

                    if erro is not None:
                        print(f'Erro: {erro}')

                    else:
                        print(f'Esperado: {saida_esperada}')
                        print(f'Recebido: {resposta_entregue}')

                    break

            print()

            if acertos == 8:
                falha = '*Código sem erros!'
                print(falha)
                respostas = open('Questão.py', 'w', encoding = 'utf-8')
                respostas.close()
                pontuacao += pontos
                guardar = open('Histórico.txt', 'a', encoding = 'utf-8')
                historico += guardar.write('\n' + detalhes.center(100, '-') + '\n' + falha + '\n')
                break
            else:
                falha = '*Código com mau funcionamento!'
                print(falha)
                print(f'Falhou no teste {n}.')
            guardar = open('Histórico.txt', 'a', encoding = 'utf-8')
            historico += guardar.write('\n' + detalhes.center(100, '-') + '\n' + falha + '\n')
if pontuacao_diag < 40:
    nivel_atual = 'Iniciante'
elif 39 < pontuacao_diag < 70:
    nivel_atual = 'Intermediário'
elif 69 < pontuacao_diag:
    nivel_atual = 'Avançado'
print(f'\nSua taxa de acertos foi de {pontuacao_diag}%. Seu nível atual é {nivel_atual}.\n')
#Painel principal.#
def painel_principal():
    painel = 'Painel Principal'
    print(painel.center(100, '='))
    print('''
    **Digite o número para acessar a opção desejada:

1) Prosseguir para os exercícios.
2) Alterar a IA.
3) Acessar a pontuação do diagnóstico.
4) Acessar o histórico.
5) Encerrar o programa.\n''')
    resp = input('Digite aqui um número de 1 a 5: ')
    while resp != '1' and resp != '2' and resp != '3' and resp != '4' and resp != '5':
        print('\n**Erro!! Caractere não suportado, por favor digite um numero de 1 a 5:\n')
        resp = input('Digite aqui:')
    
    if resp == '5':
        print()
        print(titulo.center(100, '-'))
        exit()
    elif resp == '4':
        print()
        mensagem = 'Acessando o Histórico'
        print(mensagem.center(100, '='))
        print()
        print(historico + '\n')
        painel_principal()
    elif resp == '3':
        mensagem = 'Pontuação do Diagnóstico'
        print(mensagem.center(100, '='))
        print(f'''
Pontuação tirada no diagnostico: {pontuacao_diag}%.
Nível atingido: {nivel_atual}.\n''')
        painel_principal()
    elif resp == '2':
        print()
        titulo = 'Alteração da IA'
        print(titulo.center(100, '='))
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
        print(ia_alterada.center(100, '='))
        painel_principal()
    elif resp == '1':
        mensagem = 'Prosseguindo para o Exercício'
        print(mensagem.center(100, '='))
        print()
        print(f'''
**Bem vindo aos exercícios de Python do IA Teacher!! Com base no seu desempenho anterior iremos te ajudar com exercícios no seu nível.

Nível atual: {nivel_atual}.

-Carregando exercícios do seu nível...''')