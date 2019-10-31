import blockchain from '../assets/blockchain';

const user = "Brian"

const userWallet = (name) => {
    let balance = 0;
    let transactions = [];
    const {chain} = blockchain;

    // Add all transactions to `transactions` array
    chain.forEach(function(element){
        transactions.push(...element.transactions)
    });

    // Show all transactions for a single user
    let userTransactions = transactions.filter( transaction => {
        return user === transaction.recipient || user === transaction.sender
    });

    // Sum of transactions received
    let received = transactions.reduce((acc, val) => {
        return val.recipient === user ? acc + val.amount : acc
    }, 0);

    // Sum of transactions sent
    let sent = transactions.reduce((acc, val) => {
        return val.sender === user ? acc + val.amount : acc 
    }, 0);

    // Get the balance of user transactions
    balance = received - sent;

    const userWallet = {userTransactions, balance};
    console.log(userWallet);

    return userWallet;

}

export default userWallet;