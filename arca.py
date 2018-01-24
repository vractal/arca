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
