# Estados alternativos

Cria um ambiente de filtros isolado para fazer comparações entre datas e seleções

# Set Analysis

- `$` Aplica filtros do usuário
- `1` Ignora filtros do usuário
- `$1` Seleção anterior
- `$_1` Seleção posterior
- `{MeuOutroEstado}` Aplicado o filtro realizado em outro estado alternativo criado
- `{MeuMarcador}` Aplicado o filtro realizado no marcador informado
- `Sum($<Ano={'2024'}> Venda)` - Soma do valor de venda congelando o ano em 2024 e aplicando demais filtros
- `Sum(1<Ano={'2024'}> Venda)` - Soma do valor de venda congelando o ano em 2024 e ignorando demais filtros realizados nas outras dimensões
- `Count( {1} IdCliente)` - Contagem da quantidade de clientes total ignorando qualquer filtro aplicado
- `Count( {<Cidade,Idade>} IdCliente)` - Contagem da quantidade de clientes ignorando filtros aplicados nos campos *Cidade* e *Idade*
- `Count( <UF+={'SP'}> Id_Ordem)` - Adicionando SP ao filtro que estiver aplicado de *UF*
- `Count( <UF+={'SP','RJ'}> Id_Ordem)` - Adicionando sempre SP e RJ ao filtro que estiver aplicado de *UF*
- `Count( <UF-={'SP','RJ'}> Id_Ordem)` - Retirando sempre SP e RJ ao filtro que estiver aplicado de *UF*
- `Count( <UF=-{'SP','RJ'}> Id_Ordem)` - Todos os valores de UF, exceto SP e RJ

- Ao trabalhar caracteres coringa, usa-se aspas duplas, assim como para filtrar uma data com máscara
- Aspas simples é para filtrar o conteúdo literal, duplo avalia a expressão
## Junção

- `Sum( $<Ano={2023}> + $<Pais={Brasil}>  Vendas)` - Soma das vendas do ano de 2023 **MAIS** soma das vendas do Brasil (considerando filtros dos usuários em outras dimensões)
## Exclusão

`Sum( $<Ano={2023}> - $<Pais={Brasil}>  Vendas)` - Soma das vendas do ano de 2023 **MENOS** soma das vendas do Brasil
## Operadores de interseção

`Sum( $<Ano={2023}> * $<Pais={Brasil}>  Vendas)` - Soma das vendas do ano de 2023 **E** soma das vendas do Brasil, mesmo que:
-   `Sum( $<Ano={2023}, Pais={Brasil}>  Vendas)`

## Diferença simétrica - XOR

`Sum( $<Ano={2023}> / $<Pais={Brasil}>  Vendas)` - Soma das vendas ignorando a interseção do ano de 2023 **E** do Brasil

## Avançando...

`Sum( {<Ano={">=2000<=2017"}>} Venda)`
`Sum( {<Ano={"1998", ">=2000<=2017"}>} Venda)`
`Sum( {<Ano={"1998", ">=2000<=2017"}, Pais={"B*", "*a*"}>} Venda)`
`Sum( {<Ano-={"1998", ">=2000<=2017"}, Pais-={"B*", "*a*"}>} Venda)`
`Sum( {- <Ano={"1998", ">=2000<=2017"}, Pais={"B*", "*a*"}>} Venda)`

Valor adicionado implicitamente no filtro (sempre vai somar)

`Sum( {<Ano+={"1988"}>} Venda]`

```rb
Sum({<

    [País]={"SUM(Gols_Visitante)>=2"}

>} Gols_Casa)

---------------------------------------------------------

Sum({<

    Ano={"$(=Max(Ano))"}

>} Gols_Casa)

---------------------------------------------------------

Sum({<

    Ano={"$(=Max({<País={'Puerto Rico'}>} Ano))"}

>} Gols_Casa)
```

Definição de valor de campo implícita

```rb
# Possíveis

Sum(

{<

    [País]=P({<Ano={2015}, Resultado={'Vitóra'}>} [País])

>}

Gols_Casa)
```

```rb
# Excluíveis

Sum(

{<

    [País]=E({<Ano={2015}, Resultado={'Vitóra'}>} [País])

>}

Gols_Casa)
```

## Somente filtro em uma dimensão

- Somente a dimensão Prioridade e a dimensão UF estão sendo impactadas

```rb
Count(

{

    1<Prioridade=$::Prioridade, UF=$::UF>

}

Id_Ordem)
```

