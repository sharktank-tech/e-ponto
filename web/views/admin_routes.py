from flask import Blueprint, render_template, request, redirect, url_for, flash
from web.modules.models import db, Ponto, Users
from flask_login import login_required, logout_user, current_user

admin_blueprint = Blueprint('admin', __name__, template_folder='templates/admin')


# Rota principal do painel de administração
@admin_blueprint.route('/admin')
@login_required
def admin_dashboard():
    products = Ponto.query.all()
    users = Users.query.all()
    return render_template('admin/dashboard.html', products=products, users=users)


# Gerenciamento de Usuários
@admin_blueprint.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = Users(username=username, email=email)
        new_user.set_password(password)  # Ajuste para hash da senha
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário adicionado com sucesso!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/add_user.html')

@admin_blueprint.route('/admin/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('admin.admin_dashboard'))


@admin_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("Logout bem-sucedido!", "success")
    return redirect(url_for('main.login'))