
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
