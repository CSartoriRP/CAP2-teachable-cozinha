# 🥄🍳 Projeto FIAP – Classificação de Utensílios de Cozinha

Este projeto mostra como **coletar imagens automaticamente**, treinar um modelo no **Teachable Machine** e testar em lote.

---

## 📌 Estrutura do Projeto

```
teachable-utensilios/
├── coletar_imagens_pexels.py      # Script de coleta de imagens
├── TM_Teste_em_Lote_Simples.ipynb # Notebook Colab para teste em lote
├── requirements.txt               # Dependências do Python
├── data/                          # Estrutura criada pelo script
│   ├── talheres/{train,test}
│   ├── panelas/{train,test}
│   └── utensilios_preparo/{train,test}
└── docs/                          # Relatório e prints
```

---

## 🚀 Passo 1 – Preparar Ambiente

1. Instale **Python 3.10+**  
2. Crie uma **API Key** no [Pexels](https://www.pexels.com/api/)  
3. No **PowerShell**, salve sua chave:
   ```powershell
   setx PEXELS_API_KEY "SUA_CHAVE_AQUI"
   ```

4. Crie e ative a **venv**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Instale dependências:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 📸 Passo 2 – Coletar Imagens

Execute:
```powershell
python -u coletar_imagens_pexels.py
```

➡️ O script vai:
- Buscar imagens no Pexels
- Remover duplicadas
- Separar em `train` (80%) e `test` (20%)

Resultado:  
```
data/
 ├── talheres/train + test
 ├── panelas/train + test
 └── utensilios_preparo/train + test
```

---

## 🧠 Passo 3 – Treinar no Teachable Machine

1. Acesse [Teachable Machine](https://teachablemachine.withgoogle.com/)  
2. Crie projeto → **Classificação de Imagem** → **Imagem Padrão**  
3. Crie 3 classes: `talheres`, `panelas`, `utensilios_preparo`  
4. Importe as pastas /train de cada classe  
5. Treine e ajuste parâmetros (épocas, batch, learning rate)  
6. Teste manualmente com imagens da pasta /test  

---

## 📊 Passo 4 – Teste em Lote (opcional)

1. Exporte o modelo no formato **Keras (.h5)**  
2. Abra o Colab e rode o notebook [`TM_Teste_em_Lote_Simples.ipynb`](TM_Teste_em_Lote_Simples.ipynb)  
3. Faça upload de:
   - `keras_model.h5`
   - `labels.txt`
   - `data.zip` (compacte sua pasta `data/`)  

O notebook gera:
- **Acurácia total**
- **Acurácia por classe**
- Arquivos `predicoes.csv` e `relatorio_metricas.txt`

---

## 📚 Referências
- [Teachable Machine](https://teachablemachine.withgoogle.com/)
- [API Pexels](https://www.pexels.com/api/)
