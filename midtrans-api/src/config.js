const midtransClient = require('midtrans-client');
require('dotenv').config(); // This loads the .env file


// Setup Snap API instance
const snap = new midtransClient.Snap({
    isProduction: false, // Sandbox mode
    serverKey: process.env.MIDTRANS_SERVER_KEY,
    clientKey: process.env.MIDTRANS_CLIENT_KEY,
});

module.exports = snap;
