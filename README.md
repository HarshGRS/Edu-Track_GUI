# EduTrack - Student Score Management System

A modern, animated web application for managing student scores with both desktop and web interfaces.

## Features

- 🔐 Secure login system with role-based access
- 📊 Interactive dashboard with statistics
- 👥 Student management (Add, Edit, Delete, View)
- 📈 Comprehensive reports with charts
- 🎨 Modern animated UI with smooth transitions
- 📱 Responsive design for all devices
- 🚀 Deployable web application

## Demo Credentials

- **Admin**: username: `admin`, password: `admin123`
- **Teacher**: username: `teacher`, password: `teach123`

## Installation & Setup

### Prerequisites
- Python 3.14+
- pip package manager

### Local Development

1. **Clone or download the project**
   ```bash
   cd EduTrack_GUI
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the web application**
   ```bash
   python web_app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

### Desktop Application

To run the desktop GUI version:
```bash
python main.py
```

## Deployment

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Open app**
   ```bash
   heroku open
   ```

### Other Deployment Options

- **Railway**: Connect GitHub repo
- **Render**: Connect GitHub repo
- **Vercel**: For static frontend (requires modifications)
- **AWS/GCP/Azure**: Use their app engine services

## Project Structure

```
EduTrack_GUI/
├── main.py                 # Desktop GUI application
├── web_app.py             # Web Flask application
├── database.py            # Database operations
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── runtime.txt           # Python version for deployment
├── edutrack.db           # SQLite database (auto-generated)
├── templates/            # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   └── reports.html
├── static/               # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── animations.js
│       ├── dashboard.js
│       └── reports.js
└── assets/               # Additional assets
```

## Technologies Used

### Backend
- **Flask**: Web framework
- **SQLite**: Database
- **Werkzeug**: Security utilities

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with animations
- **JavaScript**: Interactivity
- **Chart.js**: Data visualization
- **Font Awesome**: Icons

### Desktop
- **CustomTkinter**: Modern GUI framework
- **Pillow**: Image processing
- **ReportLab**: PDF generation
- **Matplotlib**: Charts

## Features Overview

### Web Interface
- **Login Page**: Animated login with floating elements
- **Dashboard**: Statistics cards, student table, add/edit modals
- **Reports**: Interactive charts, performance analytics, export options

### Desktop Interface
- **Modern GUI**: CustomTkinter with dark theme
- **Student Management**: Full CRUD operations
- **Reports**: PDF generation, charts
- **Animated UI**: Smooth transitions and effects

## API Endpoints

- `GET /` - Home page (redirects to login)
- `GET/POST /login` - User authentication
- `GET /logout` - User logout
- `GET /dashboard` - Main dashboard
- `POST /add_student` - Add new student
- `POST /update_student/<roll>` - Update student
- `GET /delete_student/<roll>` - Delete student
- `GET /api/students` - Get all students (JSON)
- `GET /reports` - Reports and analytics

## Security Features

- Session-based authentication
- CSRF protection
- Input validation
- SQL injection prevention
- Secure password handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

---

**Made with ❤️ for educational institutions**