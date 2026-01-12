# 1. On part d'une image de base Python légère (version 3.10)
FROM python:3.10-slim

# 2. On définit le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 3. On copie le fichier de dépendances pour les installer
COPY requirements.txt .

# 4. On installe les dépendances (sans cache pour gagner de la place)
RUN pip install --no-cache-dir -r requirements.txt

# 5. On copie tout le reste du code dans le conteneur
COPY . .

# 6. On dit que le conteneur va écouter sur le port 8000
EXPOSE 8000

# 7. La commande pour démarrer l'app quand le conteneur se lance
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]