- Nesse caso abaixo somente se aplicam filtros em Prioridade (estado padrão) e UF (estado alternativo - S02)

```rb
Count(

{

    1<Prioridade=$::Prioridade, UF=S02::UF>

}

Id_Ordem)
```

# Funções

## Principais

| Função            | Uso                                                                                      | Exemplo                                        |
| ----------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Sum               |                                                                                          | `Sum(Vendas)`                                  |
| Count             |                                                                                          | `Count(Cupons)`                                |
| Max               |                                                                                          | `Max(Data)`                                    |
| Min               |                                                                                          | `Min(Data)`                                    |
| Avg               |                                                                                          | `Avg(PrecoDeVenda)`                            |
| Median            |                                                                                          | `Median(Valor)`                                |
| Mode              | Retorna valor mais frequente se não houver empate                                        | `Mode(ClienteNome)`                            |
| Distinct          | Valores únicos                                                                           | `Count(Distinct ClienteNome)`                  |
| Total             | Ignora dimensões                                                                         | `Count(Total ClienteNome)`                     |
| All               | Ignora dimensões e filtros (tudo)                                                        | `Count(All ClienteNome)`                       |
| NullCount         | Contagens de linhas nulas                                                                | `NullCount(IdVenda)`                           |
| NumericCount      | Contagem de valores numéricos                                                            | `NumericCount(ValorVenda)`                     |
| TextCount         | Contagem de valores textuais                                                             | `TextCount(ClienteNome)`                       |
| FirstSortedValue  | Retorna o primeiro valor por algum critério, crescentef                                  | `FirstSortedValue(Cliente,Valor,1)`            |
| Only              | Retorna um valor se ele for único na dimensão filtrada, senão retorna nulo               | `Only(Ano)`                                    |
| MaxString         | Retorna o último valor textual por ordem alfabética                                      | `MaxString(ClienteNome)`                       |
| MinString         | Retorna o primeiro valor textual por ordem alfabética                                    | `MinString(ClienteNome)`                       |
| Concat            | Junta vários valores de texto em um só com possibilidade de delimitador                  | `Concat(Parcelamento,';')`                     |
| ValueList         | Cria uma dimensão sintética com valores informados                                       | `ValueList('A','B','C')`                       |
| ValueLoop         | Cria uma dimensão em um range numérico informado                                         | `ValueLoop(5,10)`                              |
| Aggr              | Cria uma tabela virtual para cálculo                                                     | `Avg(Aggr(Sum(Valor),Agrupamento))`            |
| If                |                                                                                          | `If(Avg(Valor) < 499, 'Ok', 'Verificar')`      |
| Alt               | Traz o primeiro valor numérico válido de uma lista                                       | `Alt(Sum(Valor),Count(Valor),'ND')`            |
| Class             | Cria uma string com o intervalo onde o número se encontra. Ex: `14 <= Idade <= 64`       | `Class(25,50,'Idade',14`                       |
| Match             | Procura a posição (index start 1) de um texto em uma lista. Ex: `3`                      | `Match('jan', 'fev', 'mar', 'jan')`            |
| MixMatch          | Igual ao Match, porém case insensitive. Ex: `3`                                          | `MixMatch('Jan', 'fev', 'mar', 'jan')`         |
| WildMatch         | Igual ao MixMatch, porém usa caracteres coringas. Ex: `4`                                | `WildMatch('Mari', 'Jan', 'Fev', 'Ma*', M??)`  |
| Pick              | "Pegar" a expressão que estiver na posição especificada na lista que se segue. Ex: `30`  | `Pick(2,Sum(Valor),30,Avg(Valor))`             |
| RowNo             | Conta a linha atual, para ignorar dimensões, inserir `Total`                             | `RowNo()`                                      |

## Cores

