from flask import render_template, redirect, url_for, session, flash, request, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from web.modules.models import db, Ponto, Users
from web.modules.data_hora import obter_data_hora_br, formato_brasileiro
from web.modules.can_register import verificar_se_pode_registrar, verifica_limite_marcacoes
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
import logging
from web.modules.calc_horas import calcular_horas_salario
from web.modules.enviar_email import enviar_email

main_blueprint = Blueprint('main', __name__)

# Configurar o logging
logging.basicConfig(level=logging.ERROR)

@main_blueprint.route('/')
@login_required
def home():
    # Busca os dados do ponto do usuário atual
    point_data = Ponto.query.filter_by(user_id=current_user.id).first()
    print(f"corrent user={current_user}")
    print(f"point data={point_data}")

    hoje = obter_data_hora_br()

    # Formatar os dados do ponto
    formatted_point_data = {
        'entrada': str(point_data.entrada)[:19] if point_data and point_data.entrada else 'Não registrado',
        'pausa': str(point_data.pausa)[:19] if point_data and point_data.pausa else 'Não registrado',
        'retorno': str(point_data.retorno)[:19] if point_data and point_data.retorno else 'Não registrado',
        'saida': str(point_data.saida)[:19] if point_data and point_data.saida else 'Não registrado'
    }

    # Verificar se todos os registros do dia estão preenchidos
    all_registered_today = all(
        value != 'Não registrado' and value[:10] == hoje
        for value in formatted_point_data.values()
    )

    # Verificar se o usuário pode registrar
    can_register = verificar_se_pode_registrar(current_user.id) and not all_registered_today

    return render_template(
        'main/index.html',
        username=session.get('username', current_user.username),
        user_id=current_user.id,
        point_data=formatted_point_data,
        can_register=can_register
    )


# Rota para a página de login
@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('senha')

        if not email or not password:
            flash("Por favor, preencha todos os campos.", "danger")
            logging.error("Tentativa de login falhou: campos vazios.")
            return redirect(url_for('main.login'))

        user = Users.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Credenciais inválidas. Tente novamente.", "danger")
            logging.error(f"Tentativa de login falhou para o e-mail: {email}.")
            return redirect(url_for('main.login'))

        login_user(user)
        flash("Login realizado com sucesso!", "success")
        logging.info(f"Usuário {user.username} logado com sucesso.")
        return redirect(url_for('main.home'))

    return render_template('conta/login.html')

# Rota para logout
@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Rota para a página de cadastro
@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('senha')

        if not username or not email or not password:
            flash("Todos os campos são obrigatórios.", "danger")
            return redirect(url_for('main.register'))

        existing_user = Users.query.filter(
            (Users.username == username) | (Users.email == email)
        ).first()

        if existing_user:
            flash("Usuário ou e-mail já existe.", "danger")
            return redirect(url_for('main.register'))

        try:
            new_user = Users(username=username, email=email, is_admin=False)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
            return redirect(url_for('main.login'))
        except IntegrityError as e:
            db.session.rollback()
            flash("Erro ao salvar usuário. Por favor, tente novamente.", "danger")
            logging.error(f"Erro de integridade: {str(e)}")
        except Exception as e:
            flash(f"Erro inesperado: {str(e)}", "danger")
            logging.error(f"Erro ao criar usuário: {str(e)}")

    return render_template('conta/register.html')

# Rota pra a pagna da conta
@main_blueprint.route('/conta')
@login_required
def conta():
    try:
        # Recupera o usuário logado
        user = current_user  # Mantenha o objeto 'user' como o 'current_user' inteiro
        horas_trabalhadas, salario = calcular_horas_salario(user.id)

        # Verifica se o objeto 'user' contém os atributos esperados
        username = user.username if user.username else 'Usuário desconhecido'
        email = user.email if user.email else 'E-mail não disponível'
        admin = user.is_admin if hasattr(user, 'is_admin') else False

        # Recupera todas as marcações de ponto do usuário
        pontos = db.session.query(Ponto).filter(Ponto.user_id == user.id).all()

        # Renderiza o modelo com os dados do usuário
        return render_template(
            'conta/conta.html',
            user=user,
            admin=admin,
            id=user.id,
            username=username,
            email=email,
            horas_trabalhadas=horas_trabalhadas,
            salario=salario,
            pontos=pontos  # Passa as marcações de ponto para o template
        )
    except Exception as e:
        flash("Erro ao acessar os dados da conta. Tente novamente.", "danger")
        print(f"Erro ao acessar dados da conta: {e}")

    # Redireciona para a página inicial em caso de erro
    return redirect(url_for('main.home'))


