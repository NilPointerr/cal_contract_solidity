// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract practice {
    address payable public owner;
    uint public amount;
    uint public num;
    struct Emp {
        string name;
        uint mobile;
        string add;
    }
    string public operator;
    Emp public emp;

    uint public total;

    struct Auth {
        string _add;
        bool Isright;
    }

    uint public ans;
    Auth public auth;
    mapping(uint => Emp) public myemp;
    event addEmp(string name, uint mobile, string add);

    constructor() payable {
        owner = payable(msg.sender);
        amount = msg.value;
    }

    function myfunc(
        string memory _name,
        uint _mobile,
        string memory _add
    ) public {
        emp = Emp(_name, _mobile, _add);
        myemp[_mobile] = emp;
        emit addEmp(_name, _mobile, _add);
        num += 1;
    }

    function revesion(string memory _add, bool _isrigth) public {
        if (msg.sender == owner) {
            _isrigth = true;
        }
        auth = Auth(_add, _isrigth);
    }

    function calculate(
        uint _num1,
        uint _num2,
        string memory _operator
    ) public returns (uint) {
        operator = _operator;
        if (keccak256(bytes(operator)) == keccak256(bytes("+"))) {
            total = _num1 + _num2;
        } else if (keccak256(bytes(operator)) == keccak256(bytes("-"))) {
            total = _num1 - _num2;
        } else if (keccak256(bytes(operator)) == keccak256(bytes("*"))) {
            total = _num1 * _num2;
        } else if (keccak256(bytes(operator)) == keccak256(bytes("/"))) {
            total = _num1 / _num2;
        } else {
            operator = "INVALID OPERATOR";
        }
        ans = total;
        return total;
    }

    function viewAns() public view returns (uint) {
        return ans;
    }
}
