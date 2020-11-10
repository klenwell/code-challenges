require_relative 'vending_machine/product_tray'

class VendingMachine
  VALID_COINS = [1, 2, 5, 10, 20, 50, 100, 200]

  InvalidCoinError = Class.new(StandardError)
  InvalidCodeError = Class.new(StandardError)
  PaymentRequiredError = Class.new(StandardError)

  attr_reader :product_trays

  def initialize
    @product_trays = initialize_product_trays
    @amount_deposited = 0
  end

  #
  # Public Interface
  #
  def insert_coin(coin)
    raise InvalidCoinError(coin) unless VALID_COINS.include? coin
    @amount_deposited += coin

  rescue InvalidCoinError => e
    display_message("Invalid coin: #{e.message}. Please try again.")
    nil
  end

  def select_product(code)
    product_tray = @product_trays[code]

    # Validate selection
    raise InvalidCodeError.new(code) if product_tray.nil?

    # Validate Payment
    change = @amount_deposited - product_tray.price
    raise PaymentRequiredError.new(change) if change < 0

    # Fetch product
    product = product_tray.deliver_product

    # Reset transaction state
    @amount_deposited = 0

    # Deliver product and change to user
    return product, change

  rescue InvalidCodeError => e
    display_message("Invalid code: #{e.message}. Please try again.")
    nil
  rescue PaymentRequiredError => e
    amount = -1 * e.message.to_i
    display_message("Please deposit #{amount}p.")
    nil
  end

  def display_message(message)
    p message
  end

  def refund_change; end

  def stock_tray(code, products)
    tray = @product_trays[code]
    tray.stock_product(products)
  end

  def report_status; end

  private

  def initialize_product_trays
    trays = {}
    rows = "ABCD".split('')
    cols = "1234".split('')

    rows.each do |row|
      cols.each do |col|
        code = "#{row}#{col}"
        price = [80, 120, 160].shuffle.first
        trays[code] = ProductTray.new(code, price)
      end
    end

    trays
  end
end
