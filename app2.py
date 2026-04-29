import streamlit as st

st.set_page_config(page_title="Analisador de Setores", layout="wide")

# ==============================
# SETORES DA ROLETA
# ==============================

setores = {
    "Setor 1": [10, 5, 24, 16, 33, 1, 20, 14, 31],
    "Setor 2": [9, 22, 18, 29, 7, 28, 12, 35, 3],
    "Setor 3": [23, 8, 30, 11, 36, 13, 27, 6, 34, 17],
    "Setor 4": [25, 2, 21, 4, 19, 15, 32, 0, 26],
}

# ==============================
# FUNÇÕES
# ==============================

def setor_do_numero(numero):

    for nome, numeros in setores.items():

        if numero in numeros:
            return nome

    return None


def limpar_historico(texto):

    texto = texto.replace(" ", "")

    partes = texto.split(",")

    historico = []
    invalidos = []

    for parte in partes:

        if parte == "":
            continue

        try:

            n = int(parte)

            if 0 <= n <= 36:
                historico.append(n)

            else:
                invalidos.append(parte)

        except:
            invalidos.append(parte)

    return historico, invalidos


def analisar_setores(historico):

    # ==============================
    # PEGA APENAS OS 10 ÚLTIMOS
    # ==============================

    ultimos_10 = historico[-10:]

    # leitura da direita para esquerda
    leitura = list(reversed(ultimos_10))

    sequencia = []

    contagem = {
        setor: 0 for setor in setores
    }

    # ==============================
    # CONTAGEM DOS SETORES
    # ==============================

    for numero in leitura:

        setor = setor_do_numero(numero)

        sequencia.append({
            "numero": numero,
            "setor": setor
        })

        if setor:
            contagem[setor] += 1

    # ==============================
    # SETOR MAIS BATIDO
    # ==============================

    maior_batida = max(contagem.values())

    setores_mais_batidos = [

        setor for setor, qtd in contagem.items()

        if qtd == maior_batida
    ]

    # ==============================
    # AUSÊNCIAS
    # ==============================

    ausencias = {}

    for setor in setores:

        # ausência atual
        ausencia_atual = 0

        for item in sequencia:

            if item["setor"] == setor:
                break

            ausencia_atual += 1

        # maior ausência recente
        maior_ausencia = 0
        ausencia_temp = 0
        encontrou_primeiro = False

        for item in sequencia:

            if item["setor"] == setor:

                if encontrou_primeiro:

                    maior_ausencia = max(
                        maior_ausencia,
                        ausencia_temp
                    )

                encontrou_primeiro = True
                ausencia_temp = 0

            else:

                if encontrou_primeiro:
                    ausencia_temp += 1

        ausencias[setor] = {
            "atual": ausencia_atual,
            "maior": maior_ausencia
        }

    # ==============================
    # RANKING
    # ==============================

    ranking = sorted(
        contagem.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # ==============================
    # SETOR MAIS AUSENTE
    # ==============================

    setor_mais_ausente = max(
        ausencias.items(),
        key=lambda x: x[1]["atual"]
    )

    return {

        "ultimos_10": ultimos_10,
        "leitura": leitura,
        "sequencia": sequencia,
        "contagem": contagem,
        "ranking": ranking,
        "maior_batida": maior_batida,
        "setores_mais_batidos": setores_mais_batidos,
        "ausencias": ausencias,
        "setor_mais_ausente": setor_mais_ausente
    }


# ==============================
# INTERFACE
# ==============================

st.title("Estratégia: Análise de Setores")

st.write(
    "Leitura feita apenas com os 10 últimos números."
)

st.info(
    "Cole o histórico separado por vírgula.\n"
    "Exemplo: 14,0,10,26,27,3,18,6,14,25"
)

historico_texto = st.text_input(
    "Histórico:",
    "14,0,10,26,27,3,18,6,14,25"
)

if st.button("Analisar"):

    historico, invalidos = limpar_historico(
        historico_texto
    )

    if invalidos:

        st.warning(
            f"Valores inválidos ignorados: {invalidos}"
        )

    if len(historico) < 10:

        st.error(
            "Digite pelo menos 10 números válidos."
        )

    else:

        resultado = analisar_setores(historico)

        st.divider()

        # ==============================
        # ÚLTIMOS 10
        # ==============================

        st.subheader("Últimos 10 números")

        st.write(resultado["ultimos_10"])

        st.subheader("Leitura direita para esquerda")

        st.write(resultado["leitura"])

        st.divider()

        # ==============================
        # SEQUÊNCIA
        # ==============================

        st.subheader("Sequência por setor")

        for item in resultado["sequencia"]:

            st.write(
                f"- {item['numero']} → {item['setor']}"
            )

        st.divider()

        # ==============================
        # CONTAGEM
        # ==============================

        st.subheader("Contagem por setor")

        col1, col2, col3, col4 = st.columns(4)

        colunas = [col1, col2, col3, col4]

        for i, (setor, numeros) in enumerate(
            setores.items()
        ):

            with colunas[i]:

                st.metric(
                    label=setor,
                    value=resultado["contagem"][setor]
                )

                st.write("Cobertura:")
                st.write(numeros)

        st.divider()

        # ==============================
        # RANKING
        # ==============================

        st.subheader("Ranking dos setores")

        for posicao, (setor, qtd) in enumerate(
            resultado["ranking"],
            start=1
        ):

            st.write(
                f"{posicao}º — "
                f"{setor}: {qtd} batida(s)"
            )

        st.divider()

        # ==============================
        # SETOR DOMINANTE AUSENTE
        # ==============================

        st.subheader("Setor dominante ausente")

        for setor in resultado["setores_mais_batidos"]:

            st.success(
                f"{setor}: "
                f"{resultado['maior_batida']} batida(s)"
            )

            st.write(
                f"Ausência atual: "
                f"{resultado['ausencias'][setor]['atual']} jogada(s)"
            )

            st.write(
                f"Maior ausência recente: "
                f"{resultado['ausencias'][setor]['maior']} jogada(s)"
            )

            st.write("Cobertura:")

            st.write(setores[setor])

        st.divider()

        # ==============================
        # SETOR MAIS AUSENTE
        # ==============================

        st.subheader("Setor mais ausente")

        nome_setor_ausente = resultado[
            "setor_mais_ausente"
        ][0]

        dados_ausente = resultado[
            "setor_mais_ausente"
        ][1]

        st.warning(
            f"{nome_setor_ausente} está ausente há "
            f"{dados_ausente['atual']} jogada(s)"
        )

        st.write("Cobertura:")

        st.write(setores[nome_setor_ausente])

        st.write(
            f"Maior ausência recente: "
            f"{dados_ausente['maior']} jogada(s)"
        )

        st.divider()

        # ==============================
        # AUSÊNCIA DE TODOS
        # ==============================

        st.subheader("Ausência de todos os setores")

        for setor in setores:

            st.write(

                f"- {setor}: "
                f"ausência atual "
                f"{resultado['ausencias'][setor]['atual']} jogada(s) | "
                f"maior ausência recente "
                f"{resultado['ausencias'][setor]['maior']} jogada(s)"
            )

        st.divider()

        # ==============================
        # RESUMO
        # ==============================

        st.subheader("Resumo rápido")

        st.write(
            "Setor(es) dominante(s):",
            resultado["setores_mais_batidos"]
        )

        for setor in resultado["setores_mais_batidos"]:

            st.write(
                f"{setor} → "
                f"{resultado['maior_batida']} batida(s) | "
                f"ausência atual: "
                f"{resultado['ausencias'][setor]['atual']}"
            )

        st.write("")

        st.write(
            f"Setor mais ausente: "
            f"{nome_setor_ausente} "
            f"({dados_ausente['atual']} jogada(s) sem bater)"
        )
