# 🤖 Automatizador de Adição de Certificados no LinkedIn

Este projeto contém um script de automação em Python, desenvolvido com a biblioteca **Selenium**, para adicionar múltiplos certificados e licenças a um perfil do LinkedIn de forma automática. A solução foi criada para otimizar o tempo de usuários que, como eu, realizaram diversos cursos e precisam atualizar seus perfis sem o trabalho manual e repetitivo de preencher cada formulário individualmente.

O script é projetado para ler uma lista de certificados de uma fonte de dados, conectar-se a uma sessão do navegador Chrome já logada no LinkedIn e preencher os formulários de adição de certificados um por um.

---

## 🚀 Funcionalidades Principais

-   **Parsing de Dados:** Processa uma string de texto com os dados dos certificados, extraindo automaticamente:
    -   Nome do Curso
    -   Mês de Emissão
    -   Ano de Emissão
    -   Competência Principal Associada
-   **Conexão a um Navegador Existente:** Conecta-se a uma instância do Google Chrome que já esteja em execução com o modo de depuração ativado. Isso evita a necessidade de fazer login pelo script, tornando o processo mais seguro e simples.
-   **Preenchimento Automático:** Navega até a página de adição de certificados e preenche todos os campos necessários do formulário, incluindo:
    -   Nome do certificado
    -   Organização emissora (com seleção inteligente da lista suspensa)
    -   Data de emissão (mês e ano)
    -   Competências (com seleção da lista de sugestões)
-   **Robustez e Tolerância a Falhas:**
    -   Utiliza esperas explícitas (`WebDriverWait`) para garantir que os elementos da página carreguem antes de interagir com eles.
    -   Inclui tratamento de exceções para lidar com erros em certificados específicos, permitindo que o script continue para o próximo sem interromper todo o processo.
    -   Gerencia pop-ups que podem aparecer após salvar um certificado.
-   **Pausas Estratégicas:** Adiciona intervalos (`time.sleep`) entre as ações para simular um comportamento mais humano e evitar bloqueios por parte do LinkedIn.

---

## 🛠️ Tecnologias Utilizadas

-   **Python 3.x**
-   **Selenium:** A principal ferramenta para automação de navegadores web.
-   **WebDriver Manager for Python:** Para gerenciar automaticamente o download do `ChromeDriver` necessário para o Selenium.
-   **Expressões Regulares (Regex):** Para a extração e o parsing dos dados dos certificados a partir de um texto bruto.

---

## ⚙️ Pré-requisitos

Antes de executar o script, certifique-se de que você tem o seguinte instalado:

