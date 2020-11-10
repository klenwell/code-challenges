require 'pry'
require_relative 'lib/vending_machine'

vm = VendingMachine.new

# Stock Machine
cheetohs = ['cheetohs'] * 8
doritos = ['doritos'] * 3
vm.stock_tray('A1', cheetohs)
vm.stock_tray('D4', doritos)

# Insufficient Change
vm.update_tray_price('A1', 50)
vm.insert_coin(100)
product, change = vm.select_product('A1')
binding.pry

# Order
[100, 20].each{|coin| vm.insert_coin(coin)}
product, change = vm.select_product('A1')
p "VM dispensed: #{product}; Your change: #{change}"
