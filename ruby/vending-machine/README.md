# Vending Machine

## Overview
I wasn't presented with this code challenge. A friend of mine was recently telling me about a coding challenge he had completed as part of a job application. It sounded kinda fun and I need to sharpen my coding skills so I did some googling and found this:

- https://github.com/jamesjoshuahill/vending-machine

## Challenge
(From [link](https://github.com/jamesjoshuahill/vending-machine) above.)

Design a vending machine in code. The vending machine should perform as follows:

  - Once an item is selected and the appropriate amount of money is inserted, the vending machine should return the correct product.
  - It should also return change if too much money is provided, or ask for more money if insufficient funds have been inserted.
  - The machine should take an initial load of products and change. The change will be of denominations 1p, 2p, 5p, 10p, 20p, 50p, £1, £2.
  - There should be a way of reloading either products or change at a later point.
  - The machine should keep track of the products and change that it contains.

Please develop the machine in ruby.

Time allowed: 24 hours.

## Getting Started
One rule I've always emphasized with my teams is that the README should be explicit in helping new developers to the project get their developer up and running as quickly as possible.

### Prerequisites

- [Ruby 2.7.2](https://www.ruby-lang.org/en/downloads/)
- [Bundler](http://bundler.io/)
- [Git](http://git-scm.com/)

### Install

If you want to run this on your own, follow these steps:

- Install [rbenv](https://github.com/rbenv/rbenv) and the appropriate version of Ruby.

      rbenv install 2.7.2

- Clone the project using git:

      git clone https://github.com/klenwell/code-challenges.git

- Install gems:

      cd code-challenges/ruby/vending-machine
      bundle install

- Run specs:

      rspec

- Play with vending machine interactively:

      ruby main.rb

## Notes
- I started with some research (googling). That led me to the repo above. I also look up some designs like THIS. Mainly to figure out the interface and naming.

- In my last corporate job years ago, we had some vending machines in our breakroom. Every once in a while I would be around making a cup of coffee when the vendor came to service it. The snack machine there was a major inspiration for my design.

- I tried not to slavishly follow other solutions I found, but they were helpful. It was interesting to see where I ended up adopting some of the same concepts and where I did not.

- The main `VendingMachine` class interface is divided between consumer and vendor methods. No authentication is enforced.

- I wasn't particularly rushing to complete this. This is where I was at the 24-hour mark:

  - https://github.com/klenwell/code-challenges/tree/24-hour-mark/ruby/vending-machine

  No tests and I think I discovered a least a couple major bugs since then. I also ended up renaming a few things.

- This really became an exercise in RSpec for me. I don't have a lot of experience with RSpec but I really liked the way some developers on my team organized our tests using it at my last gig. I was trying to recreate that. Here are the best references I found:
  - https://relishapp.com/rspec/rspec-core/v/3-9/docs
  - https://relishapp.com/rspec/rspec-expectations/v/3-9/docs
  - https://www.betterspecs.org/

- Styling preference enforced with [RuboCop](https://github.com/rubocop-hq/rubocop).
