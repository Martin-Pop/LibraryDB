from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.main.service_container import loan_service, customer_service, copy_service
from src.main.utils import parse_db_exception
from src.models.entities import CopyStatus

loan_bp = Blueprint('loans', __name__, url_prefix='/loans')


@loan_bp.route('/')
def list_loans():

    page = request.args.get('page', 1, type=int)
    limit = 10
    offset = (page - 1) * limit

    loans_list = loan_service.get_loans(offset, limit)

    rows = []
    for loan in loans_list:
        rows.append({
            'id': loan.id,
            'can_return': False if loan.return_date else True,
            'data_values': [
                loan.id,loan.customer.code, loan.copy.code,
                loan.copy.title.title, loan.loan_date.replace(microsecond=0),
                loan.return_date.replace(microsecond=0) if loan.return_date else None,
            ]
        })

    has_next = len(loans_list) == limit

    return render_template(
        'list.html',
        title="Loans",
        entity_name='loans',
        headers=['ID', 'Customer', 'Copy', 'Title', 'Loan Date', 'Return Date'],
        rows=rows,
        page=page,
        has_next=has_next
    )


@loan_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        is_closed = loan_service.is_closed(id)
        if not is_closed:
            raise Exception('Loan is not closed')

        success = loan_service.remove_loan(id)
        if success:
            flash('Loan was deleted.', 'success')
        else:
            flash('Error while deleting.', 'error')
    except Exception as e:
        flash('Error deleting loan: ' + parse_db_exception(e), 'error')

    return redirect(url_for('loans.list_loans'))


@loan_bp.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        customer = request.form['customer']
        copy = request.form['copy_code']

        try:
            success = loan_service.create_loan(customer, copy)
            if success:
                flash('Loan created successfully.', 'success')
            else:
                flash('Error while creating loan.', 'error')
            return redirect(url_for('loans.list_loans'))

        except Exception as e:
            flash('Error creating loan: ' + parse_db_exception(e), 'error')
            loan = {'customer' : customer, 'copy_code': copy}
            return render_template('loan_form.html', title="Create Loan", loan=loan)

    # GET
    return render_template('loan_form.html', title="Create Loan", loan=None)


@loan_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    loan = loan_service.get_by_id(id)
    if not loan:
        flash('Loan was not found', 'error')
        return redirect(url_for('loans.list_loans'))

    if request.method == 'POST':

        customer_code = request.form['customer']
        copy_code = request.form['copy_code']

        try:
            customer = customer_service.get_by_code(customer_code)
            if not customer:
                raise Exception('Invalid customer code')

            copy = copy_service.get_by_code(copy_code)
            if not copy:
                raise Exception('Invalid copy code')

            success = loan_service.update_loan(loan.id, customer.id, copy.id, loan.loan_date, loan.return_date)
            if success:
                flash('Loan updated successfully.', 'success')
            else:
                flash('Error while updating.', 'error')
            return redirect(url_for('loans.list_loans'))

        except Exception as e:
            flash('Error updating loan: ' + parse_db_exception(e), 'error')

    data = {
        'id': loan.id,
        'customer': loan.customer.code,
        'copy_code': loan.copy.code
    }

    if request.args.get('action') == 'return':
        states = [CopyStatus.AVAILABLE.value, CopyStatus.LOST.value, CopyStatus.DISCARDED.value]
        print(states)
        return render_template('loan_form.html', title="Close Loan", loan=data, closing=True ,statuses=states)

    return render_template('loan_form.html', title="Edit Loan", loan=data)

@loan_bp.route('/close/<int:id>', methods=['POST'])
def close(id):
    loan = loan_service.get_by_id(id)
    if not loan:
        flash('Loan was not found', 'error')
        return redirect(url_for('loans.list_loans'))

    status_str = request.form['status']

    try:
        status = CopyStatus(status_str)
        success = loan_service.close_loan(loan.customer.code, loan.copy.code, status)
        if success:
            flash('Loan closed successfully.', 'success')
        else:
            flash('Error while closed.', 'error')

    except Exception as e:
        flash('Error updating loan: ' + parse_db_exception(e), 'error')

    return redirect(url_for('loans.list_loans'))