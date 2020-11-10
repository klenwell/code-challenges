require 'pry'
require_relative 'lib/vending_machine'

vm = VendingMachine.new

# Stock Machine
cheetohs = ['cheetohs'] * 8
doritos = ['doritos'] * 3
vm.stock_tray('A1', cheetohs)
vm.stock_tray('D4', doritos)

# Order
[100, 20].each{|coin| vm.insert_coin(coin)}
product, change = vm.select_product('A1')
p "VM dispensed: #{product}; Your change: #{change}"

binding.pry
