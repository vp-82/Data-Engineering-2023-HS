pragma solidity ^0.4.21;

contract Coin {
     // The keyword "public" also allows other smart contracts to read the variable from outside.
    // This variable is of type "address" and represents the address of an Ethereum account.
    address public minter;
    mapping (address => uint) public balances;

     // Events allow Ethereum clients to respond to events on the contract.
    event Sent(address from, address to, uint amount);

    // Constructor is a special function declared using constructor keyword. 
    // It is an optional funtion and is used to initialize state variables of a contract. 
    // A constructor code is executed once when a contract is created and it is used to 
    // initialize the contract state.
    constructor() public {
        minter = msg.sender;
    }

    // With this function, the "minter" Ethereum account can send other accounts an arbitrary
    // amount of the "TestCoin".
    function mint(address receiver, uint amount) public {
        if (msg.sender != minter) return;
        balances[receiver] += amount;
    }

    // This function allows Ethereum accounts to transfer TestCoin to each other.
    function send(address receiver, uint amount) public {
        if (balances[msg.sender] < amount) return;
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        emit Sent(msg.sender, receiver, amount);
    }
}