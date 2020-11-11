require_relative "../lib/vending_machine/coin_sorter"

RSpec.describe CoinSorter do
  # For bins comparisons, this sets up an empty bin
  let(:empty_bins) { subject.load({}) }

  describe '.new' do
  end

  describe '#deposit' do
    it { is_expected.to respond_to(:deposit).with(1).arguments }

    context 'when coin is valid' do
      it { expect(subject.deposit(10)).to eq(10) }
    end

    context 'when coin is invalid' do
      it { expect { subject.deposit(3) }.to raise_error(described_class::InvalidCoinError) }
    end
  end

  describe '#load' do
    it { is_expected.to respond_to(:load).with(1).arguments }

    it 'sorts rolls into bins' do
      # Arrange
      rolls = { 1 => 10, 2 => 5, 5 => 2 }
      expected_bins = empty_bins.merge(rolls)

      # Act
      bins = subject.load(rolls)

      # Assert
      expect(bins).to eq(expected_bins)
    end

    context 'when a roll of coins is invalid' do
      it 'discards rolls of invalid coins' do
        # Arrange
        rolls = { 1 => 1, 3 => 1, 4 => 1 }
        expected_bins = empty_bins.merge({ 1 => 1 })

        # Act
        bins = subject.load(rolls)

        # Assert
        expect(bins).to eq(expected_bins)
      end
    end
  end

  describe '#roll' do
    it { is_expected.to respond_to(:roll).with(1).arguments }

    it 'sorts a list of coins into rolls (or frequency hash)' do
      # Arrange
      coins = [1, 2, 2, 5, 5, 5]

      # Act
      rolls = subject.roll(coins)

      # Assert
      expect(rolls).to eq({1 => 1, 2 => 2, 5 => 3})
    end

    context 'when some coins are invalid' do
      it 'rolls the invalid coins' do
        # Arrange
        coins = [1, 2, 2, 3, 3, 3]

        # Act
        rolls = subject.roll(coins)

        # Assert
        expect(rolls).to eq({1 => 1, 2 => 2, 3 => 3})
      end
    end

    context 'when a cheetoh is mixed with the coins' do
      it 'rolls the cheetoh, too!' do
        # Arrange
        coins = [1, 2, 2, :cheetoh]

        # Act
        rolls = subject.roll(coins)

        # Assert
        expect(rolls).to eq({1 => 1, 2 => 2, :cheetoh => 1})
      end
    end
  end

  describe '#make_change' do; end

  # TODO: inventory to sort
  describe '#inventory' do; end

  # TODO: total to sum
  describe '#total' do; end
end
