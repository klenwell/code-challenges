require_relative 'vending_machine/product_tray'
require_relative 'vending_machine/coin_sorter'

class VendingMachine
  InvalidCodeError = Class.new(StandardError)
  PaymentRequiredError = Class.new(StandardError)

  attr_reader :product_trays, :coin_sorter, :display

  INIT_PRICES = [80, 120, 160].freeze
  NO_PRODUCT = nil
  NO_CHANGE = [].freeze

  def initialize
    @product_trays = init_product_trays
    @coin_sorter = CoinSorter.new
    @amount_deposited = 0
    @display = nil
  end

  #
  # Public Interface
  #
  # Consumer Methods
  def insert_coin(coin)
    @amount_deposited += @coin_sorter.deposit(coin)
  rescue CoinSorter::InvalidCoinError => e
    display_message("Invalid coin: #{e.message}.")
    @amount_deposited
  end

  # rubocop: disable Metrics/MethodLength, Metrics/AbcSize
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
    clear_display

    # Deliver product and change to user
    [product, change]

  rescue InvalidCodeError => e
    display_message("Invalid product code: #{e.message}")
    [NO_PRODUCT, NO_CHANGE]
  rescue PaymentRequiredError => e
    underpaid = -1 * e.message.to_i
    display_message("Please deposit #{underpaid}p")
    [NO_PRODUCT, NO_CHANGE]
  rescue ProductTray::SoldOutError => e
    display_message("Product sold out: #{e.message}")
    [NO_PRODUCT, NO_CHANGE]
  rescue CoinSorter::InsufficientChangeError => e
    display_message("Insufficient change: #{e.message}")
    cancel_transaction
  end
  # rubocop: enable Metrics/MethodLength, Metrics/AbcSize

  def cancel_transaction
    coins = @coin_sorter.make_change(@amount_deposited)
    @amount_deposited = 0
    [NO_PRODUCT, coins]
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

  def count_products
    product_counts = Hash.new(0)

    @product_trays.each_value do |tray|
      tray.products.each do |product, count|
        product_counts[product] += count
      end
    end

    product_counts
  end

  def status
    <<-HDC
      Products: #{count_products}
      Coins: #{@coin_sorter.sort}
      Amount: #{@coin_sorter.sum}
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
        price = INIT_PRICES.sample
        trays[code] = ProductTray.new(code, price)
      end
    end

    trays
  end

  def display_message(message)
    @display = message
  end

  def clear_display
    @display = nil
  end
end
