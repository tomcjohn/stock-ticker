# Online Bank

This is a submission for the CashApp coding exercise - February 2021.

## Language

This submission is written in the Java Programming Language using:

- OpenJDK v11.0.2
- Gradle v6.8


## Running tests

In order to compile the code and run the tests included, please execute the following command:

``` sh
./gradlew clean test
```

## Overview

I've chosen to model my implementation based on an event store.

Based on my high-level understanding of this domain I believe this is normally how financial transactions are tracked.
It allows the balance for an account to be calculated at any point in time by reapplying all transactions leading
up to that point.

This system architecture should be much simpler and less error prone than the alternative of a system that maintains
a real-time account balance constantly updated as transactions are received, which would be much harder to ensure was
correct under high load and in a concurrent processing scenario.


## Assumptions

During implementation I made the following assumptions for the purposes of simplification:

* All transactions are in AUD, and therefore no currency conversion is required
* No parameters will be `null`, meaning no noisy, boilerplate null checking


## Design and architecture

The central domain object in this system is the `Transaction`.  The specifics of the coding exercise only mentions
people and their balances but I chose to also create an `Account` domain object as that seems logical in the context
of an online banking system.

A `Transaction` references the `Account` to which it relates by the id of the `Account`.
An `Account` has a set of authorised account holders who are the `Person`s that are permitted to make withdrawals.

In implementing a banking system as an event store each `Transaction` is an event that affects the state (ie. balance)
of the `Account` to which it refers.

There are two types of `Transaction` that can be applied to an account, a `deposit` and a `withdrawal`.
I made the `Transaction` class final and its constructor private, and added two builder methods to ensure no other
implementations of `Transaction` other than these could be created.

`Deposit` transactions are created with a positive amount value whereas the amount for `withdrawal` transactions
is negated on construction.  In this way account balances can be calculated by simply summing the amounts of all
transactions for a given account without having to check the type of each transaction.

All timestamp values are stored in `UTC` in order to ensure consistency and auditability.


## Error handling

There are two error checking cases in `TransactionStore`, both of which apply to `withdrawal` transactions only:
1) the individual performing the transaction (the `transactor`) exists in the list of authorised `Person`s on the account
2) there is sufficient balance such that when a transaction is applied the account's balance will not become negative

No error checking is performed on `Deposit` transactions - anyone who wants to put any amount of money into the bank
is welcome to!


## Flaws

1) This implementation has a race condition which would easily be exposed under load if there were more than one
   instance of the `TransactionStore` in operation.
   In the negative balance check it first fetches the current balance of the account before applying the transaction.
   Two withdrawals received and processed at the same time for amounts that are both less than the current balance
   but which together add up to more would cause the `Account` to be overdrawn as they would both pass the negative
   balance check before both then being applied to the account.

2) Too many implementations of #equals() and #hashCode()!
   I would like to have spent time figuring out more reliable methods of ensuring duplicate transactions are avoided
   and account holders could be checked for without relying on #equals() implementations in `Transaction` and `Person`.


## Improvements

The following are some of the possible ways in which this solution could be extended, given more time.

### Feature improvements:

* Allow transfers between accounts to be performed as a single atomic action.
* Implement support for transactions in other currencies backed by a regularly refreshed rate table
  (sourced from one or more central banks presumably?).
* Add the ability to open and close an `Account` to the `AccountStore` service.
* Add a check to ensure the `Account` referenced by a `Transaction` is an account that exists
  and has not been closed (ie. only accept a `Transaction` for a valid `Account`).

### Implementation improvements:

* Null checking on all method parameters - especially those on the builder functions in `Transaction`.
* Consider ways to avoid the race condition described in **Flaws** above where two withdrawals could cause an account
  to be overdrawn.
* Add a library that adds support for the `Either` datatype to simplify error handling and remove the need to throw
  exceptions from the check methods in `TransactionStore`.
* Something other than in-memory persistence of transactions - seems dicey!
* Add logging and audit logging.
