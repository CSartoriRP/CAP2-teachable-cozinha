# 🥄🍳 Projeto FIAP — Classificação de Utensílios (Teachable Machine)

Guia **simples e sem fricção** para baixar imagens do **Pexels** e organizar as pastas para treinar no **Teachable Machine**.

> **Importante:** este passo a passo **não exige** variáveis de ambiente. A chave do Pexels será lida de um **arquivo texto** dentro da pasta do projeto.

---

## ✅ O que você precisa
- **Windows** com **Python 3.10+** (confira: `python --version`)
- Uma **API Key do Pexels** (grátis): https://www.pexels.com/api/

---

## 🚀 Passo a passo (copiar e colar)

### 1) Crie a pasta do projeto e entre nela
Abra o **PowerShell** e execute:
```powershell
mkdir C:\teachable-utensilios
cd C:\teachable-utensilios
```

### 2) Baixe estes arquivos e coloque nesta pasta
- `coletar_imagens_pexels.py`
- `requirements.txt`
- `.gitignore` (opcional, para não subir a pasta `data/` ao GitHub)
- `PEXELS_API_KEY.txt` (adicione sua chave)

*(Se estiver vendo este README no GitHub, clique em cada arquivo e depois em **Download raw file**.)*

### 3) Edite o arquivo com sua chave do Pexels
Abra o arquivo `PEXELS_API_KEY.txt` e cole **apenas** a sua chave.  
Exemplo:  
```
SUA_CHAVE_DO_PEXELS_AQUI
```

### 4) Crie/ative o ambiente Python e instale dependências
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```
> Se aparecer um erro de política ao ativar a venv, rode **apenas nesta janela** e ative de novo:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
> .\.venv\Scripts\Activate.ps1
> ```

### 5) Baixe as imagens (3 classes: talheres, panelas, utensilios_preparo)
```powershell
python -u coletar_imagens_pexels.py
```
O script vai criar a estrutura:
```
data/
 ├─ talheres/            ├─ panelas/              ├─ utensilios_preparo/
 │   ├─ train/           │   ├─ train/            │   ├─ train/
 │   └─ test/            │   └─ test/             │   └─ test/
```

### 6) Treinar no Teachable Machine
1. Acesse https://teachablemachine.withgoogle.com/  
2. Novo projeto → **Classificação de Imagem** → **Imagem Padrão**  
3. Crie as classes **talheres**, **panelas** e **utensilios_preparo**  
4. **Importe as pastas `train`** de cada classe  
5. Treine e teste manualmente com imagens das pastas `test`

---

## 🧯 Solução de problemas rápida
- **“Chave Pexels não encontrada”** → garanta que **PEXELS_API_KEY.txt** está na **mesma pasta** do `coletar_imagens_pexels.py` e tem **apenas** a chave (sem espaços extras).
- **“venv não ativa”** → rode: `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process` e ative de novo.
- **Poucas imagens** → aumente `IMAGENS_POR_CLASSE` no topo do script e/ou rode novamente.

---

## 📚 Créditos e referências
- [Teachable Machine](https://teachablemachine.withgoogle.com/)
- [Pexels API](https://www.pexels.com/api/)
