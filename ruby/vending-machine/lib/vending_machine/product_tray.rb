class ProductTray
  SoldOutError = Class.new(StandardError)
  TrayFullError = Class.new(StandardError)

  attr_accessor :price

  def initialize(code, price, size=8)
    @code = code
    @price = price
    @slots = []
    @size = size
  end

  def stock_product(products)
    products.each do |product|
      raise TrayFullError if @slots.length >= @size
      @slots << product
    end
  end

  def deliver_product
    raise SoldOutError if @slots.empty?
    @slots.shift
  end

  def products
    product_counts = Hash.new(0)
    @slots.each { |product| product_counts[product] += 1 }
    product_counts
  end
end
