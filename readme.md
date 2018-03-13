
Este projeto tem o objetivo facilitar a criação de um arquivo de filmes (chamado de "Arca") a serem guardados para facilitar o compartilhamento e garantir sua acessibilidade numa era pós-pirataria.

Também, num segundo momento, permitir o  uso de tags para encontrar novos filmes do interesse do usuário, indicações diretas entre usuarios e indiretas dadas pelo próprio sistema. Também permitir criação de listas. (v2.0)

Requisitos funcionais

1. O Sistema deve manter configurações e log de alterações por determinado usuario, a partir de um cadastro com:
* Nome de usuario
* Senha
* Email

2. O Sistema deve guardar informações dos filmes salvos e pesquisados em seu banco de dados, afim de evitar chamados de api desnecessários. Deve informar também se o filme está salvo na lista(arca) ou não, e se está salvo em um dos diretorios (o arquivo em si).



3. O sistema deve guardar informações de quem adicionou determinado filme a lista, e quando. Salvar também quando e qual foi a pesquisa que adicionou determinado filme a DB. Deve apresentar uma opção para "voto", ou "+1", de reafirmação a filmes já adicionados. 

4. Listar usuarios e quais filmes adicionaram.

5. O sistema deve possuir front-end simples que possibilite acesso a todos recurso e apresentação dos dados, interagindo com o backend por meio de uma api.



"""o que? Inputar filmes, tags e comentarios. Ver filmes listados, numa lista de todos os filmes, por ordem de vezes que foi adicionado, e por tags.
quem? Usuario.
como? logando no site, inserindo no site um filme, se nao ta no banco de dados ele puxa da api de filmes, se tiver, ele adiciona mais um voto.
quando? Lista sempre. Facil acesso a inputar filme.
porque? ver filmes para guardar na arca (baixar para garantir). Segundo momento, recomendações



perguntas a fazer para a DB:
quais os filmes que estao na arca? quantas pessoas votaram em cada um?
quais as tags colocadas (total e em determinado filme)? quantas pessoas colocaram cada uma em determinado filme?
quais sao os filmes de determinada tag?
quais filmes determinado usuario votou?
determinado filme ja esta baixado? onde? qual o arquivo?



Usuario
nome
senha
email
filmes adicionados


filme
nome
data do release


arquivo?
nome
localizacao
tamanho
formato
idioma
legendas

arca

tags
nome


comentario/# REVIEW:
titulo
nome"""



#passo 1: api requests
