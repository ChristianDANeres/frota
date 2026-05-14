Upload de logos e imagens

- Limite de tamanho: 3 MB por arquivo.
- Tipos permitidos: png, jpg, jpeg, svg.
- Ao enviar, o servidor valida o arquivo e tenta redimensionar/comprimir imagens grandes usando Pillow (biblioteca `Pillow`).
- Se o redimensionamento falhar ou o arquivo permanecer maior que 3 MB, o upload será rejeitado com mensagem de erro.
- Imagens são salvas em: `app/static/uploads/cliente/<id>/logo_esquerdo.jpg` e `.../logo_direito.jpg`.

Requisitos:

Adicione `Pillow` ao ambiente do projeto (já listado em `requirements.txt`). Instale com:

```bash
.venv\Scripts\pip install -r requirements.txt
```

Observações:
- O servidor converte imagens para JPEG ao salvar e aplica compressão para reduzir tamanho.
- Você pode ajustar a resolução máxima (`1200x1200`) e qualidade (`quality=85`) no helper `app.routes.adm_routes._save_cliente_file`.
