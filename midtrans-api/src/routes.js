const express = require('express');
const { createTransaction, getTransactionStatus } = require('./handler');

const router = express.Router();

// Route for creating a transaction
router.post('/transaction', createTransaction);

// Route for fetching transaction status
router.get('/transaction/:order_id/status', getTransactionStatus);

module.exports = router;
