# 🧬 Jogo da Vida de Conway — Simulação Interativa com Interface Gráfica

Este projeto implementa uma versão moderna e interativa do clássico **Jogo da Vida de Conway**, com interface gráfica (`Tkinter`), visualização em tempo real, análise gráfica das células vivas ao longo do tempo e exportação de resultados em PNG e GIF.

---

## 🎯 Objetivo

Simular a evolução de padrões celulares em um autômato bidimensional, com controle total por parte do usuário, métricas visuais e ferramentas educacionais úteis para ensino, experimentação e apresentação científica.

---

## ✨ Funcionalidades

- ✅ Interface gráfica moderna com `Tkinter`
- 🎨 Visualização com `matplotlib` e colormap `viridis`
- 🖱️ Edição manual do grid com cliques do mouse
- 🔁 Botões para iniciar, pausar, reiniciar e aleatorizar a simulação
- 🌀 Inserção de padrões clássicos como **Glider** e **Pulsar**
- 📊 Geração automática de gráfico com **células vivas por geração**
- 🖼️ Exportação do gráfico em `grafico.png`
- 🎞️ Exportação da simulação em `conway_simulation.gif` (opcional)
- ✔️ Código limpo, comentado e fácil de modificar

---

## 📷 Capturas de Tela

### Grid com Padrão Glider em Execução

![Simulação](https://raw.githubusercontent.com/CarlosHenrique/conway-simulator/main/screenshots/simulacao_exemplo.png)

### Gráfico Gerado ao Final da Simulação

![Gráfico](https://raw.githubusercontent.com/CarlosHenrique/conway-simulator/main/screenshots/grafico_exemplo.png)

---

## 💻 Requisitos

Certifique-se de ter o Python 3.10+ instalado.  
Instale as dependências com:

```bash
pip install numpy matplotlib seaborn imageio