1.  **Python 3:** Se não tiver, baixe-o em [python.org](https://www.python.org/downloads/).
2.  **Google Chrome:** O script foi desenvolvido para funcionar com o Chrome.
3.  **Bibliotecas Python:** Instale todas as dependências necessárias com um único comando:

    ```bash
    pip install selenium webdriver-manager
    ```

---

## 📖 Como Usar

Siga estes passos cuidadosamente para configurar e executar o projeto.

### Passo 1: Clonar ou Baixar o Repositório

Faça o download dos arquivos do projeto para o seu computador.

### Passo 2: Preparar os Dados dos Certificados

1.  Haverá um arquivo chamado `DADOS_CERTIFICADOS.py` no projeto.
2.  Abra este arquivo e edite a constante `DADOS_CERTIFICADOS`.
3.  Insira os dados dos seus certificados como uma única string de texto (usando aspas triplas `"""`). Cada certificado deve estar em uma nova linha, seguindo o formato exato:

    ```
    Nome do Curso · Turma MES/ANO - Competência Principal
    ```

    -   `MES` deve ser a abreviação de 3 letras do mês (JAN, FEV, MAR, etc.).
    -   `ANO` deve ter 4 dígitos.

    **Exemplo de preenchimento do arquivo `DADOS_CERTIFICADOS.py`:**

    ```python
    DADOS_CERTIFICADOS = """
        Excel Básico · Turma SET/2023 - Microsoft Excel
        Comunicação Efetiva · Turma OUT/2023 - Comunicação
        Liderança de Equipes de Alta Performance · Turma NOV/2023 - Liderança
        Power BI para Análise de Dados · Turma JAN/2024 - Microsoft Power BI
    """
    ```
### Passo 3: Configurar a Organização Emissora Padrão

**Atenção:** O script está pré-configurado para preencher "Enap" como a organização emissora para **todos** os certificados. Se seus certificados forem de outra instituição (como SENASP, SEST SENAT, UFPB, etc.), você precisa alterar isso diretamente no código.

1.  Abra o script principal (`automacao_linkedin.py`).
2.  Procure pela linha que contém `campo_org.send_keys("Enap")`.
3.  Altere o texto `"Enap"` para o nome da sua instituição.

    **Local no código para alteração:**
    ```python
    # ... (dentro do loop 'for i, cert in enumerate(certificados):')

          campo_org = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Ex.: Microsoft']")))
          
          # ----------------------------------------------------------------- #
          # --- ALTERE A LINHA ABAIXO COM O NOME DA SUA INSTITUIÇÃO --- #
          campo_org.send_keys("Enap") 
          # ----------------------------------------------------------------- #

          time.sleep(2.5)
          campo_org.send_keys(Keys.ARROW_DOWN)
    ```
    Por exemplo, se seus cursos foram na **SEST SENAT**, a linha ficaria assim:
    ```python
    campo_org.send_keys("SEST SENAT")
    ```

### Passo 4: Iniciar o Google Chrome em Modo de Depuração

Esta é a etapa mais importante. O script **não fará login por você**. Em vez disso, ele se conectará a um navegador que você já abriu e onde já está logado.

1.  Feche todas as janelas do Google Chrome.
2.  Abra o terminal ou prompt de comando do seu sistema operacional.
3.  Execute um dos comandos abaixo, dependendo do seu sistema, para abrir uma nova instância do Chrome que o script possa controlar:

    -   **Windows:**
        ```cmd
        "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebug"
        ```
        *(O caminho para `chrome.exe` pode variar se você o instalou em um local diferente).*

    -   **macOS:**
        ```bash
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
        ```

    -   **Linux:**
        ```bash
        google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
        ```

4.  Uma nova janela do Chrome será aberta. Nesta janela, **faça login no seu perfil do LinkedIn** normalmente.

### Passo 5: Atualizar a URL do Perfil no Script (Opcional)

O script principal (`automacao_linkedin.py`) possui uma variável `PROFILE_URL`. Se desejar, atualize-a para a URL do seu próprio perfil, embora o script navegue diretamente para a página de adição.

```python
# No script principal
PROFILE_URL = "[https://www.linkedin.com/in/seu-usuario-aqui/](https://www.linkedin.com/in/seu-usuario-aqui/)"
```

### Passo 6: Executar o Script de Automação

1.  Com o Chrome em modo de depuração aberto e logado no LinkedIn, abra um **novo** terminal ou prompt de comando.
2.  Navegue até a pasta onde você salvou os arquivos do projeto.
3.  Execute o script principal:
    ```bash
    python automacao_linkedin.py
    ```
4.  O script irá se conectar ao navegador. Ele pedirá que você pressione `Enter` para iniciar.
5.  Volte para a janela do Chrome e observe a mágica acontecer! O script começará a adicionar cada certificado da sua lista.

---
## ⚠️ Aviso Importante

-   **Use por sua conta e risco.** A automação de interações em plataformas de redes sociais pode violar seus Termos de Serviço.
-   O script inclui pausas (`time.sleep`) para tornar a automação menos agressiva, mas o uso excessivo ou rápido pode levar a restrições temporárias em sua conta do LinkedIn.
-   Os seletores de elementos da web (XPaths) podem mudar se o LinkedIn atualizar seu site. Se o script parar de funcionar, pode ser necessário atualizar esses seletores.

---

## 🔧 Estrutura do Código

-   **`automacao_linkedin.py` (Script Principal):** Contém toda a lógica de automação do Selenium. Ele inicializa o driver, itera sobre a lista de certificados e preenche os formulários.
-   **`DADOS_CERTIFICADOS.py`:** Arquivo de configuração onde você armazena os dados brutos dos certificados a serem adicionados.
-   **`parse_certificate_data` (Função):** Uma função utilitária dentro do script principal, responsável por ler a string de dados brutos e transformá-la em uma lista de objetos estruturados que o script pode usar.
