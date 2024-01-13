# Spotify Bot

[![Presentation](https://99freelas.s3-sa-east-1.amazonaws.com/portfolios/imagens/original/1641617/a6877f2b-0d6b-4527-a3c9-d045cc611c61/screenshot.png?id=4029743&token=a6877f2b-0d6b-4527-a3c9-d045cc611c61&nome=screenshot&type=.png)](https://youtu.be/rXbHcNvs7ZM)

Bot que ouve playlists do Spotify e músicas especificas de playlists.

# Instalação

Segue script de instalação:

```
git clone https://github.com/riguima/spotify-bot
cd spotify-bot
pip install -r requirements.txt
```

Renomeie o arquivo `.base.config.toml` para `.config.toml` e altere as configurações `default` e `testing`.

- `TESTING` define qual configuração será utilizada, se `true` usa `testing`, caso contrário usa `default`.
- `BROWSERS_COUNT` define quantos navegadores simultaneos são abertos para ouvir as playlists.
- `DATABASE_URI` é a URL do banco de dados, exemplo com postgres: `postgresql://username:password@localhost:5432/database_name`.
- `EMAIL` e `PASSWORD` é o login para rodar os testes caso necessário.
- `PLAYLIST_URL` é a url da playlist que vai ser usada para testes.

Rode a aplicação com `python run_browsers.py && python main.py`
