from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = '901-342-106'
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'c60bca4ca3342a'
app.config['MAIL_PASSWORD'] = '66aaff542f23af'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

appointments = [

    # Add more appointments as needed
]

@app.route('/')
def index():
    return render_template('index.html', appointments=appointments)

@app.route('/book', methods=['POST'])
def book():
    if request.method == 'POST':
        service = request.form['service']
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        email = request.form['email']

        appointment = {'id': len(appointments) + 1, 'name': name, 'email': email, 'date': date}
        appointments.append(appointment)

        # Send confirmation email
        send_email(email, 'Appointment Confirmation', f"HI , {name} , your appointment for {service} on {date} at {time} has been confirmed.")

        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('index'))

@app.route('/edit/<int:appointment_id>', methods=['GET', 'POST'])
def edit(appointment_id):
    appointment = next((app for app in appointments if app['id'] == appointment_id), None)
    if not appointment:
        flash('Appointment not found', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_date = request.form['new_date']
        appointment['date'] = new_date
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', appointment=appointment)

@app.route('/delete/<int:appointment_id>')
def delete(appointment_id):
    appointment = next((app for app in appointments if app['id'] == appointment_id), None)
    if appointment:
        appointments.remove(appointment)
        flash('Appointment deleted successfully!', 'success')
    else:
        flash('Appointment not found', 'danger')

    return redirect(url_for('index'))

def send_email(name, email, date):
    msg = Message('Appointment Confirmation', sender='your_email@example.com', recipients=[email])
    msg.body = f'Hi {name}, your appointment on {date} has been booked successfully.'
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
