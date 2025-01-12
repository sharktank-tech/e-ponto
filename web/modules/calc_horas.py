from datetime import datetime
import logging
from collections import defaultdict
from flask_login import current_user
from web.modules.models import Ponto
from web import db  # Substitua pelo contexto correto do banco de dados

def calcular_horas_salario(user_id):
    try:
        # Validando o usuário atual
        if not current_user.is_authenticated:
            logging.error("Usuário não autenticado tentando calcular horas e salário.")
            return 0, 0

        # Recuperando registros de entrada e saída
        registros = db.session.query(Ponto.entrada, Ponto.saida).filter(Ponto.user_id == user_id).all()

        # Dicionário para armazenar horas por dia
        horas_por_dia = defaultdict(float)

        for entrada, saida in registros:
            if entrada and saida:
                try:
                    # Convertendo strings de data para objetos datetime
                    entrada_hora = datetime.strptime(entrada, '%d/%m/%Y %H:%M:%S')
                    saida_hora = datetime.strptime(saida, '%d/%m/%Y %H:%M:%S')

                    # Calculando as horas trabalhadas no dia
                    horas_trabalhadas = (saida_hora - entrada_hora).total_seconds() / 3600  # Convertendo para horas

                    # Somando as horas ao dicionário, agrupando por data
                    dia = entrada_hora.date()  # Obtém a data sem hora
                    horas_por_dia[dia] += horas_trabalhadas

                except ValueError as e:
                    logging.error(f"Erro ao converter data/hora para o user_id {user_id}: {e}")

        # Calculando o total de horas e salário
        total_horas = sum(horas_por_dia.values())
        taxa_hora = 17.0  # Exemplo de taxa horária (pode ser configurável)
        salario = total_horas * taxa_hora

        # Retornando as horas trabalhadas e o salário calculado
        return round(total_horas, 2), round(salario, 2)

    except Exception as e:
        logging.error(f"Erro ao calcular horas e salário para o user_id {user_id}: {e}")
        return 0, 0