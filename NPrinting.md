  
# Excel
- Na conexão com a aplicação do Qlik é possível definir uma periodicidade para fazer reload dos metadados
- Para saber o tamanho da imagem que estará no relatório, pode visualizar o tamanho que está no qlik pelo "inspecionar" (F12) do navegador e ver as dimensões do gráfico/KPI
- Nomes dos relatórios não possuem compatibilidade com UTF8, dessa forma deve ser escrito sem acentuação
- Níveis permitem fazer total e subtotal por dimensões, o cálculo é feito na célula para somar as linhas acima
- Páginas permitem criar "abas" para cada valor em uma dimensão (como ano p.ex.)
- Para criar gráficos do excel, usar os dados de tabela como modelo e inserir "delete_row" para apagar a última linha
- NPrinting atualiza automaticamente para tabelas dinâmicas vinculadas a uma tabela que tem a origem em "tabela" do Qlik

# Word
- No word para forçar uma nova página por ano por exemplo, utilizar o componente *Níveis* e antes do fim do nível colocar um *Quebra de Página*
- Possível colocar uma marca d'água para o documento que se repetirá nas páginas seguintes dos Níveis

# Power Point
- Opção de *Page* para criar slides que repetem o padrão por uma dimensão (Ano/Mês por exemplo)
- Na caixa de propriedades podem ser definidos quantos slides estão dentro do nível de *Page* em **Slides** (ex, 1-3)
- Possibilidade de inserir o gráfico padrão do Office do Power Point com os dados no Excel que é gerado vinculado pelo software (mesma lógica de formatação do excel)

# Html
- Um relatório criado em HTML pode ser adicionado ao corpo do e-mail
- Porém não pode conter códigos externos como css personalizado
- Fica dentro de opções do E-mail >> Adicionar anexo e escolhe o HTML já montado previamente
- Site *codepen* possui vários modelos de infográficos de html para uso, basta baixar o zip e susbstituir os campos pelos do NPrinting
# Qlik Entity
- Pode enviar uma Sheet (pasta) ou outro objeto como CSV e também imagem (JPEG, PNG)

# Salvar em pasta
- Cria conexão com uma pasta para ser o local de armazenar os CSVs gerados por uma tarefa

# Filtros
## Campos
- Filtros normais
	- Inserir um valor ou vários (um por linha)
	- Pode usar *selecionar excluídos* (seleção alternativa)
	- Override (sobrescrever), somente em casos para o filtro ser feito por cima dos filtros anteriores
- Filtro de número
	- Para o caso de um ano ou valor numérico
- Evaluate value
	- Avalia uma expressão do Qlik inserida, como `Year(Today())-2` (recuando para dois anos atrás)
	- Útil para datas móveis
- Advanced Search
	- Filtro para múltiplos valores e para caracteres curingas
	- Filtro de ano `>=2020<=2023`
	- Filtro com variável `>=2020<=$(Ano_Maximo)`
	- Pode ser feito um cálculo para trazer valores maiores que x  ` =Sum({<Ano_Ordem={"$(MAX(Ano_Ordem))">} Qtd_Vendas} > 3000000`
	- Ranking top 2 valores  ` =Rank(Sum({<Ano_Ordem={"$(MAX(Ano_Ordem))">} Qtd_Vendas}, 5) >= 2`
	- Filtro por nome `*L*` , `?a*`
	- Os filtros acumulados formam o **OU**
## Variáveis
- Substitui uma dimensão pelo valor de uma variável
- P.ex, uma categoria pode ser substituída por uma variável contendo ano(s)
- Usar o colchetes `[Ano_Ordem]`

## Condições
- Podem ser utilizadas em tarefas ou relatórios
- Se for em relatório apenas o relatório que apresentar erro não será enviado
- Pode ser atrelado a uma variável ou a se um gráfico possui valores

# Importação de usuário, grupos e filtros
- Feito por uma planilha padrão
- Pode atualizar usuários e cadastrador novos, assim como grupos e regras
- Pasta dentro do servidor para armazenar o xlsx
- Regra pode ser configurada para rodar em períodos agendados
- Pode rodar uma simulação da tarefa para checar o que foi feito antes da execução de fato