const snap = require('./config');

// Handle Create Transaction
const createTransaction = async (req, res) => {
    const { order_id, gross_amount } = req.body;

    if (!order_id || !gross_amount) {
        return res.status(400).json({ message: 'order_id and gross_amount are required!' });
    }

    try {
        const transactionParams = {
            transaction_details: {
                order_id,
                gross_amount,
            },
            payment_type: 'bank_transfer', // Set payment type to bank_transfer only
            enabled_payments: ['bank_transfer'], // Enable only bank transfer as a payment method
        };

        const transaction = await snap.createTransaction(transactionParams);
        res.status(201).json({
            token: transaction.token,
            redirect_url: transaction.redirect_url,
        });
    } catch (error) {
        res.status(500).json({ message: 'Error creating transaction', error: error.message });
    }
};

// Handle Get Transaction Status
const getTransactionStatus = async (req, res) => {
    const { order_id } = req.params;

    if (!order_id) {
        return res.status(400).json({ message: 'order_id is required!' });
    }

    try {
        const transactionStatus = await snap.transaction.status(order_id);
        res.status(200).json({
            status_code: transactionStatus.status_code,
            transaction_status: transactionStatus.transaction_status,
            /*fraud_status: transactionStatus.fraud_status,*/
        });
    } catch (error) {
        res.status(500).json({ message: 'Error fetching transaction status', error: error.message });
    }
};

module.exports = { createTransaction, getTransactionStatus };
