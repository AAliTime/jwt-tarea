from auth import create_token, get_current_user, hash_password, verify_password
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="API con JWT")

fake_users = {
    "maria@ujap.edu.ve": {
        "hashed": hash_password("profesor123"),
        "role": "profesor",
    },
    "estudiante@ujap.edu.ve": {
        "hashed": hash_password("estudiante123"),
        "role": "estudiante",
    },
}


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(form.username)
    if not user or not verify_password(form.password, user["hashed"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas"
        )

    token = create_token({"sub": form.username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/publico") 
def ruta_publica():
    return {"msg": "Cualquiera puede ver esto"}


@app.get("/privado") 
def ruta_privada(user=Depends(get_current_user)):
    return {"msg": f"Hola {user['sub']}, rol: {user['role']}"}


@app.get("/admin")  
def ruta_admin(user=Depends(get_current_user)):
    if user["role"] != "profesor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Solo para profesores"
        )
    return {"msg": "Panel de administración"}