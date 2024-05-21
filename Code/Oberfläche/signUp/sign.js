async function signup() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {
        alert("Die Passwörter stimmen nicht überein.");
        return;
    }

    const userData = {
        email: email,
        password: password
    };

    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (!response.ok) {
            throw new Error('Signup request failed.');
        }

        alert('Registrierung erfolgreich!');
        window.location.href = '/login.html'; // Weiterleitung zur Login-Seite nach erfolgreicher Registrierung
    } catch (error) {
        console.error('Error:', error);
        alert('Registrierung fehlgeschlagen. Bitte versuche es erneut.');
    }
}


const express = require('express');
const bodyParser = require('body-parser');
const mongodb = require('mongodb');
const MongoClient = mongodb.MongoClient;
const dotenv = require('dotenv');

dotenv.config();
const app = express();
const port = 3000;

// Middleware für JSON-Request-Body
app.use(bodyParser.json());

// Verbindungsinformationen für die MongoDB
const url = `mongodb://${process.env.DB_HOST}:${process.env.DB_PORT}`;
const dbName = process.env.DB_NAME;
const username = process.env.DB_USER;
const password = process.env.DB_PASSWORD;
const collectionName = 'Login';

// Endpunkt für die Sign-Up-Anfrage
app.post('/signup', async (req, res) => {
    const userData = req.body;

    // Verbindung zur MongoDB herstellen
    const client = new MongoClient(url, { useUnifiedTopology: true });

    try {
        await client.connect({ auth: { username, password } });

        // Datenbank und Sammlung auswählen
        const db = client.db(dbName);
        const collection = db.collection(collectionName);

        // Neuen Benutzer in die Datenbank einfügen
        const result = await collection.insertOne(userData);

        res.sendStatus(200);
    } catch (error) {
        console.error('Error:', error);
        res.sendStatus(500);
    } finally {
        // Verbindung schließen
        await client.close();
    }
});

// Server starten
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