- hexadecimal `'#FF0000'
- RGB `RGB(255,1,1)
- nomes `Blue()
- ARGB `ARGB(50,50,50,50)`
- ColorMix
    - Faz um gradiente entre uma cor e outra (formatação condicional no excel)
    - Recebe o número (entre 0 e 1), a cor do menor valor e a cor do maior valor
    - `ColorMix(0.5, Blue(), Red())`
    - Importante fazer um Set Analysis para capturar o valor mínimo e máximo total, depois dividir o valor atual por esse parâmetro e inserir no primeiro argumento da função

## Classificação

- Classificar em uma ordem específica começando com um elemento
- Nas propriedades da coluna da tabela escolher classificação personalizada e inserir a fórmula abaixo
- `Match(Agrupamento, 'Ouro')*-1`

## Funções de Data e Timestamp

Second
Minute
Hour
Day
Week
Month (multiplica por 1 traz o número)
Year
WeekYear
WeekDay (multiplica por 1 traz o número)

## Funções do sistema

Now
Today
LocalTime (pode ter horário de verão)

## Criar datas

MakeDate - Cria uma data (parametros: ano, mês dia)
MakeWeekDate - Encontra a data conforme pesquisa (parâmetros: Ano, Semana, Dia da semana)
MakeTime

## Adicionar Datas

AddMonths - Positivo ou negativo o acréscimo
AddYears - Positivo ou negativo o acréscimo
YearToDate - Checa se a data está no ano atual (conforme carregamento) e pode ser configurado para validar até outro período nas opções adicionais

## Start, End e Name

Year
Quarter
Week
Month
Day

MonthStart(MinhaData, 2) -  Mostra o início do mês de dois meses a frente (também funciona com número negativo para retroagir)

## Outras funções de data

Age - Age(DataFinal, DataNascimento) - Traz a idade em anos completos
NetWorkDays - Qtde de Dias úteis - NetWorkDays(DataInicial, DataFinal, Opcional Datas Feriados como Data)

## Funções matemáticas

Pow - Potência Pow(2,3) -> 8
Sqrt - Raíz quadrada - Sqrt(9) -> 3

## Funções de campo e seleção

`Get...(Semestre)`

GetAlternativeCount - Contagem de quantos são os outros campos possíveis na dimensão
GetExcludedCount - Contagem de campos que não são compatíveis de seleção para a dimensão
GetPossibleCount - Quantos valores são passíveis de seleção (excluídos já selecionados)
GetSelectedCount - Quantos campos estão "ticados"

GetCurrrentSelections - Retorna todos os nomes de campos e seleções aplicadas - `GetCurrentSelections()`
GetFieldSelections - Retorna as seleções para o campo informado - `GetFieldSelections(Agrupamento)`
GetObjectField - Identifica o nome do Campo na ordem informada (qual o 1o campo, 2o, etc) - `GetObjectField(1)`

## Funções de formato

Date
Dual - Converte um valor tanto para dimensão (texto) quanto para medida (valor) `Dual('Mês ' & Month(Data), Month(Data)*1)'
Interval - `Interval(100.5794, 'D hh:mm')` - Formata um intervalo de tempo (no ex, dias horas e minutos)
Money - `Money(1000, 'R$ #.##0,00', ',', '.')`
Num - Equivalente a *Money*
Time - Formata número como tempo `Time(0.8143, 'hh:mm:ss')`
Timestamp - Data e hora `Timestamp(50.123, 'DD/MM/YY hh:mm:ss')`

## Funções de interpretação

Date# - `Date(Date#('11/-10 2029', 'DD/-MM YYYY'), 'DD/MM/YYYY')`
Dual# 
Interval#
Money# 
Num# 
Text - `Text('11/10/2019)` - Preserva o formato texto original sem conversão automática
Time# - Formata número como tempo `Time(0.8143, 'hh:mm:ss')`
Timestamp# - Data e hora `Timestamp(50.123, 'DD/MM/YY hh:mm:ss')`

## Funções numéricas gerais

Div - Retorna a parte inteira de uma divisão de dois inteiros `Div(7,2)` = 3
Fabs - Absoluto do número `Fabs(4*-4)` = 16
Fact - Fatorial `Fact(5)` = 120
Frac - Resto fracionário, retorna a parte decimal de um número Float `Frac(7/3)` = 0.33
Sign - Retorna 1 se o número for positivo, zero se for zero, -1 se for negativo

## Funções de combinação e permutação

Permut - Número de arranjos possíveis `Permut(7,2)`
Conbin - Número de arranjos distintos `Combin(7,2)`

## Funções de módulo e paridade

FMod - Resto da divisão `FMod(7,3)` = 1, `FMod(7.5,3)` = 1.5
Mod - Resto inteiro da divisão de dois números, só trabalha com valores inteiros `Mod(8,3)` = 2
Even - Impar Verdadeiro/Falso
Odd - Par Verdadeiro/Falso

## Funções de arredondamento

Ceil - Arredondar para cima
Floor - Arredondar para baixo
Round - Para cima/baixo com qualquer 10^n (+/-)

## Funções de linha

Semelhantes a Window Functions no SQL

