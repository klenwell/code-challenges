require_relative "../lib/vending_machine/coin_sorter"

# rubocop: disable Metrics/BlockLength
RSpec.describe CoinSorter do
  # For bins comparisons, this sets up an empty bin
  let(:empty_bins) { subject.load({}) }

  describe '.new' do
  end

  describe '#deposit' do
    it { is_expected.to respond_to(:deposit).with(1).argument }

    context 'when coin is valid' do
      it { expect(subject.deposit(10)).to eq(10) }
    end

    context 'when coin is invalid' do
      it { expect { subject.deposit(3) }.to raise_error(described_class::InvalidCoinError) }
    end
  end

  describe '#load' do
    it { is_expected.to respond_to(:load).with(1).argument }

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
    it { is_expected.to respond_to(:roll).with(1).argument }

    it 'sorts a list of coins into rolls (or frequency hash)' do
      # Arrange
      coins = [1, 2, 2, 5, 5, 5]

      # Act
      rolls = subject.roll(coins)

      # Assert
      expect(rolls).to eq({ 1 => 1, 2 => 2, 5 => 3 })
    end

    context 'when some coins are invalid' do
      it 'rolls the invalid coins' do
        # Arrange
        coins = [1, 2, 2, 3, 3, 3]

        # Act
        rolls = subject.roll(coins)

        # Assert
        expect(rolls).to eq({ 1 => 1, 2 => 2, 3 => 3 })
      end
    end

    context 'when a cheetoh is mixed with the coins' do
      it 'rolls the cheetoh, too!' do
        # Arrange
        coins = [1, 2, 2, :cheetoh]

        # Act
        rolls = subject.roll(coins)

        # Assert
        expect(rolls).to eq({ 1 => 1, 2 => 2, :cheetoh => 1 })
      end
    end
  end

  describe '#make_change' do
    it { is_expected.to respond_to(:make_change).with(1).argument }

    before(:each) do
      rolls = { 1 => 10, 2 => 5, 5 => 2, 10 => 2 }
      subject.load(rolls)
    end

    context 'when exact change is available' do
      it { expect(subject.make_change(10)).to eq([10]) }
      it { expect(subject.make_change(20)).to eq([10, 10]) }
      it { expect(subject.make_change(35)).to eq([10, 10, 5, 5, 2, 2, 1]) }
      it { expect(subject.make_change(50)).to eq([10, 10, 5, 5] + ([2] * 5) + ([1] * 10)) }

      it 'will update coin inventory correctly' do
        # Assume
        expect(subject.inventory(10)).to eq(2)
        expect(subject.inventory(5)).to eq(2)
        expect(subject.total).to eq(50)

        # Act
        coins = subject.make_change(25)

        # Assert
        expect(coins).to eq([10, 10, 5])
        expect(subject.inventory(10)).to eq(0)
        expect(subject.inventory(5)).to eq(1)
        expect(subject.total).to eq(25)
      end
    end

    context 'when exact change is not available' do
      it 'will throw error and replace any released coins' do
        # Arrange
        num_coins_before = subject.inventory.values.sum
        total_funds_before = subject.total

        # Act
        expect { subject.make_change(51) }.to raise_error(described_class::InsufficientChangeError)

        # Assert
        expect(subject.inventory.values.sum).to eq(num_coins_before)
        expect(subject.total).to eq(total_funds_before)
      end
    end
  end

  # TODO: inventory to sort
  describe '#inventory' do; end

  # TODO: total to sum
  describe '#total' do; end
end
# rubocop: enable Metrics/BlockLength
