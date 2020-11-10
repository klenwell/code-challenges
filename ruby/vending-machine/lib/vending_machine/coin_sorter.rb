class CoinSorter
  VALID_COINS = [1, 2, 5, 10, 20, 50, 100, 200]

  InvalidCoinError = Class.new(StandardError)
  InsufficientChangeError = Class.new(StandardError)

  attr_accessor :price

  def initialize(coins=nil)
    @sorter = init_sorter
    coins.each{|coin| deposit(coin)} if coins
  end

  def deposit(coin)
    raise InvalidCoinError.new(coin) unless VALID_COINS.include? coin
    @sorter[coin] += 1
    coin
  end

  def make_change(amount)
    coins = []

    # Go backwards through the sort to make change
    VALID_COINS.sort.reverse.each do |value|
        count = amount / value
        released_coins = release_coins(value, count)
        coins.concat(released_coins)
        amount = amount - released_coins.sum
        return coins if amount == 0
    end

    raise InsufficientChangeError.new(amount)
  end

  def inventory(coin=nil)
    return @sorter[coin] unless coin.nil?
    @sorter
  end

  def total
    amount = 0

    VALID_COINS.each do |value|
      amount += @sorter[value] * value
    end

    amount
  end

  private

  def init_sorter
    sorter = {}
    VALID_COINS.each{|value| sorter[value] = 0}
    sorter
  end

  def release_coins(value, count)
    # Release coins at given value up to count
    # If not enough coins, release what you got.
    count = @sorter[value] if @sorter[value] < count

    @sorter[value] = @sorter[value] - count
    [value] * count
  end
end
