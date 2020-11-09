require_relative 'vending_machine/product_tray'

class VendingMachine
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
  def deposit_payment(amount)
    @amount_deposited += amount
  end

  def select_product(code)
    product_tray = @product_trays[code]

    # Validate selection
    raise InvalidCodeError.new(code) if product_tray.nil?

    # Validate Payment
    p product_tray
    change = @amount_deposited - product_tray.price
    raise PaymentRequiredError.new(change) if change < 0

    # Response to user
    if change
      message = "Your change is #{change}p. Enjoy your treat!"
    else
      message = "Thank you. Enjoy your treat!"
    end

    display_message(message)

    # TODO: return change, too
    product_tray.deliver_product

  rescue InvalidCodeError => e
    display_message("Invalid code: #{e.message}. Please try again.")
    nil
  rescue PaymentRequiredError => e
    amount = -1 * e.message.to_i
    display_message("Please depost #{amount}p.")
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
