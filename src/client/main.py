from app.database.models import Usuario
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.core.auth import get_password_hash
from getpass import getpass

def main(db: Session):
    # Validar que nombre y correo no estén vacíos
    while True:
        nombre = input("Ingresa el nombre de usuario: ").strip()
        correo = input("Ingresa el correo del usuario: ").strip()
        if nombre and correo:
            break
        print("❗ El nombre y el correo no pueden estar vacíos. Inténtalo de nuevo.\n")

    # Validar que las contraseñas coincidan
    while True:
        contraseña = getpass("Ingresa la contraseña del usuario: ")
        confirm_contraseña = getpass("Confirma la contraseña: ")

        if contraseña != confirm_contraseña:
            print("❗ Las contraseñas no coinciden. Inténtalo de nuevo.\n")
        elif contraseña.strip() == "":
            print("❗ La contraseña no puede estar vacía.\n")
        else:
            break

    # Otros datos (no obligatorios en este ejemplo, puedes agregar validaciones si quieres)
    number = input("Ingresa el número del usuario: ").strip()
    rol_usuario = input("Ingresa el rol del usuario (admin, super_user o produccion): ").strip()

    # Validar si ya existe el usuario
    user_exists = db.query(Usuario).filter(Usuario.username == nombre).first()
    if user_exists:
        return "❌ El usuario ya existe."

    email_exists = db.query(Usuario).filter(Usuario.email == correo).first()
    if email_exists:
        return "❌ El correo ya está en uso."

    # Crear usuario
    nuevo_usuario = Usuario(
        username=nombre,
        password=get_password_hash(contraseña),
        telefono=number,
        email=correo,
        rol=rol_usuario
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return f"✅ Usuario '{nombre}' fue creado correctamente."

if __name__ == "__main__":
    db = SessionLocal()
    try:
        response = main(db)
        print(response)
    finally:
        db.close()
