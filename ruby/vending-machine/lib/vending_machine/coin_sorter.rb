class CoinSorter
  VALID_COINS = [1, 2, 5, 10, 20, 50, 100, 200].freeze

  InvalidCoinError = Class.new(StandardError)
  InsufficientChangeError = Class.new(StandardError)

  def initialize(rolls=nil)
    @bins = init_bins
    load(rolls) unless rolls.nil?
  end

  def deposit(coin)
    raise InvalidCoinError.new(coin) unless VALID_COINS.include? coin

    @bins[coin] += 1
    coin
  end

  def load(rolls)
    # rolls is a frequency hash: coin => count
    @bins.each_key do |value|
      @bins[value] += rolls.fetch(value, 0)
    end
    @bins
  end

  def roll(coins)
    # Convert a list of coins to a frequency hash.
    rolls = Hash.new(0)
    coins.each { |value| rolls[value] += 1 }
    rolls
  end

  def make_change(amount)
    coins = []

    # Go backwards through the sort to make change
    VALID_COINS.sort.reverse.each do |value|
      count = amount / value
      released_coins = release_coins(value, count)
      coins.concat(released_coins)
      amount -= released_coins.sum
      return coins if amount == 0
    end

    # If we couldn't make change, replace coins and raise error.
    load(roll(coins))
    raise InsufficientChangeError.new(amount)
  end

  def sort
    @bins
  end

  def select(coin)
    @bins[coin]
  end

  def sum
    amount = 0

    VALID_COINS.each do |value|
      amount += @bins[value] * value
    end

    amount
  end

  private

  def init_bins
    bins = {}
    VALID_COINS.each { |value| bins[value] = 0 }
    bins
  end

  def release_coins(value, count)
    # Release coins at given value up to count
    # If not enough coins, release what you got.
    count = @bins[value] if @bins[value] < count

    @bins[value] = @bins[value] - count
    [value] * count
  end
end