# Rota pro envio do relatorio
@main_blueprint.route('/relatorio')
@login_required
def relatorio():
    try:
        destinatario = current_user.email
        if not destinatario:
            flash("E-mail do usuário não encontrado.", "danger")
            return redirect(url_for('main.home'))

        assunto = 'Relatório'
        corpo = "dados"

        # Enviar e-mail
        enviar_email(destinatario, assunto, corpo)
        flash("Relatório enviado com sucesso!", "success")

        return redirect(url_for('main.home'))

    except Exception as e:
        flash(f"Erro ao enviar o relatório: {str(e)}", "danger")
        print(f"Erro ao enviar e-mail: {e}")
        return redirect(url_for('main.home'))


# Rota para registrar as marcações
@main_blueprint.route('/registrar_ponto', methods=['POST'])
@login_required
def registrar_ponto():

    user_id = current_user.username

    # Verificar se o usuário já atingiu o limite de marcações para hoje
    if verifica_limite_marcacoes(user_id):
        flash('Você já atingiu o limite de marcações para hoje.', 'warning')
        logging.info(f'Usuário {user_id} já atingiu o limite de marcações para hoje.')
        return redirect(url_for('index'))

    try:
        # Recuperar o ponto atual do usuário usando SQLAlchemy
        ponto_atual = db.session.query(Ponto).filter(Ponto.user_id == user_id, Ponto.entrada.startswith(formato_brasileiro()[:10])).first()

        if ponto_atual is None:
            # Inserir um novo registro de ponto se não existir
            ponto_atual = Ponto(user_id=user_id, entrada=None, pausa=None, retorno=None, saida=None)
            db.session.add(ponto_atual)
            db.session.commit()

        # Determinar o tipo de registro com base nos campos preenchidos
        if not ponto_atual.entrada:
            tipo_registro = 'entrada'
        elif not ponto_atual.pausa:
            tipo_registro = 'pausa'
        elif not ponto_atual.retorno:
            tipo_registro = 'retorno'
        elif not ponto_atual.saida:
            tipo_registro = 'saida'
        else:
            flash('Todas as marcações para hoje já foram feitas.', 'info')
            return redirect(url_for('index'))

        # Registrar o horário atual no campo correspondente
        data_hora_registro = formato_brasileiro()  # Supondo que retorna 'DD/MM/YYYY HH:MM:SS'
        logging.info(f"Data e hora do registro: {data_hora_registro}")

        # Atualizar o registro de ponto no banco de dados
        if tipo_registro == 'entrada':
            ponto_atual.entrada = data_hora_registro
        elif tipo_registro == 'pausa':
            ponto_atual.pausa = data_hora_registro
        elif tipo_registro == 'retorno':
            ponto_atual.retorno = data_hora_registro
        elif tipo_registro == 'saida':
            ponto_atual.saida = data_hora_registro

        # Commit para salvar a alteração
        db.session.commit()

        flash(f'{tipo_registro.capitalize()} registrada com sucesso!', 'success')
        logging.info(f'{tipo_registro.capitalize()} registrada com sucesso para o usuário {user_id}.')
    except Exception as e:
        logging.error(f'Erro ao registrar ponto para o usuário {user_id}: {e}, entrada={ponto_atual.entrada}')
        flash('Erro ao registrar o ponto. Tente novamente mais tarde.', 'danger')

    return redirect(url_for('main.home'))

