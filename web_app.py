from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_cors import CORS
import database
import os
import io
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import csv
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)
app.secret_key = 'edutrack_secret_key_2024'

# Ensure database tables exist
database.create_tables()

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        role = database.check_login(username, password)
        if role:
            session['user'] = username
            session['role'] = role[0]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    students = database.get_all_students()

    # Calculate statistics
    total_students = len(students)
    avg_percentage = 0
    top_performers = 0

    if students:
        percentages = [student[6] for student in students if student[6] > 0]
        avg_percentage = sum(percentages) / len(percentages) if percentages else 0
        top_performers = len([student for student in students if student[6] >= 90])

    return render_template('dashboard.html',
                         students=students,
                         role=session.get('role'),
                         total_students=total_students,
                         avg_percentage=round(avg_percentage, 1),
                         top_performers=top_performers)

@app.route('/add_student', methods=['POST'])
def add_student():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    try:
        data = {
            'roll': int(request.form['roll']),
            'name': request.form['name'],
            'sub1': int(request.form['sub1']),
            'sub2': int(request.form['sub2']),
            'sub3': int(request.form['sub3'])
        }

        database.insert_student(data)
        flash('Student added successfully!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Error adding student: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/update_student/<int:roll>', methods=['POST'])
def update_student(roll):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    try:
        data = {
            'roll': roll,
            'name': request.form['name'],
            'sub1': int(request.form['sub1']),
            'sub2': int(request.form['sub2']),
            'sub3': int(request.form['sub3'])
        }

        database.update_student(data)
        flash('Student updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Error updating student: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/delete_student/<int:roll>')
def delete_student(roll):
    if 'user' not in session:
        return redirect(url_for('login'))

    database.delete_student(roll)
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/api/students')
def api_students():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    students = database.get_all_students()
    return jsonify([dict(student) for student in students])

@app.route('/reports')
def reports():
    if 'user' not in session:
        return redirect(url_for('login'))

    students = database.get_all_students()

    # Calculate statistics for reports
    total_students = len(students)
    avg_percentage = 0
    high_achievers = 0
    need_improvement = 0

    if students:
        percentages = [student[6] for student in students if student[6] > 0]
        avg_percentage = sum(percentages) / len(percentages) if percentages else 0
        high_achievers = len([s for s in students if s[6] >= 90])
        need_improvement = len([s for s in students if s[6] < 50])

    # Grade distribution
    grade_counts = {
        'A+': len([s for s in students if s[7] == 'A+']),
        'A': len([s for s in students if s[7] == 'A']),
        'B+': len([s for s in students if s[7] == 'B+']),
        'B': len([s for s in students if s[7] == 'B']),
        'C': len([s for s in students if s[7] == 'C']),
        'F': len([s for s in students if s[7] == 'F'])
    }

    # Performance data for charts
    student_names = [student[1] for student in students]
    student_percentages = [student[6] for student in students]

    return render_template('reports.html',
                         students=students,
                         total_students=total_students,
                         avg_percentage=round(avg_percentage, 1),
                         high_achievers=high_achievers,
                         need_improvement=need_improvement,
                         grade_counts=grade_counts,
                         student_names=student_names,
                         student_percentages=student_percentages)

@app.route('/export/pdf')
def export_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))

    students = database.get_all_students()
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Title
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=1
    )
    elements.append(Paragraph('EduTrack - Student Report', title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Metadata
    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=20
    )
    elements.append(Paragraph(f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', meta_style))
    elements.append(Paragraph(f'Total Students: {len(students)}', meta_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Table data
    table_data = [['Roll', 'Name', 'Sub1', 'Sub2', 'Sub3', 'Total', 'Percentage', 'Grade']]
    for student in students:
        table_data.append([
            str(student[0]),
            str(student[1]),
            str(student[2]),
            str(student[3]),
            str(student[4]),
            str(student[5]),
            f"{student[6]:.2f}%",
            str(student[7])
        ])
    
    # Create table
    table = Table(table_data, colWidths=[0.7*inch, 1.2*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.8*inch, 0.6*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'EduTrack_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@app.route('/export/excel')
def export_excel():
    if 'user' not in session:
        return redirect(url_for('login'))

    students = database.get_all_students()
    
    # Create CSV
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    
    # Header
    writer.writerow(['EduTrack - Student Report'])
    writer.writerow(['Generated on:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    writer.writerow(['Total Students:', len(students)])
    writer.writerow([])  # Empty row
    
    # Column headers
    writer.writerow(['Roll', 'Name', 'Subject 1', 'Subject 2', 'Subject 3', 'Total', 'Percentage', 'Grade'])
    
    # Data rows
    for student in students:
        writer.writerow([
            student[0],
            student[1],
            student[2],
            student[3],
            student[4],
            student[5],
            f"{student[6]:.2f}%",
            student[7]
        ])
    
    # Convert to bytes
    buffer.seek(0)
    excel_data = buffer.getvalue().encode('utf-8')
    buffer_bytes = io.BytesIO(excel_data)
    
    return send_file(
        buffer_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'EduTrack_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)