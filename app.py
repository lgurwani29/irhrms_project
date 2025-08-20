from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'
db_path = os.path.join(os.path.dirname(__file__), 'irhrms.db')
# use relative path so running from folder works
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///irhrms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    designation = db.Column(db.String(80), nullable=False)

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    basic = db.Column(db.Integer, nullable=False)
    allowance = db.Column(db.Integer, nullable=False)
    net_pay = db.Column(db.Integer, nullable=False)
    employee = db.relationship('Employee', backref='payrolls')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pnr = db.Column(db.String(50), nullable=False, unique=True)
    passenger_name = db.Column(db.String(120), nullable=False)
    train_no = db.Column(db.String(40), nullable=False)
    status = db.Column(db.String(40), nullable=False)

@app.route('/')
def index():
    totals = {
        'total_emp': Employee.query.count(),
        'total_pay': Payroll.query.count(),
        'total_res': Reservation.query.count()
    }
    return render_template('index.html', **totals)

# Employee routes
@app.route('/employees')
def employees():
    rows = Employee.query.order_by(Employee.id.desc()).all()
    return render_template('employees.html', employees=rows)

@app.route('/employees/add', methods=['GET','POST'])
def add_employee():
    if request.method == 'POST':
        emp = Employee(name=request.form['name'], department=request.form['department'], designation=request.form['designation'])
        db.session.add(emp); db.session.commit()
        flash('Employee added.'); return redirect(url_for('employees'))
    return render_template('add_employee.html')

@app.route('/employees/<int:emp_id>/edit', methods=['GET','POST'])
def edit_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    if request.method == 'POST':
        emp.name = request.form['name']; emp.department = request.form['department']; emp.designation = request.form['designation']
        db.session.commit(); flash('Employee updated.'); return redirect(url_for('employees'))
    return render_template('edit_employee.html', emp=emp)

@app.route('/employees/<int:emp_id>/delete')
def delete_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    db.session.delete(emp); db.session.commit()
    flash('Employee deleted.')
    return redirect(url_for('employees'))

# Payroll routes
@app.route('/payroll')
def payroll():
    rows = Payroll.query.order_by(Payroll.id.desc()).all()
    return render_template('payroll.html', rows=rows)

@app.route('/payroll/add', methods=['GET','POST'])
def add_payroll():
    if request.method == 'POST':
        p = Payroll(employee_id=int(request.form['employee_id']), basic=int(request.form['basic']), allowance=int(request.form['allowance']), net_pay=int(request.form['basic'])+int(request.form['allowance']))
        db.session.add(p); db.session.commit(); flash('Payroll added.'); return redirect(url_for('payroll'))
    employees = Employee.query.all()
    return render_template('add_payroll.html', employees=employees)

@app.route('/payroll/<int:pid>/edit', methods=['GET','POST'])
def edit_payroll(pid):
    row = Payroll.query.get_or_404(pid)
    if request.method == 'POST':
        row.employee_id = int(request.form['employee_id']); row.basic = int(request.form['basic']); row.allowance = int(request.form['allowance']); row.net_pay = row.basic + row.allowance
        db.session.commit(); flash('Payroll updated.'); return redirect(url_for('payroll'))
    employees = Employee.query.all()
    return render_template('edit_payroll.html', row=row, employees=employees)

@app.route('/payroll/<int:pid>/delete')
def delete_payroll(pid):
    row = Payroll.query.get_or_404(pid); db.session.delete(row); db.session.commit(); flash('Payroll deleted.'); return redirect(url_for('payroll'))

# Reservations routes
@app.route('/reservations')
def reservations():
    rows = Reservation.query.order_by(Reservation.id.desc()).all()
    return render_template('reservations.html', rows=rows)

@app.route('/reservations/add', methods=['GET','POST'])
def add_reservation():
    if request.method == 'POST':
        r = Reservation(pnr=request.form['pnr'], passenger_name=request.form['passenger_name'], train_no=request.form['train_no'], status=request.form['status'])
        db.session.add(r); db.session.commit(); flash('Reservation added.'); return redirect(url_for('reservations'))
    return render_template('add_reservation.html')

@app.route('/reservations/<int:rid>/edit', methods=['GET','POST'])
def edit_reservation(rid):
    row = Reservation.query.get_or_404(rid)
    if request.method == 'POST':
        row.pnr = request.form['pnr']; row.passenger_name = request.form['passenger_name']; row.train_no = request.form['train_no']; row.status = request.form['status']
        db.session.commit(); flash('Reservation updated.'); return redirect(url_for('reservations'))
    return render_template('edit_reservation.html', row=row)

@app.route('/reservations/<int:rid>/delete')
def delete_reservation(rid):
    row = Reservation.query.get_or_404(rid); db.session.delete(row); db.session.commit(); flash('Reservation deleted.'); return redirect(url_for('reservations'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)