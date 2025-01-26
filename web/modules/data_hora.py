from datetime import datetime
import pytz

# Define o fuso horário de Brasília
fuso_horario_br = pytz.timezone('America/Sao_Paulo')

# Formata a data e hora no padrão brasileiro com o fuso horário
def formato_brasileiro():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

def obter_data_hora_br():
    return datetime.now(fuso_horario_br).strftime('%d/%m/%Y')

def data_hora_br_registro():
    return datetime.now(fuso_horario_br).strftime('%d/%m/%Y %H:%M:%S')