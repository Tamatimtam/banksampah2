from app import create_app, db
from app.models import User

app = create_app()

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin user
        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin = User(username="admin")
            admin.set_password("admin")
            db.session.add(admin)
            db.session.commit()
    
    print("Initialized the database and created default admin user.")

if __name__ == '__main__':
    app.run(debug=True)