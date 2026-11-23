# Pathfinding e Otimização de Energia:Uma Abordagem Interativa com o Algoritmo A*

> **Trabalho Acadêmico**  
> **Disciplina:** Inteligência Artificial  
> **Curso:** Engenharia de Computação — Universidade Federal de Mato Grosso (UFMT)  
> **Docente:** Dr. Gustavo Post Sabin  

---

## 📌 Apresentação do Repositório

---

## 👥 Integrantes do Grupo

| Nome Completo | RGA |
| :--- | :--- |
| **Carlos Daniel Santana Cunha** | *202421901003* |
| **Luciano Tadeu Simões Simplicio Junior** | *202421901044* |
| **Matheus Mesquita Yukishita** | *202421901048* |

---

## 📁 Estrutura do Projeto

A organização dos diretórios do repositório está estruturada da seguinte forma:

---

## 🚀 Como Executar o Projeto


---

### 2. Relatório do Projeto (LaTeX)

#### Opção A: PDF Pré-compilado
O relatório técnico já se encontra compilado e pronto para leitura no caminho:
- `relatorio/main.pdf`

#### Opção B: Compilando o Código-Fonte LaTeX
##### Pré-requisitos
- Uma distribuição LaTeX instalada (ex: [TeX Live](https://www.tug.org/texlive/), [MiKTeX](https://miktex.org/) ou [MacTeX](https://www.tug.org/mactex/)).
- Editor de preferência (ex: **VS Code** com extensão *LaTeX Workshop*, **Texmaker**, ou envio dos arquivos da pasta `relatorio/` para o **Overleaf**).

##### Passo a Passo (Linha de Comando)
1. Acesse o diretório do relatório:
   ```bash
   cd relatorio
   ```
2. Compile o documento utilizando `latexmk` ou `pdflatex`:
   ```bash
   latexmk -pdf main.tex
   ```
   *ou*
   ```bash
   pdflatex main.tex
   bibtex main
   pdflatex main.tex
   pdflatex main.tex
   ```
3. O arquivo final compilado será gerado em `relatorio/main.pdf`.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem de Documentação:** [LaTeX](https://www.latex-project.org/) (Modelo abnTeX2 / FAENG UFMT)
- **Controle de Versão:** Git & GitHub
