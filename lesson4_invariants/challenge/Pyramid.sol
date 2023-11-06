pragma solidity ^0.8.0;

/**
 * @title Pyramid - a pyramid scheme
 * @author Certora
 * @notice address(0) cannot be a member
 * 
 * Data structures
 * ---------------
 * The pyramid must be a binary tree, with a unique root.
 *
 * Each member has:
 * - balance
 * - a parent
 * - Up to two children
 *
 * Methods
 * -------
 * - Withdraw: whenever a participant withdraws amount:
 *   * A fraction of the withdrawn amount goes to the parent
 *     (or a constant amount?)
 *   * Maybe once a certain amount X was passed to the parent, no more needs to be paid?
 *   TODO: guarantee that `withdraw` will not be mutated!
 * - Join:
 *   * there is a fixed joining price
 *   * this is paid not by the joining participant, but by the parent which admits them
 *   * only two children per participant are allowed
 *
 */
contract Pyramid {

  /**
   * @notice Member data
   * @param exists - true only if member joined
   */
  struct Member {
    uint256 balance;
    bool exists;
    address parent;
    address leftChild;
    address rightChild;
  }

  mapping(address => Member) private members;  // All pyramid members
  address private _root; // Root of the binary tree

  uint256 public immutable parentFrac;
  uint256 public immutable joiningFee;

  constructor(
    uint256 _parentFrac,
    uint256 _joiningFee
  ) {
    require(_parentFrac > 0, "Must be non-zero");
    parentFrac = _parentFrac;
    joiningFee = _joiningFee;
    
    // Set the root
    require(msg.sender != address(0), "Address zero cannot be a member");
    _root = msg.sender;
    Member storage memberData = members[msg.sender];
    memberData.exists = true;
  }

  modifier memebersOnly() {
    require(contains(msg.sender), "Not a member");
    _;
  }

  /**
   * @return whether the given address is a member
   */
  function contains(address member) public view returns (bool) {
    return members[member].exists;
  }

  /**
   * @return the unique root of the binary tree
   */
  function root() public view returns (address) {
    return _root;
  }

  /**
   * @return the member's balance in the pyramid scheme
   */
  function balanceOf(address member) memebersOnly() public view returns (uint256) {
    Member storage memberData = members[member];
    return memberData.balance;
  }

  /**
   * @notice method for depositing into the pyramid scheme by the sender
   */
  function deposit() memebersOnly() external payable {
    Member storage memberData = members[msg.sender];
    memberData.balance += msg.value;
  }

  /**
   * @param isRight use true for referring to the right child, use false for the left
   * @return if the relevant child of the parent address exists
   */
  function hasChild(
    address parent,
    bool isRight
  ) memebersOnly() public view returns (bool) {
    require(contains(parent), "Not a member");
    Member storage memberData = members[parent];
    if (isRight) {
      return memberData.rightChild != address(0);
    } else {
      return memberData.leftChild != address(0);
    }
  }

  /**
   * @notice method for withdrawing from the pyramid scheme for the sender
   * @dev for every amount x withdrawn, an amount x/y of the sender's balance will be
   * given to the sender's parent, where y is `parentFrac` (the root is excluded from
   * this)
   */
  function withdraw(uint256 amount) memebersOnly() public {
    Member storage memberData = members[msg.sender];

    // If there is no parent than the parent part is zero
    uint256 parentPart = contains(memberData.parent) ? amount / parentFrac : 0;
    uint256 totalRemove = amount + parentPart;
    require(memberData.balance >= totalRemove, "Insufficient funds");

    memberData.balance -= totalRemove;
    
    // Send parent part
    members[memberData.parent].balance += parentPart;
    
    // Send member's payment
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
  }

  /**
   * @notice method for the sender to join a new member as a child
   * @param child the address of the member to join
   * @param isRight use true to add the member as the right child, use false to add them
   * as the left child
   * @dev a joining fee amount will be deducted from the sender's balance in the pyramid
   * scheme
   */
  function join(address child, bool isRight) memebersOnly() public {
    require(!hasChild(msg.sender, isRight), "Child already exists");
    require(!contains(child), "Child already a member");
    require(child != address(0), "Address zero cannot be a member");

    Member storage memberData = members[msg.sender];
    require(memberData.balance >= joiningFee, "Insufficient funds");

    memberData.balance -= joiningFee;
    if (isRight) {
      memberData.rightChild = child;
    } else {
      memberData.leftChild = child;
    }
  }

}
