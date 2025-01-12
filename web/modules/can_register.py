from web.modules.data_hora import formato_brasileiro
from web.modules.models import db, Ponto
import logging

# Configurar o logging
logging.basicConfig(level=logging.ERROR)

def verificar_se_pode_registrar(user_id):
    """
    Verifica se o usuário pode registrar mais pontos no dia atual.
    """
    hoje = formato_brasileiro()[:10]  # Extrai apenas a data no formato 'DD/MM/YYYY'
    print(f"verificar_se_pode_registrar - Data de hoje: {hoje}")

    try:
        ponto = Ponto.query.filter(
            Ponto.user_id == user_id,
            Ponto.entrada.startswith(hoje)  # Verifica se a data de entrada começa com 'hoje'
        ).first()

        if not ponto:
            logging.info("Nenhuma marcação encontrada para hoje. Pode registrar.")
            return True

        # Verifica as marcações (entrada, pausa, retorno, saída)
        if all([ponto.entrada, ponto.pausa, ponto.retorno, ponto.saida]):
            logging.info(f"Limite de marcações atingido para {user_id} no dia {hoje}.")
            return False

        logging.info("Ainda há marcações disponíveis para registrar.")
        return True

    except Exception as e:
        logging.error(f"Erro ao verificar registro: {e}")
        return False


def verifica_limite_marcacoes(user_id):
    """
    Verifica se todas as marcações do dia já foram registradas para o usuário.
    """
    hoje = formato_brasileiro()[:10]  # Extrai apenas a data no formato 'DD/MM/YYYY'
    print(f"verifica_limite: {hoje}")

    try:
        ponto = Ponto.query.filter(
            Ponto.user_id == user_id,
            Ponto.entrada.startswith(hoje)  # Verifica se a data de entrada começa com 'hoje'
        ).first()

        if ponto:
            logging.info(f"Marcações retornadas para {hoje}: {ponto.entrada}, {ponto.pausa}, {ponto.retorno}, {ponto.saida}")
            todas_marcacoes = all(getattr(ponto, coluna) is not None for coluna in ['entrada', 'pausa', 'retorno', 'saida'])
            return todas_marcacoes
        else:
            logging.info("Nenhuma marcação encontrada para hoje.")
        return False

    except Exception as e:
        logging.error(f"Erro ao verificar limite de marcações: {e}")
        return False
