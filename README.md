# medicar

Como de padrão nos projetos Django segue o arquivo requeriments.txt, para que sejam instaladas as dependencias do projeto. Foi utilizado o banco de dado Postgres, com o usuario e senha padrão, "postgres";

Se faz necessário rodar o comando createsuperuser, para a criação de um usuário para o acesso a parte administrativa do django (Django Admin), assim tendo acesso aos cadastrados de médicos e agenda, como proposto no teste.

Para realizar o uso da API, basta acessar as seguintes rotas:

GET /agendas/ -> Para a listagem de agendas

GET /consultas/ -> Para a listagem de consultas

POST /consultas/ -> Para a marcação de consultas

*Parametros do POST de consultas
{
  "agenda_id": 1,
  "horario": "14:15"
}*

DELETE /consultas/<consulta_id> -> Para desmarcar consultas

