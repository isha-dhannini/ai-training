const express = require('express');

const app = express();

const PORT = 8080;

app.get('/', (req, res) => {
    res.send(`
        <h1>Hello! Hi from AKS!</h1>
        <p>Pod Name: ${process.env.HOSTNAME}</p>
    `);
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});