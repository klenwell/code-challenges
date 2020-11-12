# Required to avoid rspec error:
# NameError: uninitialized constant ProductTray::Forwardable
require "forwardable"

class ProductTray
  extend Forwardable

  SoldOutError = Class.new(StandardError)
  TrayFullError = Class.new(StandardError)

  attr_accessor :price

  def_delegators :@slots, :empty?

  def initialize(code, price, size=8)
    @code = code
    @price = price
    @slots = []
    @size = size
  end

  def stock_product(products)
    products.each do |product|
      raise TrayFullError.new(@code) if @slots.length >= @size

      @slots << product
    end
    @slots
  end

  def deliver_product
    raise SoldOutError.new(@code) if empty?

    @slots.shift
  end

  def products
    product_counts = Hash.new(0)
    @slots.each { |product| product_counts[product] += 1 }
    product_counts
  end

  def empty
    # Clear slots. Return any products.
    products = @slots
    @slots = []
    products
  end
end