Above - Desloca n linhas da fórmula dentro da estrutura da tabela, ignora agrupamentos com Total
Below
Bottom - Exibe o último n valor da fórmula para dentro da estrutura informada
Topk
NoOfRows

Soma acumulada na coluna
```rb
RangeSum(
	Above(Total Count(Valor), 0, RowNo(Total))
)
```

## Column

Column - Usada para pegar a enésima coluna de expressão (não pega dimensões)
`Column(2)`

## Funções de tabela dinâmica

After - Traz o valor referente ao cálculo da **próxima** coluna
Before - idem com a coluna **anterior**
First - Primeira coluna de dados 
Last - Última coluna de dados
ColumnNo - Traz o número da coluna
NoOfColumns - Qtde total de colunas

## Funções de testes de tipo de dado

IsNum
IsText

## Funções de Nulo

Null
IsNull

## Funções de Intervalo

RangeMax - `RangeSum(Sum(Valor),1,2,3)`
RangeMin
RangeCount
RangeOnly
RangeSum

## Funções de ranqueamento

Rank - `Rank(Sum(Valor))` - Faz o ranking dentro do último nível de agrupamento
	- 4 argumentos `Rank(Sum(Valor), 0)` - Traz texto com posição Ex = `1-4
	- `Rank(Sum(Valor), 1)` Menor valor do intervalo se houve empate
	- `Rank(Sum(Valor), 2)` Valor médio do intervalo se houve empate
	- `Rank(Sum(Valor), 3)` Máximo valor do intervalo se houve empate
	- `Rank(Sum(Valor), 4)` Valor pela ordem de ocorrência no intervalo (Tipo dense rank do sql)
HRank - Rank horizontal - utilizado em tabela dinâmica

## Funções de texto

Capitalize - Primeira letra em maiúscula para cada palavra
Chr
Evaluate
FindOneOf - Encontrar a enésima ocorrência de um caractere em um texto (localizar do excel)
Hash128 - Criptografar o texto
Hash160
Hash256

Index - Posição de uma substring na string (case sensitive)
Left
Right
Mid
Len
Lower
Upper
Trim
LTrim
RTrim

Ord - Traz o código do primeiro caracter
KeepChar - Mantém somente os caracteres informados (case sensitive)
PurgeChar - Remove os caracteres informados (case sensitive)
Repeat
Replace
SubField - Divide o texto em blocos por um delimitador e paga o elemento n especificado
SubStringCount - Conta quantas vezes uma substring aparece em um texto
TextBetween - Pega uma string a partir de um caracter inicial e outro final

# Dicas
## Botões

É possível adicionar botões para executar tarefas como:
- Ir para a próxima página
- Executar filtros em campos
- Limpar filtros
Também há como criar uma ação ao entrar na pasta como por exemplo limpar seleções

## Dicas Container

Possível colocar dois gráficos no container e adicionar uma condição para que de acordo com os filtros feitos pelo usuário um ou outro seja ativado, de modo a dar mais detalhes da dimensão escolhida

# Joins

## Tipos

Inner
Left
Right
Outer - mesmo que o Join sem especificar o tipo

Keep - Utilizado no lugar do join para manter a tabela original

Carregar vários arquivos com mesma estrutura de uma única vez
- Utilizar caracteres coringa, como o asterisco no nome do arquivo

Concatenate 
- Une duas tabelas com as chaves em comum e acrescentando as colunas que são únicas adicionalmente
- Para evitar união automática usar o comando `NoConcatenate`

Inline - Cria tabela manualmente
```
Load * Inline [
Agrupamento, Valor
Prata, Valor1
Ouro, Valor2
Diamante, Valor3
];
```

Crosstable - Forma de "despivotar" uma tabela, tornando ela viável para análises
`CrossTable(Meses, Receita, 2)` -> Nome das colunas, Nome dos valores, quantos campos antes existem

Drop table(s) MyTable

First - Amostragem de dados
```
First 100 Load *  from [lib://Folder_Way/MyData.csv]
```

Hierarchy - Id_Pai, Id_Filho, Nome -> Organiza os dados de forma hierarquica

# Mapeamento

Map - Substitui o que encontra pelo mapeamento, o que não encontrar permanece igual

```ruby
De_Para:
Load * Inline [
Coluna1,Coluna2
Ouro,Ruby
Diamante,Esmeralda
];

Map Pedras using De_Para;

Dados:
Load * Inline [
Pedras
Ouro
Diamante
Plantina
];
```

Para "desmapear" usar o `unmap Pedras` ou `unmap *`

ApplyMap

```rb
De_Para:
Mapping
Load * Inline [
Coluna1,Coluna2
Ouro,Ruby
Diamante,Esmeralda
];

Dados:
Load 
ApplyMap('De_Para', Pedras, 'Outras Pedras') AS Pedras
Inline [
Pedras
Ouro
Diamante
Plantina
];
```

MapSubString - Útil para remover acentos

```rb
De_Para_2:
Mapping
Load * Inline [
Pedras
O,A
o,a
];

Dados:
Load 
MapSubString('De_Para_2', Pedras) AS Pedras
Inline [
Pedras
Ouro
Diamante
Plantina
];
```

# Variáveis

Servem pra mudar dinamicamente a execução do script
Pode utilizar o objeto "variable input" que permite criar opções para o usuário escolher
SET - Armazena o dado como string sem fazer o `evaluate`
LET - Faz avaliação da expressão antes de armazenar em memória

Para chamar:
`$(myVariable)` ou `'$(myVariable)'` para retornar texto

# Store

```rb
store Dados into [lib://File_Folder/MyFolder/MyFile.qvd](qvd);
store Dados into [lib://File_Folder/MyFolder/MyFile.csv](txt, separator is ';');
```

# Carga incremental

```rb
Dados:
LOAD
ID,
A,
B
FROM [lib://File_Folder/MyFolder/MyFile.qvd](qvd);

LOAD
ID,
A,
B
FROM [lib://File_Folder/MyFolder/MyFile.qvd](qvd)
WHERE NOT EXISTS(ID);

store Dados into [lib://File_Folder/MyFolder/MyFile.qvd](qvd);
```

# Estruturas de repetição
## Do Loop

```rb
Set vContador = 1

Do While vContador <= 3

	Something...;

	Exit Do When Condition...;

	vContador = $(vContador) + 1;

Loop
```

## For Loop

```rb
For vContagem = 1 to 10

	Dados:
	Load 
		$(vContagem) as Contagem
	Autogenerate 1;

	Exit for ...;

Next
```
## For Each

```rb
For Each v in DirList('lib://Files/*') 

	For Each f in FileList('$(f)/*')
	
		Dados:
		Load
			'$(v)' as Variavel,
			'$(f)' as Variavel_2
		Autogenerate 1;

	Next f

Next v
```

```rb
informacoes:
Load * Inline [
Campo
A
B
C
D
];

For each v in FieldValueList('Campo')

	Load
		'$(v)' as Valor_Campo
	Autogenerate 1;

Next v

Drop table informacoes;
```

# Funções de tabela no script

```rb
# retorna o nome do campo
FieldName 
Let vFieldName = FieldName(1, 'Dados_1');

# retorna o número do campo
FieldNumber 
Let vFieldNumber = FieldNumber('Valor', 'Dados_1');

# retorna o número de campos (colunas)
NoOfFields
Let vNoOfFields = NoOfFields('Dados_1');

# retorna o número de registros (linhas)
NoOfRows
Let vNoOfRows = NoOfRows('Dados_1');

# retorna o número de tabelas carregadas
NoOfTables
Let vNoOfTables = NoOfTables();

# retorna o nome da tabela pelo seu índice
TableName
Let vTableName = TableName(1);

# retorna o índice da tabela tendo o seu nome
TableNumber
Let vTableNumber = TableNumber('Dados_1');
```

# Extensões

Site Qlik Garden possui os desenvolvimentos para download
Instalar na pasta do Qlik >> Sense >> Extensions >> NewExtensionNameFolder

# Ligando campos

Pode ser utilizada a função Hash128 e Hash256 para criar uma combinação de vários campos sem duplicidade
- Ideal para armazenar chaves
- `Hash128(campo1,campo2,campoN)`
No final é possível fazer o autonumber para reduzir espaço na memória

Para ligar duas tabelas fatos, se não houver a mesma quantidade de campos em ambas, os campos únicos podem ser criados com `Null() as Campo` de forma ao Qlik ligar automaticamente as duas tabelas
- Também pode ser forçada uma ligação com o comando `CONCATENATE`

Para carregar uma amostra:
- `First 10 Load * FROM ...;`

### Qualify

Usado para que o Qlik não entenda como iguais dois campos de duas tabelas com mesmo nome
`Qualify *`, `Qualify Data`, `Unqualify Store`

Chevron também é conhecido como **divisa** `<>` ou **aspas angulares**
