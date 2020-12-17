# Grape API Challenge

## Overview
This is a code challenge of my own device. I challenged myself to set up a simple API using the Grape framework after I interviewed with a couple different companies using it.

## Challenge
### Ping
The first part of the challenge is to set up the Grape framework on rack with a single ping endpoint at `/api/v1/ping`. Using curl, it should behave as follows:

```
$ curl http://localhost:9292/api/v1/ping
{"ping":"pong"}
```

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

      cd code-challenges/ruby/grape
      bundle install

- Run the server:

      bundle exec rackup

- Test form the command line:

      curl http://localhost:9292/api/v1/ping
