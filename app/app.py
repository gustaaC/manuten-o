from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    observation = db.Column(db.Text, nullable=True)

# Cria as tabelas no banco de dados, se elas não existirem
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    devices = Device.query.all()
    return render_template('index.html', devices=devices)

@app.route('/devices/new', methods=['GET', 'POST'])
def new_device():
    if request.method == 'POST':
        imei = request.form['imei']
        status = request.form['status']
        observation = request.form['observation']

        device = Device(imei=imei, status=status, observation=observation)
        db.session.add(device)
        db.session.commit()

        flash('Device added successfully.')
        return redirect(url_for('index'))

    return render_template('new_device.html')

@app.route('/device/<int:device_id>')
def device_detail(device_id):
    device = Device.query.get(device_id)
    if not device:
        flash('Device not found.')
        return redirect(url_for('index'))

    return render_template('device_detail.html', device=device)

@app.route('/update_status/<int:device_id>', methods=['POST'])
def update_status(device_id):
    device = Device.query.get(device_id)
    if not device:
        flash('Device not found.')
        return redirect(url_for('index'))

    new_status = request.form.get('status')
    if not new_status:
        flash('Invalid status.')
        return redirect(url_for('device_detail', device_id=device_id))

    device.status = new_status
    db.session.commit()

    flash('Device status updated successfully.')
    return redirect(url_for('device_detail', device_id=device_id))


if __name__ == '__main__':
    app.run(debug=True)