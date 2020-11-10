require_relative 'vending_machine/product_tray'
require_relative 'vending_machine/coin_sorter'

class VendingMachine
  InvalidCodeError = Class.new(StandardError)
  PaymentRequiredError = Class.new(StandardError)

  attr_reader :product_trays, :coin_sorter

  def initialize
    @product_trays = init_product_trays
    @coin_sorter = CoinSorter.new
    @amount_deposited = 0
  end

  #
  # Public Interface
  #
  # Consumer Methods
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

    # Prepare change and product. Be careful here to rollback any failed actions. That's
    # why need to make change first.
    change = @coin_sorter.make_change(overpaid) if overpaid
    product = product_tray.deliver_product

    # Reset transaction state
    @amount_deposited = 0

    # Deliver product and change to user
    return product, change

  rescue InvalidCodeError => e
    display_message("Invalid code: #{e.message}. Please try again.")
    nil
  rescue PaymentRequiredError => e
    underpaid = -1 * e.message.to_i
    display_message("Please deposit #{underpaid}p.")
    nil
  rescue CoinSorter::InsufficientChangeError => e
    display_message("Insufficient change: #{e.message}")
    cancel_transaction
  end

  def cancel_transaction
    coins = @coin_sorter.make_change(@amount_deposited)
    @amount_deposited = 0
    return nil, coins
  end

  def display_message(message)
    p message
  end

  # Vendor Methods
  def stock_tray(code, products)
    tray = @product_trays[code]
    tray.stock_product(products)
  end

  def update_tray_price(code, new_price)
    tray = @product_trays[code]
    tray.price = new_price
  end

  def status
    <<-HDC
Products: #{product_counts}
Coins: #{@coin_sorter.inventory}
Amount: #{@coin_sorter.total}
HDC
  end

  private

  def init_product_trays
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

  def product_counts
    product_counts = Hash.new(0)

    @product_trays.values.each do |tray|
      tray.products.each do |product, count|
        product_counts[product] += count
      end
    end

    product_counts
  end
end
