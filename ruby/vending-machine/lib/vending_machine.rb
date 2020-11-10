require_relative 'vending_machine/product_tray'
require_relative 'vending_machine/coin_sorter'

class VendingMachine
  InvalidCodeError = Class.new(StandardError)
  PaymentRequiredError = Class.new(StandardError)

  attr_reader :product_trays, :coin_sorter

  def initialize
    @product_trays = initialize_product_trays
    @coin_sorter = CoinSorter.new
    @amount_deposited = 0
  end

  #
  # Public Interface
  #
  def insert_coin(coin)
    @amount_deposited += @coin_sorter.deposit(coin)
  rescue CoinSorter::InvalidCoinError => e
    display_message("Invalid coin: #{e.message}. Please try again.")
    nil
  end

  def select_product(code)
    product_tray = @product_trays[code]

    # Validate selection
    raise InvalidCodeError.new(code) if product_tray.nil?

    # Validate payment
    overpaid = @amount_deposited - product_tray.price
    raise PaymentRequiredError.new(overpaid) if overpaid < 0
    change = @coin_sorter.make_change(overpaid) if overpaid

    # Fetch product
    product = product_tray.deliver_product

    # Reset transaction state
    @amount_deposited = 0

    # Deliver product and change to user
    return product, change

  rescue InvalidCodeError => e
    display_message("Invalid code: #{e.message}. Please try again.")
    cancel_transaction
  rescue PaymentRequiredError => e
    amount = -1 * e.message.to_i
    display_message("Please deposit #{amount}p.")
    cancel_transaction
  rescue CoinSorter::InsufficientChangeError => e
    display_message("Insufficient change: #{e.message}")
    cancel_transaction
  end

  def cancel_transaction
    coins = @coin_sorter.make_change(@amount_deposited)
    @amount_deposited = 0
    return nil, coins
  end

  def stock_tray(code, products)
    tray = @product_trays[code]
    tray.stock_product(products)
  end

  def update_tray_price(code, new_price)
    tray = @product_trays[code]
    tray.price = new_price
  end

  def display_message(message)
    p message
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
